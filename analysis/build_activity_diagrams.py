"""Fresh EPS UML activity models, authored from the approved MVP/use-case specs.

No previous diagram is read. Layout is deterministic, lane-aware and orthogonal.
Graphviz is unavailable in this environment, so an obstacle-aware grid router is
used after deterministic row placement. Native draw.io cells remain editable.
"""
from __future__ import annotations

import heapq
import json
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
OUT = BASE / "diagrams" / "activity"
FONT = "fontFamily=Helvetica;fontSize=12;fontColor=#222222;"
NODE_FONT = FONT.replace("fontSize=12", "fontSize=14")
PALETTE = {"action": ("#dae8fc", "#6c8ebf"),
           "decision": ("#fff2cc", "#d6b656"),
           "exception": ("#f5f5f5", "#666666")}


def N(key, label, lane, row, kind="action", col=0):
    return dict(id=key, label=label, lane=lane, row=row, kind=kind, col=col)


def E(a, b, guard=""):
    return dict(source=a, target=b, guard=guard)


def model(uc, actor, nodes, edges, notes, provider=None):
    return dict(uc=uc, actor=actor, provider=provider, nodes=nodes, edges=edges,
                semantic_notes=notes)


def graphs():
    g = []
    g.append(model("U1", "Guest", [
        N("start", "", 0, 0, "initial"), N("submit", "Submit ordinary-account registration", 0, 1),
        N("valid", "Valid fields, unique login, ordinary role?", 1, 2, "decision"),
        N("invalid", "Reject invalid/duplicate input; never grant Admin or Merchant", 1, 2, "exception", 1),
        N("invalid_end", "", 1, 3, "final", 1),
        N("enroll", "Start MFA enrollment; account not usable yet", 1, 3),
        N("challenge", "Complete MFA enrollment challenge", 0, 4),
        N("mfa", "Valid current MFA enrollment proof?", 1, 5, "decision"),
        N("inactive", "Invalid/expired/abandoned: keep inactive; restart enrollment", 1, 5, "exception", 1),
        N("inactive_end", "", 1, 6, "final", 1),
        N("activate", "Activate one ordinary account; audit; direct to U2 login", 1, 6),
        N("end", "", 1, 7, "final")],
        [E("start", "submit"), E("submit", "valid"), E("valid", "invalid", "[no]"), E("invalid", "invalid_end"),
         E("valid", "enroll", "[yes]"), E("enroll", "challenge"), E("challenge", "mfa"), E("mfa", "inactive", "[no]"),
         E("inactive", "inactive_end"), E("mfa", "activate", "[yes]"), E("activate", "end")],
        ["MFA enrollment precedes account usability; login is separate.", "Concurrent same-identifier registrations activate at most one account."]))
    g.append(model("U2", "Buyer / Seller / Admin", [
        N("start", "", 0, 0, "initial"), N("credentials", "Submit human login credentials", 0, 1),
        N("credential_valid", "Active account and valid primary credential?", 1, 2, "decision"),
        N("deny_primary", "Generic login failure; audit; no authenticated session", 1, 2, "exception", 1),
        N("deny_primary_end", "", 1, 3, "final", 1), N("issue", "Issue short-lived MFA challenge; protected actions blocked", 1, 3),
        N("response", "Submit enrolled MFA response", 0, 4), N("mfa_valid", "Current unused MFA proof and account still active?", 1, 5, "decision"),
        N("deny_mfa", "Reject invalid/expired/replayed proof; require valid login", 1, 5, "exception", 1),
        N("deny_mfa_end", "", 1, 6, "final", 1), N("session", "Create role-scoped human session; record safe audit event", 1, 6),
        N("end", "", 1, 7, "final")],
        [E("start", "credentials"), E("credentials", "credential_valid"), E("credential_valid", "deny_primary", "[no]"),
         E("deny_primary", "deny_primary_end"), E("credential_valid", "issue", "[yes]"), E("issue", "response"),
         E("response", "mfa_valid"), E("mfa_valid", "deny_mfa", "[no]"), E("deny_mfa", "deny_mfa_end"),
         E("mfa_valid", "session", "[yes]"), E("session", "end")],
        ["Pre-provisioned Admin only; no role elevation at login.", "Merchant client authentication is separate and cannot replace human MFA."]))
    g.append(model("U3", "Buyer / Seller / Admin", [
        N("start", "", 0, 0, "initial"), N("logout", "Select Logout", 0, 1),
        N("revoke", "Invalidate current server session; clear local session", 1, 2),
        N("confirmed", "Revocation confirmed or session already invalid?", 1, 3, "decision"),
        N("done", "Return to public login; require fresh MFA login", 1, 4),
        N("unconfirmed", "Clear local access; report unconfirmed revocation; retry when connected", 1, 4, "exception", 1),
        N("end", "", 1, 5, "final"), N("unconfirmed_end", "", 1, 5, "final", 1)],
        [E("start", "logout"), E("logout", "revoke"), E("revoke", "confirmed"), E("confirmed", "done", "[yes]"),
         E("confirmed", "unconfirmed", "[no]"), E("done", "end"), E("unconfirmed", "unconfirmed_end")],
        ["Logout is idempotent for an expired/revoked session.", "Durably accepted financial operations continue independently of the human session."]))
    g.append(model("U4", "Buyer / Seller / Merchant", [
        N("start", "", 0, 0, "initial"), N("request", "Request list/detail; Merchant uses U4.API client scope", 0, 1),
        N("scope", "Authenticated and within participant/client scope?", 1, 2, "decision"),
        N("deny", "Deny without disclosing unauthorized escrow details", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("read", "Read consistent terms, state, attempts and policy snapshot", 1, 3),
        N("available", "Truthful snapshot available?", 1, 4, "decision"),
        N("unavailable", "Report retrieval unavailable; invent no status", 1, 4, "exception", 1), N("unavailable_end", "", 1, 5, "final", 1),
        N("display", "Show authorized snapshot or empty list; pending stays pending", 1, 5), N("end", "", 1, 6, "final")],
        [E("start", "request"), E("request", "scope"), E("scope", "deny", "[no]"), E("deny", "deny_end"), E("scope", "read", "[yes]"),
         E("read", "available"), E("available", "unavailable", "[no]"), E("unavailable", "unavailable_end"),
         E("available", "display", "[yes]"), E("display", "end")],
        ["Read-only; later mutations revalidate current state.", "Merchant sees own originating-client status only, excluding private evidence and Admin audit."]))
    g.append(model("U5", "Buyer / Seller", [
        N("start", "", 0, 0, "initial"), N("reason", "Submit dispute reason and optional initial evidence", 0, 1),
        N("eligible", "Participant; held funds; no prior dispute or payout intent?", 1, 2, "decision"),
        N("deny", "Reject invalid/stale request; duplicate returns existing dispute", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("commit", "Atomically set dispute OPEN; invalidate PENDING refund proposal", 1, 3),
        N("queue", "Audit; expose dispute/evidence to parties and Admin queue; funds held", 1, 4),
        N("end", "", 1, 5, "final")],
        [E("start", "reason"), E("reason", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "commit", "[yes]"), E("commit", "queue"), E("queue", "end")],
        ["The eligibility check and OPEN transition are one atomic operation; first valid transition wins.", "Only one dispute per escrow. No dispute during FUNDING_PENDING or after payout reservation."]))
    g.append(model("U6", "Buyer / Seller", [
        N("start", "", 0, 0, "initial"), N("submit", "Submit explanation / permitted evidence for own dispute", 0, 1),
        N("valid", "Participant; valid evidence; dispute still OPEN?", 1, 2, "decision"),
        N("deny", "Reject invalid upload or closed evidence window; no partial receipt", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("append", "Atomically append attributable evidence; repeated reference returns receipt", 1, 3),
        N("expose", "Audit; expose saved evidence to both parties and reviewing Admin", 1, 4), N("end", "", 1, 5, "final")],
        [E("start", "submit"), E("submit", "valid"), E("valid", "deny", "[no]"), E("deny", "deny_end"),
         E("valid", "append", "[yes]"), E("append", "expose"), E("expose", "end")],
        ["Evidence and Admin decision serialize: earlier evidence must be reviewed; earlier decision closes submission.", "Evidence is append-only and does not change terms or authorize money movement."]))
    g.append(model("U7", "Buyer / Seller", [
        N("start", "", 0, 0, "initial"), N("choose", "Choose Propose Full Refund or Withdraw own proposal", 0, 1),
        N("eligible", "Participant; HELD/DELIVERED; no dispute/payout; action valid?", 1, 2, "decision"),
        N("deny", "Reject stale, duplicate-conflicting or unauthorized request", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("choice", "Requested action?", 1, 3, "decision"),
        N("propose", "Create PENDING proposal; freeze seller delivery recording + buyer release", 1, 4),
        N("withdraw", "Atomically mark own PENDING proposal WITHDRAWN; retain history", 1, 4, "action", 1),
        N("end", "", 1, 5, "final"), N("withdraw_end", "", 1, 5, "final", 1)],
        [E("start", "choose"), E("choose", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "choice", "[yes]"), E("choice", "propose", "[propose]"), E("choice", "withdraw", "[withdraw]"),
         E("propose", "end"), E("withdraw", "withdraw_end")],
        ["Propose requires no other PENDING proposal; withdraw requires original proposer and still-PENDING status.", "A PENDING refund proposal freezes seller delivery recording and buyer release. Withdrawal or refusal restores otherwise eligible actions without rolling back saved delivery.", "Full amount to original funding source only; no payment instruction until counterparty approval.", "A competing approval/dispute wins atomically; dispute invalidates the proposal."]))
    g.append(model("U8", "Counterparty", [
        N("start", "", 0, 0, "initial"), N("respond", "Review full refund to original source; choose Accept / Reject", 0, 1),
        N("eligible", "Refund response eligible?", 1, 2, "decision"),
        N("deny", "Reject self-approval/stale request; duplicate returns prior result", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("choice", "Counterparty response?", 1, 3, "decision"),
        N("approve", "Atomically APPROVE proposal + reserve full Refund; REFUND_PENDING", 1, 4),
        N("reject", "Mark proposal REJECTED; audit; no payment instruction", 1, 4, "action", 1), N("reject_end", "", 1, 5, "final", 1),
        N("p3", "P3: refund through original funding provider/source", 2, 5),
        N("result", "Authoritative P3 result?", 1, 6, "decision"),
        N("success", "Expose REFUNDED only after confirmed success", 1, 7), N("end", "", 1, 8, "final"),
        N("pending", "Keep REFUND_PENDING; PENDING/UNKNOWN; A5 query only", 1, 7, "exception", 1), N("pending_end", "", 1, 8, "final", 1),
        N("failed", "Keep Refund reservation; attempt FAILED; A5 same-direction retry", 1, 9, "exception", 1), N("failed_end", "", 1, 10, "final", 1)],
        [E("start", "respond"), E("respond", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "choice", "[yes]"), E("choice", "approve", "[accept]"), E("choice", "reject", "[reject]"),
         E("reject", "reject_end"), E("approve", "p3"), E("p3", "result"), E("result", "success", "[SUCCEEDED]"),
         E("success", "end"), E("result", "pending", "[uncertain]"), E("pending", "pending_end"),
         E("result", "failed", "[FAILED]"), E("failed", "failed_end")],
        ["The response guard requires an authenticated participant other than the proposer, a PENDING proposal, confirmed held funds, and no dispute or accepted payout.", "Acceptance/withdrawal/dispute race: first valid transition wins.", "Refusal restores otherwise eligible seller delivery recording and buyer release without rolling back saved delivery.", "FAILED requires authoritative proof that no money moved; uncertainty does not permit retry.", "Approved Refund permanently locks direction; no later participant release/dispute."], "Original Bank / Gateway mock"))
    g.append(model("B1", "Buyer / Merchant variant", [
        N("start", "", 0, 0, "initial"), N("terms", "Submit parties, Goods/Services, positive VND amount, deliverable, criteria", 0, 1),
        N("valid", "Authenticated; authorized parties; distinct buyer/seller; valid terms?", 1, 2, "decision"),
        N("deny", "Reject invalid scope/terms or changed payload under same reference", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("duplicate", "Same operation reference already saved?", 1, 3, "decision"),
        N("existing", "Return original escrow; no duplicate agreement", 1, 4, "action", 1), N("existing_end", "", 1, 5, "final", 1),
        N("save", "Save AWAITING_SELLER + one policy snapshot; record originating client", 1, 4),
        N("show", "Audit; present seller review; return reference; funding unavailable", 1, 5), N("end", "", 1, 6, "final")],
        [E("start", "terms"), E("terms", "valid"), E("valid", "deny", "[no]"), E("deny", "deny_end"),
         E("valid", "duplicate", "[yes]"), E("duplicate", "existing", "[yes]"), E("existing", "existing_end"),
         E("duplicate", "save", "[no]"), E("save", "show"), E("show", "end")],
        ["B1.API uses separate client auth and provisioned seller binding; human B1 binds buyer to session.", "Policy snapshot is atomic. Seller accepts before funding; buyer accepts captured terms through B3.", "Lost response: query or repeat same reference; no money moves at creation."]))
    g.append(model("B2", "Buyer", [
        N("start", "", 0, 0, "initial"), N("cancel", "Request cancellation of own unfunded escrow", 0, 1),
        N("eligible", "AWAITING_SELLER/FUNDING and conclusively no collection?", 1, 2, "decision"),
        N("deny", "Reject held/unknown funding or stale state; keep pending uncertainty", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("commit", "Atomically set CANCELLED; disable seller response/funding; audit", 1, 3),
        N("show", "Return CANCELLED; repeated cancellation returns existing result", 1, 4), N("end", "", 1, 5, "final")],
        [E("start", "cancel"), E("cancel", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "commit", "[yes]"), E("commit", "show"), E("show", "end")],
        ["Authorization and eligibility rechecked atomically with cancellation.", "Funding reservation versus cancellation: first valid transition wins.", "Prior funding must never have started or be authoritative FAILED with no collection."]))
    g.append(model("B3", "Buyer", [
        N("start", "", 0, 0, "initial"), N("submit", "Accept captured terms; choose Bank/Gateway; submit full funding", 0, 1),
        N("eligible", "Funding eligible?", 1, 2, "decision"),
        N("deny", "Reject stale/unauthorized input; duplicate returns existing attempt", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("reserve", "Atomically reserve stable funding attempt; FUNDING_PENDING", 1, 3),
        N("provider", "Receive full-VND funding request; return/callback result", 2, 4),
        N("p1", "Apply P1: authenticate and correlate authoritative result", 1, 5),
        N("outcome", "Verified outcome?", 1, 6, "decision"),
        N("held", "HELD once; retain original provider/source; audit", 1, 7), N("end", "", 1, 8, "final"),
        N("failed", "Confirmed no collection: FAILED; AWAITING_FUNDING; retry/cancel eligible", 1, 7, "exception", 1), N("failed_end", "", 1, 8, "final", 1),
        N("pending", "Unknown/nonfinal/invalid result: FUNDING_PENDING; A5 query; no retry/cancel", 1, 9, "exception", 1), N("pending_end", "", 1, 10, "final", 1)],
        [E("start", "submit"), E("submit", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "reserve", "[yes]"), E("reserve", "provider"), E("provider", "p1"), E("p1", "outcome"),
         E("outcome", "held", "[SUCCEEDED]"), E("held", "end"), E("outcome", "failed", "[FAILED]"), E("failed", "failed_end"),
         E("outcome", "pending", "[uncertain]"), E("pending", "pending_end")],
        ["Funding eligibility requires the authenticated named buyer, seller-accepted captured terms, no held funds and no unresolved attempt; the full positive VND amount and selected mock method must match.", "Click/browser redirect never proves receipt; P1 applies a full held-money credit once.", "Funding and cancellation compete atomically; only one active funding attempt.", "Invalid callback is quarantined and cannot authorize HELD or a new attempt."], "Selected Bank / Gateway mock"))
    g.append(model("B4", "Buyer", [
        N("start", "", 0, 0, "initial"), N("accept", "Review completion/criteria; explicitly accept and request full release", 0, 1),
        N("eligible", "DELIVERED; evidence satisfied; no proposal/dispute/payout?", 1, 2, "decision"),
        N("deny", "Reject unauthorized/stale request; repeat returns existing operation", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("reserve", "Atomically save buyer acceptance + full Release intent; RELEASE_PENDING", 1, 3),
        N("p2", "P2: execute full seller payout through Bank mock", 2, 4),
        N("outcome", "Authoritative P2 outcome?", 1, 5, "decision"),
        N("released", "Expose RELEASED only after matching confirmed success", 1, 6), N("end", "", 1, 7, "final"),
        N("unknown", "Keep RELEASE_PENDING; PENDING/UNKNOWN; A5 query only", 1, 6, "exception", 1), N("unknown_end", "", 1, 7, "final", 1),
        N("failed", "No money moved: attempt FAILED; preserve Release; A5 retry only", 1, 8, "exception", 1), N("failed_end", "", 1, 9, "final", 1)],
        [E("start", "accept"), E("accept", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "reserve", "[yes]"), E("reserve", "p2"), E("p2", "outcome"), E("outcome", "released", "[SUCCEEDED]"),
         E("released", "end"), E("outcome", "unknown", "[uncertain]"), E("unknown", "unknown_end"),
         E("outcome", "failed", "[FAILED]"), E("failed", "failed_end")],
        ["Buyer identity and all conditions are rechecked in one atomic transition; first valid transition wins.", "No delivery-triggered/timed release. Reserved payout prohibits new dispute or opposite payout.", "P2 handles duplicate/late confirmations without a second payout."], "Partner Bank mock"))
    g.append(model("S1", "Seller", [
        N("start", "", 0, 0, "initial"), N("review", "Review terms/policy; choose Accept or Reject", 0, 1),
        N("eligible", "Named seller; current AWAITING_SELLER agreement?", 1, 2, "decision"),
        N("deny", "Reject stale/opposite response; repeated same response returns result", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("choice", "Seller response?", 1, 3, "decision"),
        N("accept", "Atomically freeze terms; AWAITING_FUNDING; audit", 1, 4),
        N("reject", "Atomically CANCELLED / SELLER_REJECTED; audit; no funding", 1, 4, "action", 1),
        N("end", "", 1, 5, "final"), N("reject_end", "", 1, 5, "final", 1)],
        [E("start", "review"), E("review", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "choice", "[yes]"), E("choice", "accept", "[accept]"), E("choice", "reject", "[reject]"),
         E("accept", "end"), E("reject", "reject_end")],
        ["Response and eligibility check commit atomically against buyer cancellation.", "Persistence uncertainty is checked through U4; no confirmed saved acceptance means no funding.", "Accepted terms require cancellation/recreation to change; no money moves here."]))
    g.append(model("S2", "Seller", [
        N("start", "", 0, 0, "initial"), N("submit", "Submit full goods delivery/service completion and required evidence", 0, 1),
        N("eligible", "Named seller; HELD; policy satisfied; no proposal/dispute/payout?", 1, 2, "decision"),
        N("deny", "Reject missing evidence/stale state; keep completion unchanged", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("save", "Atomically save completion; DELIVERED; full funds remain held", 1, 3),
        N("show", "Audit; expose to buyer; repeated reference returns existing record", 1, 4), N("end", "", 1, 5, "final")],
        [E("start", "submit"), E("submit", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "save", "[yes]"), E("save", "show"), E("show", "end")],
        ["Default Goods evidence optional; Services required; use the escrow's snapshot rather than latest policy.", "Eligibility and save serialize against refund/dispute/payout transitions.", "Completion never authorizes automatic release; buyer acceptance remains required."]))
    g.append(model("A1", "Admin", [
        N("start", "", 0, 0, "initial"), N("review", "Review terms, latest evidence and history; choose full outcome + rationale", 0, 1),
        N("eligible", "Authorized; OPEN dispute; held funds; rationale; no payout?", 1, 2, "decision"),
        N("deny", "Reject invalid/resolved/competing decision; duplicate returns saved result", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("latest", "Reviewed evidence revision still current?", 1, 3, "decision"),
        N("rereview", "Display new evidence; require fresh Admin review", 1, 3, "exception", 1),
        N("commit", "Atomically RESOLVED; close evidence; reserve full chosen outcome; audit", 1, 4),
        N("direction", "Saved decision?", 1, 5, "decision"),
        N("release", "Invoke P2; RELEASE_PENDING; Bank mock pays seller", 1, 6),
        N("refund", "Invoke P3; REFUND_PENDING; original provider/source", 1, 6, "action", 1),
        N("release_end", "", 1, 7, "final"), N("refund_end", "", 1, 7, "final", 1)],
        [E("start", "review"), E("review", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
         E("eligible", "latest", "[yes]"), E("latest", "rereview", "[no]"), E("rereview", "review", "[review]"),
         E("latest", "commit", "[yes]"), E("commit", "direction"), E("direction", "release", "[release]"),
         E("direction", "refund", "[refund]"), E("release", "release_end"), E("refund", "refund_end")],
        ["Decision and evidence revision recheck are atomic; first valid Admin decision wins.", "Decision is final but money status remains separate: P2/P3 confirm success; uncertainty is reconciled by A5.", "No appeal, new dispute, split outcome or opposite-direction retry after final decision."]))
    g.append(model("A2", "Admin", [
        N("start", "", 0, 0, "initial"), N("show", "Display current policy version; future escrows only", 1, 1),
        N("edit", "Set Goods/Services evidence-required booleans + reason", 0, 2),
        N("valid", "Authorized; supported values/reason; current version?", 1, 3, "decision"),
        N("deny", "Reject unsupported fields; stale version requires renewed review", 1, 3, "exception", 1), N("deny_end", "", 1, 4, "final", 1),
        N("changed", "Settings actually changed?", 1, 4, "decision"),
        N("nochange", "Return existing active version; no new version", 1, 5, "action", 1), N("nochange_end", "", 1, 6, "final", 1),
        N("publish", "Atomically publish new version + before/after audit", 1, 5),
        N("future", "Apply to future B1 only; existing policy snapshots unchanged", 1, 6), N("end", "", 1, 7, "final")],
        [E("start", "show"), E("show", "edit"), E("edit", "valid"), E("valid", "deny", "[no]"), E("deny", "deny_end"),
         E("valid", "changed", "[yes]"), E("changed", "nochange", "[no]"), E("nochange", "nochange_end"),
         E("changed", "publish", "[yes]"), E("publish", "future"), E("future", "end")],
        ["Only evidence-required booleans are configurable; no fees/currency/auto-release or split payout.", "Default Goods optional, Services required. Failed persistence leaves prior policy active."]))
    g.append(model("A3", "Admin", [
        N("start", "", 0, 0, "initial"), N("filter", "Choose creation-date interval / transaction type", 0, 1),
        N("valid", "Authorized analytics access and valid filters?", 1, 2, "decision"),
        N("deny", "Reject invalid/unauthorized query; disclose no analytics", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("aggregate", "Aggregate state counts, disputes, unresolved attempts and full VND totals", 1, 3),
        N("available", "Current aggregation available?", 1, 4, "decision"),
        N("unavailable", "Report unavailable; any older data explicitly timestamped", 1, 4, "exception", 1), N("unavailable_end", "", 1, 5, "final", 1),
        N("display", "Show timestamp + mock label; empty dataset gives zero totals", 1, 5), N("end", "", 1, 6, "final")],
        [E("start", "filter"), E("filter", "valid"), E("valid", "deny", "[no]"), E("deny", "deny_end"),
         E("valid", "aggregate", "[yes]"), E("aggregate", "available"), E("available", "unavailable", "[no]"),
         E("unavailable", "unavailable_end"), E("available", "display", "[yes]"), E("display", "end")],
        ["Read-only overview; not an audited financial statement.", "Unconfirmed funding is excluded from held money; reserved/failed-pending payouts remain held exactly once."]))
    g.append(model("A4", "Admin", [
        N("start", "", 0, 0, "initial"), N("query", "Choose reference/time interval and optional event type", 0, 1),
        N("valid", "Authorized audit access and valid filters?", 1, 2, "decision"),
        N("deny", "Deny invalid/unauthorized query; existing audit remains intact", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
        N("read", "Read chronological correlated events; never edit/delete", 1, 3),
        N("available", "Audit retrieval available?", 1, 4, "decision"),
        N("unavailable", "Report unavailable; fabricate no event or payment success", 1, 4, "exception", 1), N("unavailable_end", "", 1, 5, "final", 1),
        N("show", "Display safe event fields or empty result; mask private data; exclude secrets", 1, 5), N("end", "", 1, 6, "final")],
        [E("start", "query"), E("query", "valid"), E("valid", "deny", "[no]"), E("deny", "deny_end"), E("valid", "read", "[yes]"),
         E("read", "available"), E("available", "unavailable", "[no]"), E("unavailable", "unavailable_end"),
         E("available", "show", "[yes]"), E("show", "end")],
        ["No audit mutation is offered; attempted edit/delete cannot change history or money.", "No passwords, MFA codes, session/client/provider secrets or secret-bearing callback payloads."]))
    g.append(model("A5", "Admin", [
        N("start", "", 0, 0, "initial"), N("inspect", "Inspect unresolved/failed attempt and locked outcome", 0, 1),
        N("query", "Authorize Admin; query original attempt reference; no transfer", 1, 2),
        N("response", "Return authoritative same-attempt status or timeout", 2, 3),
        N("valid", "Authenticated matching result with no contradiction?", 1, 4, "decision"),
        N("invalid", "Keep unresolved; flag mismatch/contradiction; no manual success", 1, 4, "exception", 1), N("invalid_end", "", 1, 5, "final", 1),
        N("outcome", "Authoritative outcome?", 1, 5, "decision"),
        N("success", "Apply P1/P2/P3 success once; concurrent callback becomes duplicate", 1, 6), N("success_end", "", 1, 7, "final"),
        N("unknown", "Retain PENDING/UNKNOWN; reservation intact; disable Retry", 1, 6, "exception", 1), N("unknown_end", "", 1, 7, "final", 1),
        N("kind", "FAILED with no money moved: operation?", 1, 8, "decision"),
        N("funding", "Funding: AWAITING_FUNDING; only buyer may initiate B3 retry", 1, 8, "action", 1), N("funding_end", "", 1, 9, "final", 1),
        N("retry", "Explicitly request same-direction payout Retry", 0, 9),
        N("safe", "Proof saved; no active attempt; same amount/destination/direction?", 1, 10, "decision"),
        N("deny_retry", "Reject unsafe/changed retry; repeated click returns active attempt", 1, 10, "exception", 1), N("deny_retry_end", "", 1, 11, "final", 1),
        N("dispatch", "Atomically create one linked attempt; invoke P2/P3; audit", 1, 11), N("end", "", 1, 12, "final")],
        [E("start", "inspect"), E("inspect", "query"), E("query", "response"), E("response", "valid"),
         E("valid", "invalid", "[no]"), E("invalid", "invalid_end"), E("valid", "outcome", "[yes]"),
         E("outcome", "success", "[SUCCEEDED]"), E("success", "success_end"), E("outcome", "unknown", "[uncertain]"),
         E("unknown", "unknown_end"), E("outcome", "kind", "[FAILED]"), E("kind", "funding", "[funding]"),
         E("funding", "funding_end"), E("kind", "retry", "[payout]"), E("retry", "safe"), E("safe", "deny_retry", "[no]"),
         E("deny_retry", "deny_retry_end"), E("safe", "dispatch", "[yes]"), E("dispatch", "end")],
        ["Reconciliation queries never create money movement; only authoritative no-money-moved failure permits retry.", "A payout retry preserves reservation and direction; Admin cannot fund as buyer or mark success manually.", "Callback/query use the same atomic confirmation path; contradictory finals are quarantined."], "Responsible Bank / Gateway mock"))
    g.append(model("P1", "", [
        N("start", "", 2, 0, "initial"), N("receive", "Send callback / query result for stored Funding reference", 2, 1),
        N("valid", "Authenticated; reference/provider/operation/full VND match?", 1, 2, "decision"),
        N("invalid", "Quarantine invalid result; safe audit; money state unchanged", 1, 2, "exception", 1), N("invalid_end", "", 1, 3, "final", 1),
        N("prior", "Previously final or conflicting stored outcome?", 1, 4, "decision"),
        N("duplicate", "Matching duplicate: ack; contradiction: flag; never regress/credit twice", 1, 4, "exception", 1), N("duplicate_end", "", 1, 5, "final", 1),
        N("outcome", "Verified receipt outcome?", 1, 5, "decision"),
        N("held", "Atomically SUCCEEDED + HELD once; retain source/provider; audit", 1, 6),
        N("saved", "Result durably saved?", 1, 7, "decision"), N("end", "", 1, 8, "final"),
        N("failed", "No receipt: FAILED + AWAITING_FUNDING; buyer retry/cancel eligible", 1, 6, "exception", 1), N("failed_end", "", 1, 7, "final", 1),
        N("pending", "FUNDING_PENDING; PENDING/UNKNOWN; no new funding/cancel; A5 query", 1, 9, "exception", 1), N("pending_end", "", 1, 10, "final", 1)],
        [E("start", "receive"), E("receive", "valid"), E("valid", "invalid", "[no]"), E("invalid", "invalid_end"),
         E("valid", "prior", "[yes]"), E("prior", "duplicate", "[yes]"), E("duplicate", "duplicate_end"), E("prior", "outcome", "[no]"),
         E("outcome", "held", "[SUCCEEDED]"), E("held", "saved"), E("saved", "end", "[yes]"), E("saved", "pending", "[no]"),
         E("outcome", "failed", "[FAILED]"), E("failed", "failed_end"), E("outcome", "pending", "[uncertain]"), E("pending", "pending_end")],
        ["B3 already persisted the funding attempt; click/redirect is never proof of receipt.", "Late success on the same unresolved eligible attempt applies once; contradictory final results do not reopen a closed escrow.", "Failure transitions likewise commit atomically; unsaved outcomes remain unresolved and are queried by the same reference."], "Selected Bank / Gateway mock"))
    for uc, direction, terminal, provider in [
        ("P2", "Release", "RELEASED", "Partner Bank mock"),
        ("P3", "Refund", "REFUNDED", "Original Bank / Gateway mock")]:
        pending = "RELEASE_PENDING" if uc == "P2" else "REFUND_PENDING"
        destination = "agreed seller via Bank mock" if uc == "P2" else "original funding provider/source"
        g.append(model(uc, "", [
            N("start", "", 1, 0, "initial"), N("read", f"Read saved full {direction} authorization and reserved amount", 1, 1),
            N("eligible", "Matching authorization/reservation/destination; one eligible attempt?", 1, 2, "decision"),
            N("deny", "Reject missing/changed/opposite/concurrent instruction; no provider call", 1, 2, "exception", 1), N("deny_end", "", 1, 3, "final", 1),
            N("dispatch", f"Send stable full-VND {direction} instruction; keep {pending}", 1, 3),
            N("provider", f"Execute to {destination}; callback/query same reference", 2, 4),
            N("valid", "Authenticated matching result; amount/destination/reference valid?", 1, 5, "decision"),
            N("invalid", "Keep unresolved; flag mismatch/contradiction; A5 query same reference", 1, 5, "exception", 1), N("invalid_end", "", 1, 6, "final", 1),
            N("outcome", "Authoritative transfer result?", 1, 6, "decision"),
            N("success", f"Atomically SUCCEEDED + {terminal}; consume reservation once; audit", 1, 7), N("end", "", 1, 8, "final"),
            N("failed", f"No money moved: FAILED; keep {pending} and {direction} reservation", 1, 7, "exception", 1), N("failed_end", "", 1, 8, "final", 1),
            N("uncertain", f"Keep {pending}; PENDING/UNKNOWN; no retry/opposite payout; A5 query", 1, 9, "exception", 1), N("uncertain_end", "", 1, 10, "final", 1)],
            [E("start", "read"), E("read", "eligible"), E("eligible", "deny", "[no]"), E("deny", "deny_end"),
             E("eligible", "dispatch", "[yes]"), E("dispatch", "provider"), E("provider", "valid"), E("valid", "invalid", "[no]"),
             E("invalid", "invalid_end"), E("valid", "outcome", "[yes]"), E("outcome", "success", "[SUCCEEDED]"), E("success", "end"),
             E("outcome", "failed", "[FAILED]"), E("failed", "failed_end"), E("outcome", "uncertain", "[uncertain]"), E("uncertain", "uncertain_end")],
            [f"{direction} authorization is immutable; A5 retries only the same full outcome after authoritative no-money-moved failure.",
             "Duplicate/late matching success applies once; stale results cannot regress a terminal outcome; contradictory finals are flagged.",
             "Dispatch/result persistence failures remain unresolved under the same reference; no compensating second transfer.",
             "One escrow has one final money outcome, RELEASED or REFUNDED; never both."], provider))
    return shorten_activity_labels(g)


def shorten_activity_labels(items):
    """Keep topology/geometry; retain original detail in manifest notes/fields."""
    labels = {
      "U1": {
        "submit":"Submit ordinary-account details", "valid":"Valid ordinary registration?",
        "invalid":"Reject invalid / duplicate input;\nno privileged account", "enroll":"Start MFA enrollment;\naccount remains inactive",
        "challenge":"Complete MFA enrollment", "mfa":"Enrollment proof valid?",
        "inactive":"Keep inactive;\nrestart MFA enrollment", "activate":"Activate ordinary account;\naudit; direct to Login"},
      "U2": {
        "credentials":"Submit human login credentials", "credential_valid":"Credentials + account valid?",
        "deny_primary":"Deny login;\nno authenticated session", "issue":"Issue MFA challenge;\nkeep access blocked",
        "response":"Submit enrolled MFA proof", "mfa_valid":"MFA valid + account active?",
        "deny_mfa":"Reject invalid MFA;\nrequire a valid login", "session":"Create role-scoped session;\naudit safe login event"},
      "U3": {
        "logout":"Select Logout", "revoke":"Revoke server session;\nclear local access",
        "confirmed":"Revocation confirmed?", "done":"Return to Login;\nrequire fresh MFA",
        "unconfirmed":"Clear local access;\nrevocation unconfirmed;\nretry when connected"},
      "U4": {
        "request":"Request own escrow list / detail", "scope":"Caller + scope valid?",
        "deny":"Deny protected data access", "read":"Read authorized,\nconsistent escrow snapshot",
        "available":"Snapshot available?", "unavailable":"Report query unavailable;\ninvent no status",
        "display":"Show snapshot / empty list;\npending stays pending"},
      "U5": {
        "reason":"Submit dispute reason\nand optional proof", "eligible":"Dispute eligible?",
        "deny":"Reject invalid / stale request;\nreuse accepted dispute", "commit":"Open one dispute;\ninvalidate refund proposal",
        "queue":"Audit; expose to parties/Admin;\nkeep full funds held"},
      "U6": {
        "submit":"Submit explanation / proof\nfor own dispute", "valid":"Evidence submission eligible?",
        "deny":"Reject invalid / late evidence;\nno partial receipt", "append":"Append evidence once;\nrecord author and time",
        "expose":"Audit receipt;\nshare with parties/Admin"},
      "U7": {
        "choose":"Propose full refund\nor withdraw own proposal", "eligible":"Refund action eligible?",
        "deny":"Reject invalid / stale action;\nno duplicate proposal", "choice":"Propose or withdraw?",
        "propose":"Create PENDING proposal;\nfreeze seller delivery\nand buyer release",
        "withdraw":"Mark WITHDRAWN;\nretain history and delivery"},
      "U8": {
        "respond":"Review full refund;\naccept or reject", "eligible":"Refund response eligible?",
        "deny":"Reject self / stale response;\nreuse accepted result", "choice":"Accept or reject?",
        "approve":"Approve proposal;\nreserve full refund", "reject":"Reject proposal;\nno payout instruction",
        "p3":"Call P3:\nrefund original source", "result":"Authoritative refund result?",
        "success":"Show confirmed REFUNDED", "pending":"Keep REFUND_PENDING;\nA5 query only",
        "failed":"FAILED: no money moved;\nkeep refund lock;\nA5 retry only"},
      "B1": {
        "terms":"Enter parties, VND amount,\ndeliverable + criteria", "valid":"Creation request eligible?",
        "deny":"Reject invalid scope / terms\nor reference conflict", "duplicate":"Request already saved?",
        "existing":"Return existing escrow;\ncreate no duplicate", "save":"Save AWAITING_SELLER;\ncapture policy + client",
        "show":"Audit; invite seller review;\nreturn escrow reference"},
      "B2": {
        "cancel":"Request unfunded cancellation", "eligible":"Safe cancellation eligible?",
        "deny":"Reject stale / unknown funding;\nkeep money state", "commit":"Set CANCELLED atomically;\nblock funding; audit",
        "show":"Show saved cancellation;\nduplicates reuse result"},
      "B3": {
        "submit":"Accept terms; choose mock;\nfund the full amount", "eligible":"Funding eligible?",
        "deny":"Reject invalid funding;\nreuse existing attempt", "reserve":"Reserve one funding attempt;\nFUNDING_PENDING",
        "provider":"Receive funding instruction;\nreturn / callback result", "p1":"Apply P1:\nverify provider confirmation",
        "outcome":"Verified funding result?", "held":"Record HELD once;\nretain source; audit",
        "failed":"FAILED: no collection;\nAWAITING_FUNDING", "pending":"Keep FUNDING_PENDING;\nA5 query only;\nno retry / cancellation"},
      "B4": {
        "accept":"Accept seller completion;\nrequest full release", "eligible":"Buyer release eligible?",
        "deny":"Reject invalid release;\nreuse accepted operation", "reserve":"Save buyer acceptance;\nreserve full release",
        "p2":"Call P2:\nBank pays agreed seller", "outcome":"Authoritative release result?",
        "released":"Show confirmed RELEASED", "unknown":"Keep RELEASE_PENDING;\nA5 query only",
        "failed":"FAILED: no money moved;\nkeep release lock;\nA5 retry only"},
      "S1": {
        "review":"Review terms;\naccept or reject", "eligible":"Seller response eligible?",
        "deny":"Reject stale / opposite reply;\nreuse accepted result", "choice":"Accept or reject?",
        "accept":"Freeze accepted terms;\nAWAITING_FUNDING; audit", "reject":"CANCELLED: SELLER_REJECTED;\nblock funding; audit"},
      "S2": {
        "submit":"Submit full completion\nand required evidence", "eligible":"Seller completion eligible?",
        "deny":"Reject invalid / stale delivery;\nkeep completion unchanged", "save":"Save DELIVERED atomically;\nfull funds remain held",
        "show":"Audit; expose to buyer;\nduplicates reuse receipt"},
      "A1": {
        "review":"Review dispute + proof;\nchoose outcome + reason", "eligible":"Admin decision eligible?",
        "deny":"Reject invalid / stale decision;\nreuse accepted result", "latest":"Evidence revision current?",
        "rereview":"Show new evidence;\nrequire fresh review", "commit":"Save final decision;\nclose evidence; reserve funds",
        "direction":"Release or refund?", "release":"Call P2:\nfull seller release", "refund":"Call P3:\nrefund original source"},
      "A2": {
        "show":"Show current policy;\nfuture escrows only", "edit":"Set evidence flags;\nenter change reason",
        "valid":"Policy update eligible?", "deny":"Reject invalid / stale policy;\nrequire fresh review",
        "changed":"Any setting changed?", "nochange":"Keep current policy version",
        "publish":"Publish new policy version;\naudit before / after", "future":"Use for new escrows;\nkeep existing snapshots"},
      "A3": {
        "filter":"Choose date / type filters", "valid":"Query authorized + valid?",
        "deny":"Reject invalid / denied query;\ndisclose no analytics", "aggregate":"Aggregate recorded states\nand mock VND totals",
        "available":"Current results available?", "unavailable":"Report unavailable;\nlabel any older snapshot",
        "display":"Show time + mock label;\nempty set = zero totals"},
      "A4": {
        "query":"Choose reference, dates\nand event type", "valid":"Audit query eligible?",
        "deny":"Deny invalid / unauthorized query;\npreserve audit", "read":"Read ordered audit events;\nnever edit or delete",
        "available":"Audit results available?", "unavailable":"Report unavailable;\nfabricate no event",
        "show":"Show safe fields / no matches;\nmask data; omit secrets"},
      "A5": {
        "inspect":"Inspect attempt\nand locked outcome", "query":"Authorize Admin;\nquery original attempt",
        "response":"Return correlated status\nor timeout", "valid":"Provider result valid?",
        "invalid":"Keep unresolved; flag conflict;\nno manual success", "outcome":"Authoritative result?",
        "success":"Apply P1 / P2 / P3 once;\naudit outcome", "unknown":"Keep PENDING / UNKNOWN;\nretain lock; no retry",
        "kind":"Failed: funding or payout?", "funding":"AWAITING_FUNDING;\nbuyer alone retries B3",
        "retry":"Request approved payout retry", "safe":"Safe same-direction retry?",
        "deny_retry":"Reject unsafe retry;\nreuse active attempt", "dispatch":"Create linked attempt;\ncall P2 / P3; audit"},
      "P1": {
        "receive":"Send Funding result\nfor stored attempt", "valid":"Provider result matched?",
        "invalid":"Quarantine invalid result;\npreserve money; audit", "prior":"Stored result final / conflicting?",
        "duplicate":"Duplicate: acknowledge;\ncontradiction: flag;\nnever credit twice", "outcome":"Verified receipt result?",
        "held":"Commit HELD + SUCCEEDED;\nretain source; audit", "saved":"Result durably saved?",
        "failed":"FAILED: no receipt;\nAWAITING_FUNDING", "pending":"Keep FUNDING_PENDING;\nA5 query only;\nno funding / cancellation"},
      "P2": {
        "read":"Read saved Release intent\nand full reservation", "eligible":"Release execution eligible?",
        "deny":"Reject invalid instruction;\nno provider call", "dispatch":"Send full-VND Release;\nkeep RELEASE_PENDING",
        "provider":"Bank pays agreed seller;\nreturn correlated result", "valid":"Release result matched?",
        "invalid":"Keep unresolved;\nflag mismatch; A5 query", "outcome":"Authoritative release result?",
        "success":"Commit RELEASED once;\nconsume reservation; audit", "failed":"FAILED: no money moved;\nkeep RELEASE_PENDING lock",
        "uncertain":"Keep RELEASE_PENDING;\nA5 query only;\nno new money instruction"},
      "P3": {
        "read":"Read saved Refund intent\nand full reservation", "eligible":"Refund execution eligible?",
        "deny":"Reject invalid instruction;\nno provider call", "dispatch":"Send full-VND Refund;\nkeep REFUND_PENDING",
        "provider":"Return to original source;\nreturn correlated result", "valid":"Refund result matched?",
        "invalid":"Keep unresolved;\nflag mismatch; A5 query", "outcome":"Authoritative refund result?",
        "success":"Commit REFUNDED once;\nconsume reservation; audit", "failed":"FAILED: no money moved;\nkeep REFUND_PENDING lock",
        "uncertain":"Keep REFUND_PENDING;\nA5 query only;\nno new money instruction"}
    }
    for g in items:
        overrides=labels[g["uc"]]
        visible={n["id"] for n in g["nodes"] if n["kind"] in ("action","decision","exception")}
        assert set(overrides)==visible,(g["uc"],set(overrides)^visible)
        for n in g["nodes"]:
            if n["id"] not in overrides:
                continue
            n["detail"]=n["label"]
            n["label"]=overrides[n["id"]]
            assert len(n["label"].splitlines()) <= (2 if n["kind"]=="decision" else 3)
            if n["label"] != n["detail"]:
                g["semantic_notes"].append(f"{n['id']} — full condition/action: {n['detail']}")
    return items


def rect_for(node, lane_defs):
    lane = lane_defs[node["lane"]]
    center_x = lane["x"] + (160 if node["col"] == 0 else 470)
    kind = node["kind"]
    w, h = (20, 20) if kind == "initial" else ((40, 40) if kind == "final" else ((240, 100) if kind == "decision" else (240, 80)))
    y = 210 + node["row"] * 130 - h/2
    return dict(x=center_x-w/2, y=y, w=w, h=h)


def compress(points):
    out = []
    for p in points:
        if out and p == out[-1]:
            continue
        if len(out) >= 2 and ((out[-2][0] == out[-1][0] == p[0]) or (out[-2][1] == out[-1][1] == p[1])):
            out[-1] = p
        else:
            out.append(p)
    return out


def port(rect, side):
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
    return {"top": (x+w/2, y), "bottom": (x+w/2, y+h),
            "left": (x, y+h/2), "right": (x+w, y+h/2)}[side]


NORMAL = {"top": (0, -1), "bottom": (0, 1), "left": (-1, 0), "right": (1, 0)}
PIN = {"top": (.5, 0), "bottom": (.5, 1), "left": (0, .5), "right": (1, .5)}


def route(source, target, rects, width, height, used, uc):
    s, t = rects[source], rects[target]
    sc = (s["x"]+s["w"]/2, s["y"]+s["h"]/2)
    tc = (t["x"]+t["w"]/2, t["y"]+t["h"]/2)
    if uc == "A1" and source == "rereview" and target == "review":
        p, q = port(s, "right"), port(t, "top")
        return ("right", "top"), [p, (width-10,p[1]), (width-10,q[1]-30), (q[0],q[1]-30), q]
    if (uc == "P1" and source == "outcome" and target == "pending") or (uc in ("P2","P3") and source == "outcome" and target == "uncertain"):
        p, q = port(s, "bottom"), port(t, "right")
        corridor=t["x"]+t["w"]+30
        return ("bottom", "right"), [p,(p[0],p[1]+30),(corridor,p[1]+30),(corridor,q[1]),q]
    if source in ("outcome", "result") and tc[1]-sc[1] >= 300 and tc[0] > sc[0]:
        p, q = port(s, "right"), port(t, "right")
        corridor = t["x"]+t["w"]+30
        return ("right", "right"), [p,(corridor,p[1]),(corridor,q[1]),q]
    if abs(sc[1]-tc[1]) < 60:
        sides = ("right", "left") if sc[0] < tc[0] else ("left", "right")
    elif tc[1] > sc[1]:
        sides = ("bottom", "top")
    else:
        sides = ("left", "left") if sc[0] > tc[0] else ("right", "right")
    p, q = port(s, sides[0]), port(t, sides[1])
    ns, nt = NORMAL[sides[0]], NORMAL[sides[1]]
    # Half-grid circles are snapped only at routing stubs, preserving exact pins.
    a = (round((p[0]+ns[0]*30)/10)*10, round((p[1]+ns[1]*30)/10)*10)
    b = (round((q[0]+nt[0]*30)/10)*10, round((q[1]+nt[1]*30)/10)*10)
    blocked = set()
    for r in rects.values():
        for x in range(int((r["x"]-10)//10)*10, int((r["x"]+r["w"]+10)//10)*10+1, 10):
            for y in range(int((r["y"]-10)//10)*10, int((r["y"]+r["h"]+10)//10)*10+1, 10):
                if r["x"]-9 <= x <= r["x"]+r["w"]+9 and r["y"]-9 <= y <= r["y"]+r["h"]+9:
                    blocked.add((x, y))
    blocked.discard(a); blocked.discard(b)
    heap = [(0, 0, a[0], a[1], -1)]
    start = (a[0], a[1], -1)
    scores = {start: 0}
    parent = {}
    end = None
    while heap:
        _, cost, x, y, direction = heapq.heappop(heap)
        state = (x, y, direction)
        if cost != scores.get(state):
            continue
        if (x, y) == b:
            end = state
            break
        for d, (dx, dy) in enumerate(((10, 0), (0, 10), (-10, 0), (0, -10))):
            xx, yy = x+dx, y+dy
            if not (10 <= xx <= width-10 and 140 <= yy <= height-10) or (xx, yy) in blocked:
                continue
            move = 10 + (22 if direction != -1 and direction != d else 0)
            move += used.get((min(x, xx), min(y, yy), max(x, xx), max(y, yy)), 0) * 20
            nxt = (xx, yy, d); new = cost+move
            if new < scores.get(nxt, 10**20):
                scores[nxt] = new; parent[nxt] = state
                heapq.heappush(heap, (new+abs(xx-b[0])+abs(yy-b[1]), new, xx, yy, d))
    if end is None:
        raise RuntimeError(f"No route {source} -> {target}")
    pts = []
    while end != start:
        pts.append((end[0], end[1])); end = parent[end]
    pts.append(a); pts.reverse()
    for aa, bb in zip(pts, pts[1:]):
        segment = (min(aa[0],bb[0]), min(aa[1],bb[1]), max(aa[0],bb[0]), max(aa[1],bb[1]))
        used[segment] = used.get(segment, 0)+1
    # Include exact endpoint-normal stubs before compressed grid route.
    out = compress([p, (p[0]+ns[0]*30, p[1]+ns[1]*30), *pts,
                    (q[0]+nt[0]*30, q[1]+nt[1]*30), q])
    return sides, out


def add_cell(root, cid, value, style, parent, rect=None, **attrs):
    cell = ET.SubElement(root, "mxCell", {"id": cid, "value": value, "style": style, "parent": parent, **attrs})
    if rect:
        ET.SubElement(cell, "mxGeometry", {"x": str(rect["x"]), "y": str(rect["y"]),
                                             "width": str(rect["w"]), "height": str(rect["h"]), "as": "geometry"})
    return cell


def write_diagram(g, specs):
    uc = g["uc"]; prefix = f"AD-{uc}-"
    # EPS always owns two action columns; explicit provider lane is omitted when absent.
    lane_defs = {1: dict(x=330 if g["actor"] else 30, w=640, label="EPS")}
    if g["actor"]:
        lane_defs[0] = dict(x=30, w=300, label=g["actor"])
    if g["provider"]:
        lane_defs[2] = dict(x=lane_defs[1]["x"]+640, w=300, label=g["provider"])
    width = max(l["x"]+l["w"] for l in lane_defs.values())+30
    maxrow = max(n["row"] for n in g["nodes"])
    lane_height = 160 + maxrow*130 + 110 - 100
    footer_y = 100+lane_height+20
    height = footer_y+140
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "26.0.0", "type": "device"})
    diagram = ET.SubElement(mxfile, "diagram", {"id": f"AD-{uc}", "name": f"AD_{uc}"})
    graph = ET.SubElement(diagram, "mxGraphModel", {"dx": str(width), "dy": str(height), "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "0", "pageScale": "1", "pageWidth": str(width), "pageHeight": str(height), "math": "0", "shadow": "0", "background": "#ffffff"})
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"}); ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    title = f"{uc} — {specs[uc]['name']}"
    add_cell(root, prefix+"title", title, "text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontStyle=1;fontFamily=Helvetica;fontSize=16;fontColor=#222222;", "1", dict(x=30,y=20,w=width-60,h=40), vertex="1")
    add_cell(root, prefix+"subtitle", "UML activity • Academic mock escrow • VND • One full outcome", "text;html=1;align=left;"+FONT, "1", dict(x=30,y=60,w=width-60,h=20), vertex="1")
    for num, lane in sorted(lane_defs.items(), key=lambda item:item[1]["x"]):
        add_cell(root, prefix+f"lane-{num}", lane["label"], "swimlane;html=1;whiteSpace=wrap;startSize=40;horizontal=1;container=1;collapsible=0;recursiveResize=0;pointerEvents=0;fillColor=#ffffff;swimlaneFillColor=#ffffff;strokeColor=#b3b3b3;fontFamily=Helvetica;fontSize=14;fontStyle=1;fontColor=#222222;", "1", dict(x=lane["x"],y=100,w=lane["w"],h=lane_height), vertex="1")
    rects = {n["id"]: rect_for(n, lane_defs) for n in g["nodes"]}
    for n in g["nodes"]:
        r = rects[n["id"]]; lane = lane_defs[n["lane"]]
        rel = dict(x=r["x"]-lane["x"], y=r["y"]-100,w=r["w"],h=r["h"])
        if n["kind"] == "initial":
            style = "ellipse;html=1;aspect=fixed;fillColor=#222222;strokeColor=#222222;"+FONT
        elif n["kind"] == "final":
            style = "ellipse;html=1;aspect=fixed;fillColor=#ffffff;strokeColor=#222222;strokeWidth=2;"+FONT
        else:
            fill, stroke = PALETTE[n["kind"]]
            shape = "rhombus;" if n["kind"] == "decision" else "rounded=1;arcSize=15;"
            style = shape+"whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacing=6;fillColor="+fill+";strokeColor="+stroke+";"+NODE_FONT
        add_cell(root, prefix+n["id"], n["label"], style, prefix+f"lane-{n['lane']}", rel, vertex="1")
        if n["kind"] == "final":
            add_cell(root, prefix+n["id"]+"-core", "", "ellipse;html=1;aspect=fixed;fillColor=#222222;strokeColor=#222222;", prefix+n["id"], dict(x=10,y=10,w=20,h=20), vertex="1")
    used = {}; routes = []
    for index, edge in enumerate(g["edges"]):
        sides, points = route(edge["source"], edge["target"], rects, width, 100+lane_height, used, uc)
        exitx, exity = PIN[sides[0]]; entryx, entryy = PIN[sides[1]]
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;endSize=8;strokeColor=#444444;labelBackgroundColor=#ffffff;exitX={exitx};exitY={exity};exitDx=0;exitDy=0;entryX={entryx};entryY={entryy};entryDx=0;entryDy=0;"+FONT
        cell = add_cell(root, prefix+f"edge-{index+1:02d}", edge["guard"], style, "1", edge="1", source=prefix+edge["source"], target=prefix+edge["target"])
        geom = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry", "x": "-0.4", "y": "0"})
        waypoints = ET.SubElement(geom, "Array", {"as": "points"})
        for x,y in points[1:-1]:
            ET.SubElement(waypoints, "mxPoint", {"x": str(x), "y": str(y)})
        ET.SubElement(geom, "mxPoint", {"x": "0", "y": "-10", "as": "offset"})
        routes.append(dict(source=edge["source"],target=edge["target"],guard=edge["guard"],points=points))
    # Mechanically derived three-role legend; lane headers carry no semantic fill.
    legend = prefix+"legend"
    add_cell(root, legend, "Legend", "rounded=0;html=1;container=1;verticalAlign=top;align=left;spacing=8;fillColor=#ffffff;strokeColor=#b3b3b3;fontStyle=1;"+FONT, "1", dict(x=30,y=footer_y,w=540,h=100), vertex="1")
    for i, (role, label) in enumerate((("action", "Action / saved outcome"),("decision", "Decision with guards"),("exception", "Rejected / unresolved / blocked"))):
        fill,stroke=PALETTE[role]
        add_cell(root,prefix+"legend-"+role,"",f"rounded=0;html=1;fillColor={fill};strokeColor={stroke};","%s"%legend,dict(x=10,y=30+i*20,w=20,h=10),vertex="1")
        add_cell(root,prefix+"legend-label-"+role,label,"text;html=1;align=left;"+FONT,legend,dict(x=40,y=25+i*20,w=460,h=20),vertex="1")
    add_cell(root,prefix+"footer","Activity final ends this interaction.\nA pending escrow has no final money outcome.","text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;"+FONT,"1",dict(x=590,y=footer_y+10,w=width-620,h=80),vertex="1")
    ET.indent(mxfile, space="  ")
    filename = OUT/f"AD_{uc}.drawio"
    ET.ElementTree(mxfile).write(filename,encoding="utf-8",xml_declaration=True)
    action_count=sum(n["kind"] in ("action","decision","exception") for n in g["nodes"])
    assert action_count<=15,(uc,action_count)
    return dict(diagram_id=f"AD-{uc}", use_case=uc, title=title, filename=str(filename.relative_to(BASE)).replace("\\","/"),
                node_count=len(g["nodes"]), activity_decision_count=action_count, edge_count=len(g["edges"]),
                width=width,height=height,semantic_notes=g["semantic_notes"],lanes=lane_defs,
                nodes=[dict(**n,geometry=rects[n["id"]]) for n in g["nodes"]],edges=routes,
                source_requirement_ids=specs[uc].get("source_requirement_ids",specs[uc].get("requirements",[])))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    human=json.loads((BASE/"content_user_buyer.json").read_text(encoding="utf-8-sig"))
    remaining=json.loads((BASE/"content_seller_admin_payment.json").read_text(encoding="utf-8-sig"))
    ucs=human["use_cases"]+(remaining["use_cases"] if isinstance(remaining,dict) else remaining)
    specs={u["id"]:u for u in ucs}
    items=graphs()
    assert {g["uc"] for g in items}==set(specs)
    manifest=[write_diagram(g,specs) for g in items]
    result=dict(schema_version="1.0", diagram_type="UML activity", source_policy="Freshly authored from approved MVP and current use-case specifications; no prior diagrams read or imported.", source_files=["content_user_buyer.json","content_seller_admin_payment.json"], layout="Deterministic lane-aware rows with obstacle-aware orthogonal grid routing; Graphviz unavailable.", style="Built-in default palette; Helvetica 14 actions/decisions and 16 titles; minimal blue actions, yellow decisions, grey exceptions; semantic legend included. Full action/guard details remain in node detail fields and semantic notes.",diagrams=manifest)
    (BASE/"activity_models.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(dict(diagrams=len(manifest),max_width=max(d["width"] for d in manifest),max_height=max(d["height"] for d in manifest),max_actions=max(d["activity_decision_count"] for d in manifest))))


if __name__=="__main__":
    main()
