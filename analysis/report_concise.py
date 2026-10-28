"""Concise report wording; full supporting models remain unchanged.

Latest instruction: follow the sample outline, shorten Analysis only, and keep
Introduction/Planning untouched. These summaries preserve the agreed MVP.
"""
import copy

# Each entry: purpose, trigger, preconditions, (actor, action) flow, postconditions.
CONTENT = {
'U1': (
 'Create an ordinary user account.', 'Guest selects Register.',
 ['The login identifier is not already registered.'],
 [('Guest','Enter account details and password.'),('EPS','Validate the details and start MFA enrollment; do not grant Admin or Merchant privileges.'),('Guest','Complete the MFA enrollment challenge.'),('EPS','Create the account after successful verification and direct the user to Login.'),('EPS','For invalid details, a duplicate identifier or failed MFA, reject registration without activating an account.')],
 ['A valid ordinary account is created; the user must log in separately.']),
'U2': (
 'Start an authenticated user session.', 'User selects Login.',
 ['An active user or pre-provisioned Admin account exists.'],
 [('User','Submit the login identifier and password.'),('EPS','Verify credentials and request the enrolled MFA factor.'),('User','Submit the MFA response.'),('EPS','Verify MFA, create the session and show the permitted workspace.'),('EPS','Reject invalid credentials or MFA without creating a session. Merchant client credentials cannot be used as a human login.')],
 ['A successful login creates a session with the account\'s existing permissions.']),
'U3': (
 'End the current user session.', 'User selects Logout.',
 ['A current or previously expired session is available.'],
 [('User','Select Logout.'),('EPS','Invalidate the current session and show Login. An already expired session returns the same result.')],
 ['The previous session cannot access protected functions.']),
'U4': (
 'View escrows and their current progress.', 'User opens the escrow list or an escrow detail.',
 ['The user is authenticated and is a participant in the requested escrow.'],
 [('User','Request the list or select an escrow.'),('EPS','Check access and retrieve the authorised record.'),('EPS','Show terms, lifecycle, payment status, delivery, refund proposal and dispute status.'),('EPS','Show unresolved operations as pending with a query reference; viewing does not move money.'),('EPS','Reject access to another user\'s escrow without disclosing its data.')],
 ['The authorised current status is displayed; the escrow is unchanged.']),
'U5': (
 'Request Admin resolution of a held escrow.', 'Buyer or Seller selects Open Dispute.',
 ['The escrow is HELD or DELIVERED; no dispute has previously been opened and no payout is reserved.'],
 [('Buyer/Seller','Enter the dispute reason.'),('EPS','Recheck participant access and dispute eligibility.'),('EPS','Open the dispute and invalidate any pending refund proposal in one state change.'),('EPS','Save the case and allow both parties to submit evidence; block delivery and ordinary release.'),('EPS','Reject a stale or concurrent request if another payout or dispute decision has already been accepted.')],
 ['One OPEN dispute exists; the full amount remains held.']),
'U6': (
 'Add evidence to an open dispute.', 'A participant selects Submit Evidence.',
 ['The participant belongs to the escrow and the dispute remains OPEN.'],
 [('Buyer/Seller','Submit evidence and a short explanation.'),('EPS','Validate the submission and recheck that no final decision has been recorded.'),('EPS','Save the evidence with its author and submission time.'),('EPS','Reject unauthorised submissions or evidence received after the final decision.')],
 ['Accepted evidence is available for dispute review.']),
'U7': (
 'Propose or withdraw a full refund.', 'A participant selects Propose Refund or Withdraw Proposal.',
 ['The escrow is HELD or DELIVERED, with no open dispute or reserved payout.'],
 [('Buyer/Seller','Submit a full-refund reason, or select their pending proposal for withdrawal.'),('EPS','For a new proposal, check that no other proposal is pending; save it and notify the counterpart.'),('EPS','While the proposal is pending, block new delivery recording and ordinary Buyer release.'),('EPS','Allow only the proposer to withdraw before approval. Restore otherwise eligible actions without deleting saved delivery.'),('EPS','Reject stale requests; repeated requests return the recorded result.')],
 ['The proposal is PENDING or WITHDRAWN; no money is transferred.']),
'U8': (
 'Accept or reject the counterpart\'s full-refund proposal.', 'The counterpart responds to a proposal.',
 ['The proposal is PENDING and the escrow has no open dispute or reserved payout.'],
 [('Buyer/Seller','Review the proposal and choose Accept or Reject.'),('EPS','Recheck that the responder is the counterpart and the proposal remains eligible.'),('EPS','On acceptance, approve the proposal and reserve the full refund as REFUND_PENDING; invoke P3.'),('EPS','On rejection, mark REJECTED and restore otherwise eligible actions without reverting delivery.'),('EPS','Reject self-approval or a stale response. A repeated response returns the recorded result.')],
 ['Approval starts P3; rejection makes no payment. Only confirmed provider success produces REFUNDED.']),
'B1': (
 'Create an escrow agreement.', 'Buyer selects Create Escrow.',
 ['The Buyer is authenticated; the Buyer and Seller are distinct existing users.'],
 [('Buyer','Enter the Seller, GOODS/SERVICES, full VND amount, deliverable and acceptance criteria.'),('EPS','Validate the agreement and capture the current evidence policy and Seller destination.'),('EPS','Save the escrow as AWAITING_SELLER and notify the Seller.'),('EPS','Reject invalid terms or self-trading. An identical repeated creation returns the existing escrow.')],
 ['The agreement awaits Seller acceptance; no funding has started.']),
'B2': (
 'Cancel an escrow before funding.', 'Buyer selects Cancel.',
 ['The escrow is AWAITING_SELLER or AWAITING_FUNDING; no money was received and no funding result is unresolved.'],
 [('Buyer','Confirm cancellation of their escrow.'),('EPS','Recheck ownership and funding status.'),('EPS','Set CANCELLED and record the reason.'),('EPS','Reject cancellation while funding is active or unknown. A repeated cancellation returns the existing result.')],
 ['The cancelled escrow cannot accept funding or payout.']),
'B3': (
 'Fund the full accepted agreement through a mock provider.', 'Buyer selects Fund Escrow.',
 ['Seller has accepted; the escrow is AWAITING_FUNDING with no unresolved funding attempt.'],
 [('Buyer','Review the terms, accept them and choose Bank or Gateway.'),('EPS','Save a funding reference and set FUNDING_PENDING.'),('Bank/Gateway','Process the full VND funding request and return a result through P1.'),('EPS','Show the confirmed result, or keep pending if the result is uncertain.'),('EPS','Only confirmed failure with no receipt returns AWAITING_FUNDING, allowing the Buyer to retry or cancel.')],
 ['Only P1 confirmation establishes HELD. A timeout does not permit another funding attempt.']),
'B4': (
 'Accept delivery and request full release to the Seller.', 'Buyer selects Confirm Acceptance.',
 ['The escrow is DELIVERED and its evidence policy is satisfied; no refund proposal, open dispute or payout is pending.'],
 [('Buyer','Review delivery and confirm acceptance.'),('EPS','Recheck access, evidence and escrow eligibility.'),('EPS','Reserve the full amount as RELEASE_PENDING and invoke P2 through the Bank mock.'),('EPS','Show the pending or confirmed result.'),('EPS','Reject a conflicting request; a repeated acceptance returns the saved release decision.')],
 ['Release is requested once. RELEASED requires confirmed Bank settlement.']),
'S1': (
 'Accept or reject a proposed escrow agreement.', 'Seller opens the proposed terms.',
 ['The escrow is AWAITING_SELLER and the user is its Seller.'],
 [('Seller','Review the terms and choose Accept or Reject.'),('EPS','Recheck Seller access and the current state.'),('EPS','On acceptance, lock the terms and set AWAITING_FUNDING; on rejection, set CANCELLED with the reason.'),('EPS','Reject a stale change or return the previously recorded response.')],
 ['Accepted terms cannot be edited; funding is permitted only after acceptance.']),
'S2': (
 'Record goods delivery or service completion.', 'Seller selects Record Delivery/Completion.',
 ['The escrow is HELD, with no pending refund proposal, open dispute or reserved payout.'],
 [('Seller','Submit delivery information or the completed work and required evidence.'),('EPS','Check Seller access and the escrow\'s captured evidence policy.'),('EPS','Save completion, set DELIVERED and notify the Buyer.'),('EPS','Reject missing required evidence or an ineligible state; do not release money automatically.')],
 ['Delivery is recorded; the full amount remains held for Buyer acceptance or another eligible outcome.']),
'A1': (
 'Resolve a dispute with one full payout decision.', 'Admin selects an open dispute.',
 ['Admin is authenticated; the dispute is OPEN, funds are held and no payout is reserved.'],
 [('Admin','Review the agreement, evidence and payment status.'),('Admin','Choose full release or full refund and enter a reason.'),('EPS','Recheck the case; save RESOLVED and reserve the chosen payout in one state change.'),('EPS','Invoke P2 for release or P3 for refund. This decision does not require Buyer acceptance.'),('EPS','Show the pending or confirmed settlement; reject a conflicting second decision.')],
 ['The decision and payout direction are final; only provider confirmation completes the payment.']),
'A2': (
 'Configure delivery-evidence requirements for new escrows.', 'Admin opens Escrow Policy.',
 ['Admin is authenticated with policy permission.'],
 [('Admin','Review and edit the evidence-required flag for GOODS and SERVICES.'),('EPS','Validate the flags and save a new policy version.'),('EPS','Apply it only to escrows created afterwards; keep existing snapshots unchanged.'),('EPS','Record the change in the audit trail. Automatic release and milestones are not configurable.')],
 ['A valid policy version is available for new agreements.']),
'A3': (
 'View basic statistics for simulated escrows.', 'Admin opens Analytics.',
 ['Admin is authenticated with analytics permission.'],
 [('Admin','Select the period and transaction type.'),('EPS','Calculate counts and VND amounts by lifecycle state.'),('EPS','Show the observation time and simulated-data label; separate pending amounts from final outcomes.')],
 ['Statistics are displayed without changing escrow records.']),
'A4': (
 'Inspect recorded system and escrow events.', 'Admin opens Audit Trail.',
 ['Admin is authenticated with audit permission.'],
 [('Admin','Filter events by escrow, period or event type.'),('EPS','Return attributable events and correlation references, excluding authentication secrets.'),('EPS','Display the audit trail as read-only; show an empty result when no events match.')],
 ['Audit records remain unchanged.']),
'A5': (
 'Reconcile uncertain operations and retry confirmed-failed payouts.', 'Admin selects an unresolved or failed payment attempt.',
 ['Admin is authenticated; the original provider and operation references are available.'],
 [('Admin','Request the status of the original operation.'),('EPS','Authenticate and match the provider result, then apply P1, P2 or P3 once.'),('EPS','For an unknown result, retain pending and allow queries only.'),('EPS','For confirmed failed funding with no receipt, return AWAITING_FUNDING; only the Buyer may fund again.'),('Admin','For a provider-confirmed failed payout with no money moved, request a retry.'),('EPS','Create one linked attempt with the same amount, direction and beneficiary. Never permit manual success or an opposite payout.')],
 ['The status is reconciled, remains pending, or has one authorised same-direction retry.']),
'P1': (
 'Confirm whether the full funding amount was received.', 'Bank/Gateway sends a callback or answers a status query.',
 ['A saved funding attempt exists.'],
 [('EPS','Authenticate the provider and match escrow, operation, attempt, full amount and VND.'),('EPS','On confirmed receipt, record the held balance and set HELD once.'),('EPS','On confirmed failure with no receipt, return AWAITING_FUNDING.'),('EPS','For pending or unknown results, retain FUNDING_PENDING.'),('EPS','Return the stored result for duplicates. Reject mismatched or contradictory results and flag them for reconciliation.')],
 ['Funds are held only after a valid receipt; a duplicate never creates another credit.']),
'P2': (
 'Execute and confirm one full release to the Seller.', 'B4/A1 authorises release, or A5 authorises an eligible retry.',
 ['A full release decision and fixed Seller destination are saved; a retry requires confirmed failure with no money moved.'],
 [('EPS','Send the full VND amount to the Bank mock using the saved release reference.'),('Bank','Execute the mock transfer and return a callback or query result.'),('EPS','Authenticate and match the attempt, amount, currency and destination.'),('EPS','On success, set RELEASED once. On failure, keep RELEASE_PENDING and its reservation for an eligible A5 retry; on uncertainty, query only.'),('EPS','Reuse duplicate results and reject mismatches. Do not accept a new dispute or opposite payout after reservation.')],
 ['The Seller is paid once on confirmed success; otherwise the same release remains pending.']),
'P3': (
 'Execute and confirm one full refund to the original source.', 'U8/A1 authorises refund, or A5 authorises an eligible retry.',
 ['A full refund decision and original funding source are saved; a retry requires confirmed failure with no money moved.'],
 [('EPS','Send the full VND refund through the original funding provider using the saved refund reference.'),('Bank/Gateway','Execute the mock refund and return a callback or query result.'),('EPS','Authenticate and match the attempt, amount, currency and original source.'),('EPS','On success, set REFUNDED once. On failure, keep REFUND_PENDING and its reservation for an eligible A5 retry; on uncertainty, query only.'),('EPS','Reuse duplicate results and reject mismatches. Do not accept a new dispute or opposite payout after reservation.')],
 ['The original source is refunded once on confirmed success; otherwise the same refund remains pending.'])
}

def concise_cases(cases):
    output = copy.deepcopy(cases)
    assert {u['id'] for u in output} == set(CONTENT)
    for uc in output:
        usage, activation, pre, flow, post = CONTENT[uc['id']]
        uc.update(usage=usage, activation=activation, preconditions=pre,
                  flow=[{'index':str(i),'by':by,'action':action} for i,(by,action) in enumerate(flow,1)],
                  postconditions=post)
        if uc['id']=='B1':
            uc['api_variants']=[{'id':'B1.API','actor':'Merchant',
                'summary':'Authenticate the Merchant client, use its bound Seller and validate the same B1 terms. Save client ownership and return the escrow reference and AWAITING_SELLER. Reject another Seller or conflicting request reuse; identical repeats return the existing escrow.'}]
        if uc['id']=='U4':
            uc['api_variants']=[{'id':'U4.API','actor':'Merchant',
                'summary':'Authenticate the Merchant client and return only its owned escrow status. Pending results include a query reference. Reject other clients\' escrows and exclude private dispute evidence and Admin audit data.'}]
    return output

NFR = {
'Performance Requirements':[
 'Target p95 response time is at most 2 seconds for internal create/query operations with 20 concurrent sessions and 1,000 simulated escrows, excluding user/provider waiting. This target has not been measured.',
 'Accepted operations must return a pending status and query reference when provider settlement is unresolved.'],
'Operational Requirements':[
 'Preserve pending operations, policy snapshots and provider references after interruption so reconciliation can resume without duplicate transfers.',
 'Distinguish unknown outcomes from confirmed failures. Retry a payout only after confirmed failure with no money moved, preserving its direction and beneficiary.',
 'Keep audit records and dashboard counts consistent with recorded escrow states.'],
'Security Requirements':[
 'Require MFA for human accounts and invalidate the session on logout. Authenticate Merchant clients separately.',
 'Check role, participant access and Merchant ownership on every protected operation.',
 'Use TLS and authenticate provider confirmations; reject mismatched amount, currency, destination or operation references.',
 'Keep the audit trail read-only and exclude passwords, MFA secrets and access tokens from logs.',
 'Process repeated or concurrent money decisions once, allowing only one final release or refund.'],
'Cultural and Political Requirements':[
 'Use whole VND amounts and clear delivery, acceptance and evidence terms for both goods and services.',
 'Use synthetic data, label funds/providers as simulated and restrict personal and dispute evidence to authorised users.',
 'Legal claims in Planning remain unverified for real deployment; the MVP makes no claim of real-money custody or regulatory approval.']}
