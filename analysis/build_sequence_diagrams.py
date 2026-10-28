"""Build fresh EPS analysis sequence diagrams with the drawio-skill engine.

The approved use-case JSON files are the source of scope and traceability.
No old diagram is opened or reused. All coordinates for lifelines, activations,
and messages come from seqlayout.layout; only UML combined fragments, the
page title, and a notation key are added after deterministic sequence layout.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SKILL = Path(r"C:\Users\lenovo\.codex\skills\drawio-skill")
OUTPUT = HERE / "diagrams" / "sequence"


def m(src, dst, label, **kw):
    return {"from": src, "to": dst, "label": label, **kw}


def r(src, dst, label):
    return m(src, dst, label, **{"return": True})


def a(src, dst, label):
    return m(src, dst, label, **{"async": True, "activate": False})


def note(over, text):
    return {"note": text, "over": over}


def alt(*branches):
    return {"fragment": "alt", "branches": [{"guard": guard, "steps": steps} for guard, steps in branches]}


def opt(guard, *steps):
    return {"fragment": "opt", "branches": [{"guard": guard, "steps": list(steps)}]}


def p(pid, label, role="entity", actor=False):
    return {"id": pid, "label": label if actor else f"«{role}»\n{label}", "role": role, "actor": actor}


def human(actor="Buyer / Seller", entity="Escrow", control="Escrow Control", boundary="Escrow UI", audit=True):
    parts = [p("user", actor, "actor", True), p("ui", boundary, "boundary"),
             p("ctrl", control, "control"), p("record", entity)]
    if audit:
        parts.append(p("audit", "Audit Trail"))
    return parts


def human_start(request, check="Authorize participant; check state"):
    return [m("user", "ui", request), m("ui", "ctrl", "MFA session identity + request"),
            m("ctrl", "record", check), r("record", "ctrl", "Identity, scope and current state")]


def deny(text="Invalid MFA, wrong party or stale state"):
    return (text, [r("ctrl", "ui", "Reject without state change"), r("ui", "user", "Denied / authorized current status")])


def audited(action):
    return [m("ctrl", "audit", action)]


def ref(target, label):
    return {"ref": target, "label": label}


MODELS = {}


def add(uid, parts, steps, notes=None):
    MODELS[uid] = {"id": uid, "participants": parts, "steps": steps, "notes": notes or []}


# Human account lifecycle: no escrow state or real money is created here.
add("U1", human("Guest", "Account", "Account Control", "Account UI"), [
    m("user", "ui", "Submit ordinary-account registration"),
    m("ui", "ctrl", "Identifier, password, display name"),
    m("ctrl", "record", "Validate ordinary role + uniqueness"),
    r("record", "ctrl", "Validation and uniqueness result"),
    alt(("Valid input; ordinary role only", [
        m("ctrl", "record", "Create inactive enrollment record"),
        r("ctrl", "ui", "MFA enrollment instructions"),
        r("ui", "user", "Complete enrollment challenge"),
        m("user", "ui", "Submit enrollment response"),
        m("ui", "ctrl", "Verify current enrollment response"),
        alt(("MFA confirmed; identifier still unique", [
            m("ctrl", "record", "Activate ordinary account once"),
            *audited("Record registration; omit secrets"),
            r("ctrl", "ui", "Registration succeeded; no session"),
            r("ui", "user", "Continue to U2 Login with MFA")]),
            ("Invalid / expired factor or uniqueness race", [
                r("ctrl", "ui", "No usable account / conflict"),
                r("ui", "user", "Restart enrollment or correct input")]))]),
        ("Invalid input / duplicate / privileged role", [
            r("ctrl", "ui", "Reject registration / privilege request"),
            r("ui", "user", "No privileged or duplicate account")]))
], ["Public registration never grants Admin or Merchant access."])

add("U2", human("Human user", "Account + Session", "Access Control", "Login UI"), [
    m("user", "ui", "Submit identifier + primary credential"),
    m("ui", "ctrl", "Authenticate human account"),
    m("ctrl", "record", "Validate active account + credential"),
    r("record", "ctrl", "Primary-credential result"),
    alt(("Valid primary credential and active account", [
        r("ctrl", "ui", "Issue short-lived MFA challenge"),
        r("ui", "user", "Request enrolled-factor response"),
        m("user", "ui", "Submit MFA response"),
        m("ui", "ctrl", "Verify current unconsumed challenge"),
        alt(("MFA valid; account still eligible", [
            m("ctrl", "record", "Consume challenge; create session"),
            *audited("Record login without secrets"),
            r("ctrl", "ui", "Authenticated identity + existing rights"),
            r("ui", "user", "Open permitted starting view")]),
            ("Invalid, expired, replayed or ineligible", [
                *audited("Record failed authentication safely"),
                r("ctrl", "ui", "No authenticated session"),
                r("ui", "user", "Generic failure / new challenge")]))]),
        ("Unknown / invalid / inactive account", [
            r("ctrl", "ui", "Generic login failure"),
            r("ui", "user", "Protected operations unavailable")]))
], ["Admin is pre-provisioned. Merchant credentials use a separate client flow."])

add("U3", human("Human user", "Session", "Access Control", "Account UI"), [
    m("user", "ui", "Select Logout"), m("ui", "ctrl", "Invalidate current session"),
    m("ctrl", "record", "Revoke session reference"),
    alt(("Revocation confirmed or session already invalid", [
        r("record", "ctrl", "Session cannot be reused"),
        opt("An active session existed", *audited("Record active-session logout")),
        r("ctrl", "ui", "Logout confirmed"),
        r("ui", "user", "Clear local access; show Login")]),
        ("Interruption; revocation not confirmed", [
            r("record", "ctrl", "Revocation unresolved"),
            r("ctrl", "ui", "Clear local session; report uncertainty"),
            r("ui", "user", "Local access ended; confirmation pending"),
            opt("Connectivity restored", m("ui", "ctrl", "Retry original session revocation"))]))
], ["Already accepted funding/payout requests survive logout."])

add("U4", human(audit=False), [
    *human_start("Open own escrow list / details", "Authorize participant-scoped read"),
    alt(("MFA valid; participant scope; snapshot available", [
        m("ctrl", "record", "Read terms, policy + status snapshot"),
        r("record", "ctrl", "Lifecycle, proposal, dispute, attempt"),
        r("ctrl", "ui", "Authorized snapshot + allowed actions"),
        r("ui", "user", "Show explicit pending / final result"),
        opt("Caller refreshes", m("user", "ui", "Request another read"),
            m("ui", "ctrl", "Reauthorize and reread current state"))]),
        ("Authorized empty result", [r("ctrl", "ui", "Empty list"), r("ui", "user", "No matching escrows")]),
        ("Authorized retrieval temporarily unavailable", [
            r("ctrl", "ui", "Temporary retrieval error"), r("ui", "user", "No invented status or result")]),
        deny("Invalid MFA / unknown or unauthorized reference"))
], ["Read only. PENDING/UNKNOWN is never HELD or a final payout result.",
    "Every subsequent write rechecks permissions and current state."])

add("U5", human(entity="Escrow + Dispute"), [
    *human_start("Submit dispute reason + initial proof", "Check party, HELD/DELIVERED + no intent"),
    alt(("Funds held; no prior dispute or payout intent", [
        m("ctrl", "record", "Atomic OPEN + INVALIDATED offer + evidence"),
        r("record", "ctrl", "One dispute; participant choices blocked"),
        *audited("Record opening and proposal invalidation"),
        r("ctrl", "ui", "Dispute reference; funds remain held"),
        r("ui", "user", "OPEN dispute; evidence window available")]),
        ("Same opening operation already accepted", [
            r("ctrl", "ui", "Existing dispute reference; no duplicate"),
            r("ui", "user", "Show existing authorized dispute")]),
        deny("Payout pending / prior dispute / unheld / invalid caller"))
], ["The atomic opening invalidates any PENDING refund offer.",
    "First valid transition wins; no new dispute after payout reservation."])

add("U6", human(entity="Dispute + Evidence", control="Dispute Control"), [
    *human_start("Submit explanation / evidence", "Authorize participant + OPEN dispute"),
    alt(("Valid evidence; OPEN at atomic append", [
        m("ctrl", "record", "Append evidence, author, time + revision"),
        *audited("Record evidence receipt, not secrets"),
        r("ctrl", "ui", "Saved receipt; update Admin review set"),
        r("ui", "user", "Evidence visible to parties and Admin")]),
        ("Repeated identical submission reference", [
            r("ctrl", "ui", "Existing receipt; no duplicate evidence"),
            r("ui", "user", "Original submission retained")]),
        deny("Admin decision committed first / invalid evidence / caller"))
], ["If evidence commits first, Admin must review the updated evidence revision.",
    "If decision commits first, the evidence window is closed."])

add("U7", human(entity="Escrow + Proposal"), [
    *human_start("Propose or withdraw full refund", "Authorize participant; HELD/DELIVERED"),
    alt(("Propose; no active offer, dispute or payout", [
        m("ctrl", "record", "Atomic PENDING offer + identities/source"),
        r("record", "ctrl", "PENDING: block delivery + buyer release"),
        *audited("Record proposal reason and identity"),
        r("ctrl", "ui", "PENDING; delivery and release frozen"),
        r("ui", "user", "Await counterparty acceptance / rejection")]),
        ("Withdraw; caller owns still-PENDING offer", [
            m("ctrl", "record", "Atomically set WITHDRAWN; retain history"),
            *audited("Record proposer withdrawal"),
            r("ctrl", "ui", "Keep delivery state; recheck actions"),
            r("ui", "user", "No refund instruction created")]),
        deny("Stale / wrong party / dispute / payout pending"))
], ["A PENDING offer freezes seller completion recording and buyer release; all funds remain held.",
    "Rejection/withdrawal restores eligible actions without reverting existing delivery. Acceptance/dispute blocks stale withdrawal."])

u8parts = human("Counterparty", "Escrow + Proposal") + [p("pay", "Payment Control", "control")]
add("U8", u8parts, [
    *human_start("Accept or reject full-refund proposal", "Check other party + PENDING offer"),
    alt(("Accept; still held; no dispute or payout", [
        m("ctrl", "record", "Atomic APPROVED + REFUND_PENDING intent"),
        r("record", "ctrl", "Both consents; full amount reserved"),
        *audited("Record mutual consent + full refund intent"),
        m("ctrl", "pay", "P3: full refund to original source"),
        r("pay", "ctrl", "Current refund attempt / result"),
        r("ctrl", "ui", "Pending until verified provider success"),
        r("ui", "user", "Show REFUND_PENDING or REFUNDED")]),
        ("Reject; valid other party and active offer", [
            m("ctrl", "record", "Set REJECTED; no payout authorization"),
            *audited("Record counterparty rejection"),
            r("ctrl", "ui", "Other eligible actions restored"),
            r("ui", "user", "Funds remain held")]),
        deny("Self-accept / withdrawn / invalidated / payout race"))
], ["Once REFUND_PENDING, new dispute and opposite release are blocked.",
    "Duplicate acceptance returns the existing intent; unknown results use A5."])

add("B1", human("Buyer", "Escrow + Policy"), [
    *human_start("Submit seller, terms + full VND amount", "Check actual buyer; different active seller"),
    alt(("Valid goods/service agreement; VND > 0", [
        m("ctrl", "record", "Capture one complete policy version"),
        m("ctrl", "record", "Create once; set AWAITING_SELLER"),
        *audited("Record creation + operation reference"),
        r("ctrl", "ui", "Escrow reference + policy snapshot"),
        r("ui", "user", "Seller acceptance needed; no funds held")]),
        ("Same operation reference and identical terms", [
            r("ctrl", "ui", "Return original escrow"),
            r("ui", "user", "Track same agreement; no duplicate")]),
        deny("Invalid parties / self-trade / terms / changed duplicate"))
], ["Terms and policy are captured at creation; no edit use case exists.",
    "Funding remains unavailable until seller accepts in S1."])

add("B2", human("Buyer", "Escrow + Attempt"), [
    *human_start("Cancel unfunded escrow", "Check buyer, unfunded state + all attempts"),
    alt(("AWAITING_SELLER/FUNDING; no possible receipt", [
        m("ctrl", "record", "Atomic CANCELLED; disable funding"),
        *audited("Record cancellation; preserve history"),
        r("ctrl", "ui", "CANCELLED; no refund required"),
        r("ui", "user", "Agreement closed")]),
        ("Already CANCELLED", [r("ctrl", "ui", "Return original cancellation"), r("ui", "user", "CANCELLED")]),
        deny("Funding won race / PENDING or UNKNOWN / held funds"))
], ["Cancellation is allowed only before funding or after confirmed no-collection failure."])

fundparts = human("Buyer", "Escrow + Attempt") + [p("provider", "Selected Funding Mock", "external")]
add("B3", fundparts, [
    *human_start("Accept captured terms; choose funding mock", "Check buyer; seller accepted; no active attempt"),
    alt(("AWAITING_FUNDING; eligible full VND funding", [
        m("ctrl", "record", "Reserve attempt; set FUNDING_PENDING"),
        *audited("Record buyer acceptance + funding attempt"),
        m("ctrl", "provider", "Fund full VND amount; stable references"),
        alt(("Provider result returned / later callback", [
            a("provider", "ctrl", "P1: authenticated funding result"),
            r("ctrl", "ui", "P1-verified current funding result"),
            r("ui", "user", "HELD only after confirmed receipt")]),
            ("Timeout or ambiguous dispatch/result", [
                m("ctrl", "record", "Keep FUNDING_PENDING; attempt UNKNOWN"),
                r("ctrl", "ui", "Original attempt awaits A5 query"),
                r("ui", "user", "No second funding or cancellation")]))]),
        ("Identical operation already accepted", [
            r("ctrl", "ui", "Existing funding attempt/result"),
            r("ui", "user", "No new collection")]),
        deny("Unaccepted / cancelled / held / unresolved prior attempt"))
], ["Choose one of Bank mock or Gateway mock for each eligible attempt.",
    "A browser redirect or button click never establishes HELD."])

releaseparts = human("Buyer", "Escrow + Attempt") + [p("pay", "Payment Control", "control")]
add("B4", releaseparts, [
    *human_start("Accept full completion; request release", "Check buyer, DELIVERED + captured evidence"),
    alt(("No PENDING offer, dispute or payout; funds held", [
        m("ctrl", "record", "Atomic acceptance + RELEASE_PENDING lock"),
        r("record", "ctrl", "Full amount reserved; choices closed"),
        *audited("Record attributable buyer release intent"),
        m("ctrl", "pay", "P2: full seller payout via Bank mock"),
        r("pay", "ctrl", "Current attempt; confirmed / unresolved"),
        r("ctrl", "ui", "RELEASED only on verified Bank success"),
        r("ui", "user", "Final result or RELEASE_PENDING")]),
        ("Same accepted release operation repeated", [
            r("ctrl", "ui", "Existing intent and attempt result"),
            r("ui", "user", "No second seller payout")]),
        deny("Active refund offer / dispute / missing proof / payout race"))
], ["PENDING refund proposal blocks normal release. Delivery alone is insufficient.",
    "After RELEASE_PENDING, opposite payout and new dispute are blocked."])

add("S1", human("Seller", "Escrow + Terms"), [
    *human_start("Review terms; choose Accept or Reject", "Check named seller + AWAITING_SELLER"),
    alt(("Accept; proposal still awaits seller", [
        m("ctrl", "record", "Freeze terms; set AWAITING_FUNDING"),
        *audited("Record seller acceptance"),
        r("ctrl", "ui", "Seller accepted; buyer may fund"),
        r("ui", "user", "Accepted immutable agreement")]),
        ("Reject; proposal still awaits seller", [
            m("ctrl", "record", "CANCELLED; reason SELLER_REJECTED"),
            *audited("Record seller rejection"),
            r("ctrl", "ui", "Proposal closed; funding blocked"),
            r("ui", "user", "CANCELLED")]),
        deny("Buyer cancelled / opposite response / invalid seller"))
], ["A repeated identical response returns the original result.",
    "Correcting accepted terms requires eligible cancellation and new creation."])

add("S2", human("Seller", "Escrow + Delivery"), [
    *human_start("Submit goods/service completion + proof", "Check named seller, HELD + policy snapshot"),
    alt(("HELD; no offer/dispute/payout; proof satisfied", [
        m("ctrl", "record", "Save delivery/work record; set DELIVERED"),
        *audited("Record seller completion"),
        r("ctrl", "ui", "Completion saved; full funds remain held"),
        r("ui", "user", "Await buyer review / acceptance")]),
        ("Same completion operation repeated", [
            r("ctrl", "ui", "Return existing completion receipt"),
            r("ui", "user", "No second completion or payout")]),
        deny("Missing required proof / proposal / dispute / payout"))
], ["Use the evidence policy saved at creation, never today's policy.",
    "Defaults: Goods optional; Services required. Completion never auto-releases."])

a1parts = human("Admin", "Escrow + Dispute", "Dispute Control", "Admin UI") + [p("pay", "Payment Control", "control")]
add("A1", a1parts, [
    *human_start("Review OPEN dispute + all evidence", "Authorize Admin; load latest evidence revision"),
    m("ctrl", "record", "Read immutable terms + evidence + history"),
    r("record", "ctrl", "Review set, full amount and revision"),
    r("ctrl", "ui", "Two full outcomes + complete review set"),
    m("user", "ui", "Choose Release or Refund; enter rationale"),
    m("ui", "ctrl", "Submit final decision + reviewed revision"),
    alt(("OPEN; latest evidence reviewed; no payout intent", [
        m("ctrl", "record", "Atomic RESOLVED + payout lock + evidence closed"),
        r("record", "ctrl", "Immutable decision; RELEASE/REFUND_PENDING"),
        *audited("Record Admin, rationale + direction"),
        m("ctrl", "pay", "P2 release or P3 refund; full amount"),
        r("pay", "ctrl", "Current payment attempt/result"),
        r("ctrl", "ui", "Decision final; payment separately pending"),
        r("ui", "user", "Provider confirmation decides money success")]),
        ("New evidence arrived before commit", [
            r("ctrl", "ui", "Reload evidence; decision not committed"),
            r("ui", "user", "Review updated record before deciding")]),
        deny("Not Admin / rationale absent / already resolved / race"))
], ["Admin decision is separately audited authority; normal buyer release remains explicit.",
    "No appeal or split outcome. Failed payout keeps the chosen direction locked."])

add("A2", human("Admin", "Policy Version", "Policy Control", "Admin UI"), [
    *human_start("Open evidence policy configuration", "Authorize Admin; load active policy version"),
    r("ctrl", "ui", "Goods/Services evidence flags + version"),
    m("user", "ui", "Save evidence-required flags + reason"),
    m("ui", "ctrl", "Boolean settings + reviewed version"),
    alt(("Changed valid flags; reason; version still current", [
        m("ctrl", "record", "Publish new complete policy version"),
        *audited("Record before/after, Admin + reason"),
        r("ctrl", "ui", "New policy for future creation only"),
        r("ui", "user", "Existing escrow snapshots unchanged")]),
        ("Identical settings; no policy change", [
            r("ctrl", "ui", "Return current policy version"),
            r("ui", "user", "No new version published")]),
        ("Another Admin changed policy", [
            r("ctrl", "ui", "Version conflict; reload latest policy"),
            r("ui", "user", "Review before resubmitting")]),
        deny("Unauthorized / unsupported settings / invalid values"))
], ["Only evidence-required per Goods/Services is editable in the MVP.",
    "No fees, currency, automatic release or split-payment controls."])

add("A3", human("Admin", "Analytics View", "Analytics Control", "Admin UI", audit=False), [
    *human_start("Request dashboard; date/type filters", "Authorize Admin; validate filters"),
    alt(("Authorized; valid filters; data available", [
        m("ctrl", "record", "Aggregate counts and simulated VND sums"),
        r("record", "ctrl", "Held, released, refunded + unresolved counts"),
        r("ctrl", "ui", "Results, filter interval + refresh time"),
        r("ui", "user", "Read-only mock-data dashboard")]),
        ("Valid filters; no matching records", [
            r("ctrl", "ui", "Zero totals; explicit empty result"),
            r("ui", "user", "No matching mock escrows")]),
        ("Aggregation unavailable", [
            r("ctrl", "ui", "Refresh failed; no invented totals"),
            r("ui", "user", "Prior timestamp shown if retaining old view")]),
        deny("Invalid MFA / role / filter interval"))
], ["Pending/failed reserved payouts count within held funds exactly once.",
    "Unconfirmed funding is excluded from held amounts."])

add("A4", human("Admin", "Audit Trail", "Audit Control", "Admin UI", audit=False), [
    *human_start("Request audit history + filters", "Authorize Admin read; validate scope"),
    alt(("Authorized read; records available", [
        m("ctrl", "record", "Read chronological immutable events"),
        r("record", "ctrl", "Time, actor, reference, state, reason"),
        r("ctrl", "ui", "Filtered events; mask sensitive fields"),
        r("ui", "user", "Read-only audit with correlated details")]),
        ("Authorized; no matching event", [
            r("ctrl", "ui", "Empty audit result"),
            r("ui", "user", "No event inferred or synthesized")]),
        ("Audit retrieval temporarily unavailable", [
            r("ctrl", "ui", "Audit unavailable; stored history unchanged"),
            r("ui", "user", "No synthesized event or money result")]),
        deny("Unauthorized, invalid filters or attempted mutation"))
], ["No Admin edit/delete action. Passwords, codes, tokens and client secrets are excluded.",
    "Audit history does not substitute for provider confirmation."])

a5parts = human("Admin", "Escrow + Attempt", "Payment Control", "Admin UI") + [p("provider", "Responsible Mock", "external")]
add("A5", a5parts, [
    *human_start("Inspect attempt; request reconciliation", "Authorize Admin; load original references"),
    alt(("MFA valid; authorized Admin; recorded original attempt", [
      m("ctrl", "provider", "Query original attempt; no money instruction"),
      r("provider", "ctrl", "Authenticated correlated status"),
      alt(("SUCCEEDED; valid references and full amount", [
        m("ctrl", "record", "Apply P1/P2/P3 confirmation exactly once"),
        *audited("Record authoritative reconciliation result"),
        r("ctrl", "ui", "HELD / RELEASED / REFUNDED as applicable")]),
        ("PENDING / UNKNOWN / timeout / mismatch", [
            m("ctrl", "record", "Keep pending; preserve payout reservation"),
            r("ctrl", "ui", "Query-only; retry and manual success denied")]),
        ("Funding FAILED; authoritative no collection", [
            m("ctrl", "record", "Attempt FAILED; AWAITING_FUNDING"),
            r("ctrl", "ui", "Buyer may use B3/B2; Admin cannot fund")]),
        ("Payout FAILED; authoritative no money moved", [
            m("ctrl", "record", "Keep *_PENDING; attempt FAILED"),
            r("ctrl", "ui", "Same approved direction eligible for retry"),
            opt("Admin explicitly retries; no active/newer attempt", 
                m("user", "ui", "Retry the approved full payout"),
                m("ui", "ctrl", "Retry same amount, recipient + direction"),
                m("ctrl", "record", "Atomic new linked attempt; retain decision"),
                m("ctrl", "provider", "P2/P3: execute one linked retry"),
                *audited("Record retry and old/new references"))])),
      r("ui", "user", "Display truthful current status")]),
      deny("Unauthorized Admin / invalid MFA / unknown attempt"))
], ["Unknown results are query-only. Only final failure proving no movement permits retry.",
    "Callback/query races share one atomic confirmation path; no manual success."])

# Provider integrations use conceptual boundaries, controls, and domain entities.
p1parts = [p("provider", "Selected Funding Mock", "external"), p("boundary", "Payment Boundary", "boundary"),
           p("ctrl", "Payment Control", "control"), p("record", "Escrow + Attempt"), p("audit", "Audit Trail")]
add("P1", p1parts, [
    a("provider", "boundary", "Funding callback / queried status"),
    m("boundary", "ctrl", "Authenticate result + correlate attempt"),
    m("ctrl", "record", "Match provider, operation, escrow + VND amount"),
    r("record", "ctrl", "Expected attempt + current money state"),
    alt(("Verified SUCCEEDED; eligible PENDING/UNKNOWN attempt", [
        m("ctrl", "record", "Atomic attempt SUCCEEDED + HELD once"),
        m("ctrl", "record", "Retain original funding provider/source"),
        *audited("Record full confirmed mock receipt"),
        r("ctrl", "boundary", "Confirmation applied once")]),
        ("Verified FAILED; no collection and no prior success", [
            m("ctrl", "record", "Attempt FAILED; AWAITING_FUNDING"),
            *audited("Record authoritative no-receipt failure"),
            r("ctrl", "boundary", "Failure stored; no held-money credit")]),
        ("PENDING / UNKNOWN; attempt not already final", [
            m("ctrl", "record", "Keep FUNDING_PENDING + attempt status"),
            r("ctrl", "boundary", "No cancel, second funding or delivery")]),
        ("Same applied success or stale nonfinal after success", [
            r("ctrl", "boundary", "Acknowledge duplicate; no extra credit")]),
        ("Invalid, mismatched or contradictory final result", [
            *audited("Flag discrepancy safely; omit secrets"),
            r("ctrl", "boundary", "Reject/quarantine; preserve money state")])) ,
    r("boundary", "provider", "Stored acknowledgement / rejected result")
], ["A late matching success after UNKNOWN may apply once; no client click proves receipt.",
    "Contradiction after final failure/cancellation cannot reopen or credit twice."])


def payout(uid, outcome, caller, providerlabel, finalstate, detail):
    parts = [p("caller", caller, "control"), p("ctrl", "Payment Control", "control"),
             p("record", "Escrow + Attempt"), p("boundary", "Payment Boundary", "boundary"),
             p("provider", providerlabel, "external"), p("audit", "Audit Trail")]
    pending = "RELEASE_PENDING" if uid == "P2" else "REFUND_PENDING"
    add(uid, parts, [
        m("caller", "ctrl", f"Execute authorized full {outcome.lower()}"),
        m("ctrl", "record", "Check saved decision, reservation + attempt"),
        r("record", "ctrl", "Full VND amount + approved destination"),
        alt(("Valid intent; no competing active attempt", [
            m("ctrl", "boundary", f"Send {outcome}; stable operation reference"),
            m("boundary", "provider", detail),
            r("ctrl", "caller", f"{pending}; not final success"),
            ref(uid + "_settlement", "Callback/status settlement; unknown results use A5")]),
            ("Invalid authorization / destination / opposite intent", [
                r("ctrl", "caller", "Reject before calling provider")]))
    ], ["Decision and exclusive full-amount reservation are saved before the external call.",
        "Timeout keeps attempt UNKNOWN and the reservation; A5 queries the original reference without a new transfer."])
    settlement = [p("provider", providerlabel, "external"), p("boundary", "Payment Boundary", "boundary"),
                  p("ctrl", "Payment Control", "control"), p("record", "Escrow + Attempt"), p("audit", "Audit Trail")]
    add(uid + "_settlement", settlement, [
        a("provider", "boundary", "Callback / original-attempt query result"),
        m("boundary", "ctrl", "Authenticate provider + correlate full result"),
        m("ctrl", "record", "Match intent, attempt, amount + destination"),
        r("record", "ctrl", "Recorded references + finality status"),
        alt(("SUCCEEDED; matched; not already applied", [
            m("ctrl", "record", f"Atomic SUCCEEDED + {finalstate} once"),
            *audited(f"Record confirmed full {outcome.lower()}")]),
            ("FAILED; final no movement; no earlier success", [
                m("ctrl", "record", f"Attempt FAILED; retain {pending}"),
                *audited("Record failure; same-direction retry via A5")]),
            ("PENDING / UNKNOWN; no final success", [
                m("ctrl", "record", f"Keep {pending}; query-only reconciliation")]),
            ("Same success applied / stale nonfinal", [
                r("ctrl", "boundary", "Existing outcome; no extra transfer")]),
            ("Invalid, unmatched or contradictory final result", [
                *audited("Flag discrepancy; preserve money state")])),
        r("ctrl", "boundary", "Stored current result / rejected mismatch"),
        r("boundary", "provider", "Acknowledge accepted result / reject invalid")
    ], ["The callback and query paths use the same atomic, duplicate-safe confirmation.",
        "Refunds retain the original provider/source; release uses Bank mock. No opposite outcome or new dispute after reservation."])
    MODELS[uid + "_settlement"]["logical_id"] = uid
    MODELS[uid + "_settlement"]["entry_guard"] = "A saved full payout intent and original attempt already exist"
    MODELS[uid + "_settlement"]["module_title"] = "Provider settlement and duplicate handling"


payout("P2", "Release", "B4 / A1 / A5", "Partner Bank Mock", "RELEASED",
       "Full VND seller payout; same seller destination")
payout("P3", "Refund", "U8 / A1 / A5", "Original Funding Mock", "REFUNDED",
       "Full VND refund; original funding reference/source")

api_create_parts = [p("merchant", "Merchant / Marketplace", "external"), p("boundary", "Merchant Boundary", "boundary"),
                    p("access", "Client Access", "control"), p("ctrl", "Escrow Control", "control"),
                    p("record", "Escrow + Policy"), p("audit", "Audit Trail")]
add("B1.API", api_create_parts, [
    m("merchant", "boundary", "Create: client ref, parties, VND + terms"),
    m("boundary", "access", "Verify separate Merchant credential"),
    r("access", "boundary", "Client identity + seller binding"),
    alt(("Client valid; seller matches pre-provisioned binding", [
        m("boundary", "ctrl", "B1 shared rules + Merchant association"),
        m("ctrl", "record", "Validate parties; snapshot one policy version"),
        alt(("New scoped reference; valid shared B1 terms", [
            m("ctrl", "record", "Create once; AWAITING_SELLER"),
            m("ctrl", "record", "Persist originating Merchant + client ref"),
            *audited("Record scoped Merchant creation"),
            r("ctrl", "boundary", "Escrow ref, client ref, policy + status")]),
            ("Same scoped reference, identical content", [
                r("ctrl", "boundary", "Original escrow; no duplicate creation")]),
            ("Changed reference content / invalid terms / role flags", [
                r("ctrl", "boundary", "Reject scope or shared-rule violation")]))]),
        ("Invalid client or unbound seller", [
            r("boundary", "merchant", "Scoped denial; no escrow data")])) ,
    r("boundary", "merchant", "Created/original result or scoped error")
], ["Real seller performs S1; actual buyer performs B3/B4 with human MFA.",
    "Merchant cannot assert consent, funding success, delivery, refund or dispute."])

api_read_parts = [p("merchant", "Merchant / Marketplace", "external"), p("boundary", "Merchant Boundary", "boundary"),
                  p("access", "Client Access", "control"), p("ctrl", "Escrow Control", "control"), p("record", "Escrow + Attempt")]
add("U4.API", api_read_parts, [
    m("merchant", "boundary", "Query own escrow / scoped client reference"),
    m("boundary", "access", "Verify separate Merchant credential"),
    r("access", "boundary", "Client authentication result"),
    alt(("Separate Merchant authentication valid", [
      m("boundary", "ctrl", "Apply U4 with originating-client scope"),
      m("ctrl", "record", "Authorize immutable Merchant association"),
      alt(("Own known escrow; truthful snapshot available", [
        r("record", "ctrl", "Consistent lifecycle + attempt snapshot"),
        r("ctrl", "boundary", "Refs, type, VND + reconciliation status"),
        r("boundary", "merchant", "Authorized snapshot; pending stays pending"),
        opt("Merchant polls again", m("merchant", "boundary", "Repeat authorized status query"),
            m("boundary", "ctrl", "Reauthenticate / recheck client scope"))]),
        ("Unknown / cross-client reference", [
            r("ctrl", "boundary", "Scoped error; no unauthorized disclosure"),
            r("boundary", "merchant", "No evidence, secrets or Admin-only data")]),
        ("Truthful snapshot temporarily unavailable", [
            r("ctrl", "boundary", "Temporary retrieval error"),
            r("boundary", "merchant", "No invented success")]))]),
      ("Invalid / missing Merchant credential", [
          r("boundary", "merchant", "Client denial; no escrow query or data")]))
], ["Read only. Polling never authorizes a payment or participant action.",
    "Exclude private evidence, other merchants' transactions and Admin-only audit."])


def import_layout():
    path = SKILL / "scripts" / "seqlayout.py"
    spec = importlib.util.spec_from_file_location("drawio_sequence_layout", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    module.LIFELINE_W = 140
    module.HEADER_H = 80
    module.TOP = 100
    module.ROW = 80
    module.SELF_ROW = 100
    module.NOTE_ROW = 75
    module.MIN_SPACING = 220
    module.BOTTOM_PAD = 20
    module.LIFELINE = module.LIFELINE.replace("size=40;", "size=80;")
    # The official native viewer registers seqActorStick: its fixed circular
    # 30px head and 36px arms do not stretch with the 140px lifeline width.
    module.ACTOR = (module.ACTOR.replace("size=40;", "size=80;")
                    .replace("participant=umlActor;", "participant=seqActorStick;")
                    .replace("spacingBottom=-14;", "spacingBottom=-4;"))
    return module


def wrapped(text, width=28):
    return "<br>".join(textwrap.wrap(str(text), width=width, break_long_words=False, break_on_hyphens=False))


def flatten(steps, first, depth=0):
    flat, frames = [], []
    for step in steps:
        if "ref" in step:
            flat.append({"note": "__reference_marker__", "over": first, "_ref": step["ref"],
                         "_ref_label": step["label"]})
            continue
        if "fragment" not in step:
            msg = dict(step)
            if "label" in msg:
                msg["label"] = wrapped(msg["label"])
            if "note" in msg:
                msg["note"] = wrapped(msg["note"], 33)
            flat.append(msg)
            continue
        start = len(flat)
        branch_markers = []
        nested_frames = []
        for branch in step["branches"]:
            branch_markers.append({"index": len(flat), "guard": branch["guard"]})
            flat.append({"note": "__fragment_marker__", "over": first, "_marker": True})
            nested, childframes = flatten(branch["steps"], first, depth + 1)
            offset = len(flat)
            for frame in childframes:
                frame["start"] += offset
                frame["end"] += offset
                for marker in frame["branches"]:
                    marker["index"] += offset
            flat.extend(nested)
            nested_frames.extend(childframes)
        frames.append({"operator": step["fragment"], "start": start, "end": len(flat),
                       "depth": depth, "branches": branch_markers})
        frames.extend(nested_frames)
    return flat, frames


def cell(root, cid, value, style, x, y, width, height):
    elem = ET.SubElement(root, "mxCell", {"id": cid, "value": value, "style": style, "vertex": "1", "parent": "1"})
    ET.SubElement(elem, "mxGeometry", {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"})
    return elem


def row_positions(messages, layout):
    y = layout.TOP + layout.HEADER_H + 50
    positions = []
    for msg in messages:
        positions.append(y)
        y += layout.NOTE_ROW if "note" in msg else layout.SELF_ROW if msg.get("from") == msg.get("to") else layout.ROW
    return positions, y


def style_append(elem, additions):
    elem.set("style", elem.get("style", "") + additions)


def render_xml(model, title, source_info, layout):
    # Use the longest visible header line for geometry estimation, then layer
    # the stereotype text onto the native lifeline. HTML markup is never
    # mistaken for visible label width by the skill engine.
    richparts = [{**entry, "label": entry["label"].replace("\n", "<br>")} for entry in model["participants"]]
    parts = [{**entry, "label": entry["id"]} for entry in model["participants"]]
    flat, frames = flatten(model["steps"], parts[0]["id"])
    spec = {"title": f"SD {model['id']} - {title}", "participants": parts, "messages": flat}
    # Required skill engine owns lifeline / activation / arrow geometry.
    doc = ET.fromstring(layout.layout(spec))
    doc.set("host", "app.diagrams.net")
    doc.set("version", "26.0.0")
    diagram = doc.find("diagram")
    diagram.set("id", f"EPS-SD-{model['id']}")
    graph = diagram.find("mxGraphModel")
    graph.set("background", "#ffffff")
    root = graph.find("root")
    cells = {item.get("id"): item for item in root.findall("mxCell")}
    positions, end_y = row_positions(flat, layout)
    lifelines = [cells[entry["id"]] for entry in parts]
    right = max(float(item.find("mxGeometry").get("x")) + float(item.find("mxGeometry").get("width")) for item in lifelines)
    page_w = int(right + 60)
    for item in root.findall("mxCell"):
        if item.get("id") in ("0", "1"):
            continue
        style_append(item, "fontFamily=Helvetica;fontSize=14;fontColor=#243447;")
        if item.get("edge") == "1":
            # mxGraph otherwise infers a tiny edge-label box (46px in the
            # native DOM). Explicit model-unit width preserves readable lines.
            style_append(item, "whiteSpace=wrap;labelWidth=210;labelBackgroundColor=#ffffff;endSize=8;spacing=2;")
        if item.get("id", "").startswith("act"):
            style_append(item, "fillColor=#ffffff;strokeColor=#6c8ebf;")
    for entry in richparts:
        item = cells[entry["id"]]
        item.set("value", entry["label"])
        if entry["role"] in ("boundary", "control"):
            style_append(item, "fillColor=#dae8fc;strokeColor=#6c8ebf;")
        else:
            style_append(item, "fillColor=#f5f5f5;strokeColor=#666666;")
    # Add only native UML combined fragments; reserved rows keep guard labels
    # well clear of the next message. Frames remain behind lifelines/messages.
    for ix, frame in enumerate(frames):
        depth = frame["depth"]
        fx = 18 + depth * 10
        fy = positions[frame["start"]] - 35
        fend = positions[frame["end"]] if frame["end"] < len(positions) else end_y
        fw = right + 25 - fx - depth * 10
        fheight = fend - 30 - fy
        fcell = cell(root, f"fragment_{ix}", frame["operator"],
                     "shape=umlFrame;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#8b939e;"
                     "fontFamily=Helvetica;fontSize=14;align=left;verticalAlign=top;spacingLeft=6;spacingTop=2;"
                     "pointerEvents=0;container=0;", fx, fy, fw, fheight)
        root.remove(fcell)
        root.insert(2 + ix, fcell)
        for j, branch in enumerate(frame["branches"]):
            by = positions[branch["index"]]
            if j:
                separator = ET.SubElement(root, "mxCell", {"id": f"fragment_{ix}_separator_{j}",
                    "style": "endArrow=none;dashed=1;strokeColor=#aeb6bf;html=1;", "edge": "1", "parent": "1"})
                geom = ET.SubElement(separator, "mxGeometry", {"relative": "1", "as": "geometry"})
                ET.SubElement(geom, "mxPoint", {"x": str(fx), "y": str(by - 35), "as": "sourcePoint"})
                ET.SubElement(geom, "mxPoint", {"x": str(fx + fw), "y": str(by - 35), "as": "targetPoint"})
            cell(root, f"fragment_{ix}_guard_{j}", "[" + wrapped(branch["guard"], 75) + "]",
                 "text;html=1;whiteSpace=wrap;fillColor=#ffffff;strokeColor=none;align=left;verticalAlign=middle;"
                 "fontFamily=Helvetica;fontSize=14;fontColor=#40556b;spacingLeft=4;",
                 fx + 65, by - 20, fw - 85, 36)
    for i, message in enumerate(flat):
        if message.get("_marker"):
            root.remove(cells[f"note{i}"])
        elif message.get("_ref"):
            root.remove(cells[f"note{i}"])
            ry = positions[i] - 25
            frame = cell(root, f"reference_{i}", "ref",
                "shape=umlFrame;html=1;whiteSpace=wrap;fillColor=#ffffff;strokeColor=#6c8ebf;"
                "fontFamily=Helvetica;fontSize=14;align=left;verticalAlign=top;spacingLeft=6;spacingTop=2;",
                45, ry, right - 45, 60)
            frame.set("data-ref", message["_ref"])
            cell(root, f"reference_{i}_label", f"SD {message['_ref']} — " + wrapped(message["_ref_label"], 75),
                "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=center;verticalAlign=middle;"
                "fontFamily=Helvetica;fontSize=14;fontColor=#243447;",
                110, ry + 15, right - 135, 40)
    cell(root, "page_title", f"SD {model['id']} — {title}",
         "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=left;verticalAlign=middle;"
         "fontFamily=Helvetica;fontSize=16;fontStyle=1;fontColor=#243447;", 30, 10, page_w - 60, 42)
    subtitle = "EPS academic MVP | simulated VND | analysis-level interactions | time flows downward"
    if model.get("entry_guard"):
        subtitle = f"Continuation of SD {model.get('logical_id', model['id'])} | Entry: {model['entry_guard']}"
    cell(root, "page_subtitle", wrapped(subtitle, max(90, int((page_w - 60) / 6.5))),
         "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=left;fontFamily=Helvetica;fontSize=12;fontColor=#666666;",
         30, 58, page_w - 60, 30)
    footer_y = end_y + 30
    # Put the complete business constraints on the logical overview once.
    # Continuations keep them in the manifest and explicitly point to that
    # overview, leaving room for 8–10 readable messages on an A4-sized figure.
    is_main = model["id"] == model.get("logical_id", model["id"])
    if is_main:
        text = " ".join(model["notes"])
        cell(root, "business_constraints", wrapped(text, max(70, int((page_w - 130) / 6.3))),
             "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;align=left;"
             "fontFamily=Helvetica;fontSize=12;fontColor=#4d4630;spacingLeft=12;spacingRight=14;",
             30, footer_y, page_w - 90, 60)
        footer_y += 68
    else:
        cell(root, "context_reference", f"Context and business constraints: SD {model.get('logical_id', model['id'])}. This view is one complete guarded continuation.",
             "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=left;"
             "fontFamily=Helvetica;fontSize=12;fontColor=#666666;", 30, footer_y, page_w - 90, 30)
        footer_y += 36
    # The notes create a third semantic color; state its role together with the
    # blue EPS collaborators and gray actors/entities/external mocks.
    legend = "Blue: EPS boundary/control. Gray: actor/entity/external mock." + (" Yellow: business constraint." if is_main else "")
    cell(root, "legend_colors", legend,
         "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=left;"
         "fontFamily=Helvetica;fontSize=11;fontColor=#666666;", 30, footer_y, page_w - 90, 24)
    cell(root, "legend_arrows", "Solid filled arrow = request; dashed open arrow = async event or gray return. Frames show guarded alternatives/options.",
         "text;html=1;whiteSpace=wrap;fillColor=none;strokeColor=none;align=left;"
         "fontFamily=Helvetica;fontSize=11;fontColor=#666666;", 30, footer_y + 25, page_w - 90, 28)
    footer_y += 56
    graph.set("pageWidth", str(page_w))
    graph.set("pageHeight", str(footer_y + 20))
    graph.set("dx", str(page_w))
    graph.set("dy", str(footer_y + 20))
    # Semantic provenance is embedded in the editable artifact, not a claim
    # that any implementation or mock provider has already been tested.
    graph.set("data-model-id", model["id"])
    graph.set("data-source", source_info)
    ids = [item.get("id") for item in root.findall("mxCell")]
    assert len(ids) == len(set(ids)), f"duplicate IDs in {model['id']}"
    assert len(parts) <= 7
    for item in root.findall("mxCell"):
        if item.get("edge") == "1":
            assert item.find("mxGeometry") is not None
    spec["participants"] = richparts
    return ET.tostring(doc, encoding="unicode"), spec, frames, page_w, footer_y + 20


def used_participants(steps):
    used = set()
    for step in steps:
        if "fragment" in step:
            for branch in step["branches"]:
                used |= used_participants(branch["steps"])
        elif "from" in step:
            used |= {step["from"], step["to"]}
        elif "over" in step:
            used.add(step["over"])
    return used


def prune_participants(model):
    used = used_participants(model["steps"])
    if used:
        model["participants"] = [entry for entry in model["participants"] if entry["id"] in used]


def candidates(steps):
    found = []
    for step in steps:
        if "fragment" not in step or step["fragment"] not in ("alt", "opt"):
            continue
        for branch in step["branches"]:
            flat, _ = flatten(branch["steps"], "placeholder")
            message_count = sum("from" in message for message in flat)
            if message_count >= 3:
                found.append((len(flat), branch))
            found.extend(candidates(branch["steps"]))
    return found


def module_suffix(logical_id, guard):
    guard_lower = guard.lower()
    if logical_id == "U1":
        return "enrollment" if "valid input" in guard_lower else "activation"
    if logical_id == "U2":
        return "mfa"
    if logical_id == "U4":
        return "tracking"
    if logical_id == "U8":
        return "accept_refund" if "accept" in guard_lower else "reject_refund"
    if logical_id == "B3":
        return "funding"
    if logical_id == "B4":
        return "authorize_release"
    if logical_id == "A1":
        return "resolution"
    if logical_id == "A2":
        return "publish_policy"
    if logical_id == "A5":
        if "admin" in guard_lower and "attempt" in guard_lower:
            return "reconciliation"
        if "payout failed" in guard_lower:
            return "retry"
        if "succeeded" in guard_lower:
            return "confirmed_result"
        return "status_handling"
    if logical_id == "P1":
        return "confirmed_receipt" if "succeeded" in guard_lower else "failed_funding" if "failed" in guard_lower else "result_handling"
    if logical_id.endswith(".API"):
        return "authorized_request"
    return "authorized_flow"


def extract_dispatcher(model, logical, position, fragment, queue):
    part_id = f"{logical}_outcomes"
    serial = 2
    while part_id in MODELS:
        part_id = f"{logical}_outcomes_{serial}"
        serial += 1
    MODELS[part_id] = {"id": part_id, "logical_id": logical,
        "participants": list(model["participants"]), "steps": [fragment],
        "notes": list(model["notes"]),
        "entry_guard": "The preceding intake and authorization checks have completed",
        "module_title": "Guarded outcomes and permitted next actions"}
    queue.append(part_id)
    model["steps"][position] = ref(part_id, "Guarded outcomes; apply exactly the matching branch")
    prune_participants(model)


def modularize(layout, sources):
    """Factor guarded business paths, never crop images or slice arbitrary rows."""
    # A1 has a natural boundary between inspecting the review set and submitting
    # a reasoned final decision; do not split its ten-message linear prefix at
    # an arbitrary row merely to meet a figure-size target.
    review = MODELS["A1"]
    decision_id = "A1_decision"
    MODELS[decision_id] = {"id": decision_id, "logical_id": "A1",
        "participants": list(review["participants"]), "steps": review["steps"][7:],
        "notes": list(review["notes"]),
        "entry_guard": "Authorized Admin has inspected the latest evidence revision",
        "module_title": "Submit and commit final dispute decision"}
    review["steps"] = review["steps"][:7] + [ref(decision_id, "Submit reasoned final decision after reviewing evidence")]
    queue = list(MODELS)
    cursor = 0
    while cursor < len(queue):
        uid = queue[cursor]
        model = MODELS[uid]
        logical = model.get("logical_id", uid)
        model["logical_id"] = logical
        prune_participants(model)
        base_title = sources[logical]["name"]
        title = base_title + (" — " + model["module_title"] if model.get("module_title") else "")
        while True:
            _, _, _, width, height = render_xml(model, title, "current-use-case-content", layout)
            if width <= 1400 and height <= 1500:
                break
            # Keep intake and outcome dispatch as natural modules before
            # fragmenting individual tiny branches merely to fit the page.
            preferred = [(i, step) for i, step in enumerate(model["steps"])
                         if i >= 2 and step.get("fragment") == "alt" and len(step["branches"]) >= 3]
            if preferred:
                position, fragment = max(preferred, key=lambda entry: len(entry[1]["branches"]))
                extract_dispatcher(model, logical, position, fragment, queue)
                continue
            options = candidates(model["steps"])
            if not options:
                # Extract a whole result/decision dispatcher when its common
                # intake plus several tiny branches is the source of height.
                # This is a complete semantic fragment, never an image slice.
                fragment_positions = [(i, step) for i, step in enumerate(model["steps"])
                                      if "fragment" in step and step["fragment"] == "alt"]
                if not fragment_positions or len(model["steps"]) == 1:
                    raise RuntimeError(f"No natural business module remaining for oversized view {uid}: {width}x{height}")
                position, fragment = max(fragment_positions, key=lambda entry: len(entry[1]["branches"]))
                extract_dispatcher(model, logical, position, fragment, queue)
                continue
            _, branch = max(options, key=lambda entry: entry[0])
            suffix = module_suffix(logical, branch["guard"])
            part_id = f"{logical}_{suffix}"
            serial = 2
            while part_id in MODELS:
                part_id = f"{logical}_{suffix}_{serial}"
                serial += 1
            part = {"id": part_id, "logical_id": logical, "participants": list(model["participants"]),
                    "steps": branch["steps"], "notes": list(model["notes"]),
                    "entry_guard": branch["guard"], "module_title": branch["guard"]}
            MODELS[part_id] = part
            queue.append(part_id)
            branch["steps"] = [ref(part_id, branch["guard"])]
            prune_participants(model)
        cursor += 1


def main():
    shared = json.loads((HERE / "content_user_buyer.json").read_text(encoding="utf-8-sig"))["use_cases"]
    other = json.loads((HERE / "content_seller_admin_payment.json").read_text(encoding="utf-8-sig"))
    source = {uc["id"]: uc for uc in shared + other}
    assert len(source) == 22
    source["B1.API"] = {**source["B1"], "id": "B1.API", "name": "Create Escrow — Merchant API Variant"}
    source["U4.API"] = {**source["U4"], "id": "U4.API", "name": "View/Track Escrows — Merchant API Variant"}
    assert set(source).issubset(MODELS)
    layout = import_layout()
    modularize(layout, source)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for uid, model in MODELS.items():
        logical = model.get("logical_id", uid)
        uc = source[logical]
        title = uc["name"] + (" — " + model["module_title"] if model.get("module_title") else "")
        source_info = "content_user_buyer.json" if logical.startswith(("U", "B")) else "content_seller_admin_payment.json"
        xml, spec, frames, width, height = render_xml(model, title, source_info, layout)
        name = f"SD_{uid}.drawio"
        (OUTPUT / name).write_text(xml, encoding="utf-8")
        manifest.append({"id": uid, "logical_id": logical, "is_main": uid == logical,
                         "title": title, "group": uc["group"],
                         "filename": f"diagrams/sequence/{name}", "source": source_info,
                         "source_requirement_ids": uc.get("source_requirement_ids", uc.get("requirements", [])),
                         "participants": len(spec["participants"]), "messages": sum("note" not in x for x in spec["messages"]),
                         "page_width": width, "page_height": height,
                         "spec": spec, "fragments": frames, "business_notes": model["notes"],
                         "references": [message["_ref"] for message in spec["messages"] if message.get("_ref")],
                         "entry_guard": model.get("entry_guard", "")})
    logical_diagrams = [{"logical_id": uid, "title": uc["name"], "default_main": f"diagrams/sequence/SD_{uid}.drawio",
                         "parts": [{"id": view["id"], "title": view["title"], "filename": view["filename"]}
                                   for view in manifest if view["logical_id"] == uid and not view["is_main"]]}
                        for uid, uc in source.items()]
    (HERE / "sequence_models.json").write_text(json.dumps({
        "schema_version": "1.0", "language": "en", "creation": "Fresh builder output; the active sequence set also contains selected native edits, which this builder will not overwrite.",
        "layout_engine": str(SKILL / "scripts" / "seqlayout.py"),
        "count": len(logical_diagrams), "view_count": len(manifest), "logical_diagrams": logical_diagrams,
        "diagrams": manifest}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(logical_diagrams)} logical sequences as {len(manifest)} fresh native UML views and sequence_models.json")
    print(f"Participants: {min(x['participants'] for x in manifest)}–{max(x['participants'] for x in manifest)}; messages: {sum(x['messages'] for x in manifest)}")


if __name__ == "__main__":
    raise SystemExit(
        "Refusing to regenerate active sequence XML: the active set includes "
        "reviewed native edits. Run this fresh builder only in a clean scratch "
        "copy of the project; use analysis/promote_sequence_merge.py for the "
        "guarded one-time B3 promotion."
    )
