<!-- Companion to the retained LaTeX source. -->

# Analysis

## General Use cases Diagram

EPS is an academic escrow simulation for goods and services. Each agreement has one Buyer, one distinct Seller and one full VND amount, funded through a Bank or Payment Gateway mock. The overview is divided into focused views for readability.

![Account access](analysis/diagrams/overview/UC_Account.png)

![Shared escrow-party actions](analysis/diagrams/overview/UC_SharedParty.png)

![Buyer journey](analysis/diagrams/overview/UC_Buyer.png)

![Seller journey](analysis/diagrams/overview/UC_Seller.png)

![Administration](analysis/diagrams/overview/UC_Admin.png)

![Payment integration](analysis/diagrams/overview/UC_Payment.png)

- **Guest:** registers an ordinary account and logs in with MFA.
- **Buyer:** creates and funds an escrow, accepts delivery and requests release.
- **Seller:** accepts the agreement and records delivery or service completion. Both participants may request a refund or open a dispute.
- **Admin:** resolves disputes, updates policy, views analytics/audit and reconciles pending transfers.
- **Merchant/Marketplace:** creates and queries only its own escrows through a separately authenticated client.
- **Partner Bank:** simulates funding, Seller release and refunds for Bank-funded escrows.
- **Payment Gateway:** simulates funding and refunds to the original Gateway source.

Buyer and Seller are roles in each transaction. Release uses the Bank mock; refund returns through the original funding provider. Real money, partial payments, milestones and automatic release are outside this MVP.

## Use case Details

### User's Use cases Details

**U1: Register**

| Field | Description |
| --- | --- |
| Use Case Code | U1 |
| Use Case Name | Register |

**Actor:** Guest

**Usage:** Create an ordinary user account.

**Activation Event:** Guest selects Register.

**Preconditions:** The login identifier is not already registered.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Guest | Enter account details and password. |
| 2 | EPS | Validate the details and start MFA enrollment; do not grant Admin or Merchant privileges. |
| 3 | Guest | Complete the MFA enrollment challenge. |
| 4 | EPS | Create the account after successful verification and direct the user to Login. |
| 5 | EPS | For invalid details, a duplicate identifier or failed MFA, reject registration without activating an account. |

**Postconditions:** A valid ordinary account is created; the user must log in separately.

**U2: Login with MFA**

| Field | Description |
| --- | --- |
| Use Case Code | U2 |
| Use Case Name | Login with MFA |

**Actor:** Buyer; Seller; Admin

**Usage:** Start an authenticated user session.

**Activation Event:** User selects Login.

**Preconditions:** An active user or pre-provisioned Admin account exists.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | User | Submit the login identifier and password. |
| 2 | EPS | Verify credentials and request the enrolled MFA factor. |
| 3 | User | Submit the MFA response. |
| 4 | EPS | Verify MFA, create the session and show the permitted workspace. |
| 5 | EPS | Reject invalid credentials or MFA without creating a session. Merchant client credentials cannot be used as a human login. |

**Postconditions:** A successful login creates a session with the account's existing permissions.

**U3: Logout**

| Field | Description |
| --- | --- |
| Use Case Code | U3 |
| Use Case Name | Logout |

**Actor:** Buyer; Seller; Admin

**Usage:** End the current user session.

**Activation Event:** User selects Logout.

**Preconditions:** A current or previously expired session is available.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | User | Select Logout. |
| 2 | EPS | Invalidate the current session and show Login. An already expired session returns the same result. |

**Postconditions:** The previous session cannot access protected functions.

**U4: View/Track Escrows**

| Field | Description |
| --- | --- |
| Use Case Code | U4 |
| Use Case Name | View/Track Escrows |

**Actor:** Buyer; Seller; Merchant/Marketplace (U4.API variant)

**Usage:** View escrows and their current progress.

**Activation Event:** User opens the escrow list or an escrow detail.

**Preconditions:** The user is authenticated and is a participant in the requested escrow.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | User | Request the list or select an escrow. |
| 2 | EPS | Check access and retrieve the authorised record. |
| 3 | EPS | Show terms, lifecycle, payment status, delivery, refund proposal and dispute status. |
| 4 | EPS | Show unresolved operations as pending with a query reference; viewing does not move money. |
| 5 | EPS | Reject access to another user's escrow without disclosing its data. |
| API | Merchant | U4.API: Authenticate the Merchant client and return only its owned escrow status. Pending results include a query reference. Reject other clients' escrows and exclude private dispute evidence and Admin audit data. |

**Postconditions:** The authorised current status is displayed; the escrow is unchanged.

**U5: Open Dispute**

| Field | Description |
| --- | --- |
| Use Case Code | U5 |
| Use Case Name | Open Dispute |

**Actor:** Buyer; Seller

**Usage:** Request Admin resolution of a held escrow.

**Activation Event:** Buyer or Seller selects Open Dispute.

**Preconditions:** The escrow is HELD or DELIVERED; no dispute has previously been opened and no payout is reserved.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer/Seller | Enter the dispute reason. |
| 2 | EPS | Recheck participant access and dispute eligibility. |
| 3 | EPS | Open the dispute and invalidate any pending refund proposal in one state change. |
| 4 | EPS | Save the case and allow both parties to submit evidence; block delivery and ordinary release. |
| 5 | EPS | Reject a stale or concurrent request if another payout or dispute decision has already been accepted. |

**Postconditions:** One OPEN dispute exists; the full amount remains held.

**U6: Submit Dispute Evidence**

| Field | Description |
| --- | --- |
| Use Case Code | U6 |
| Use Case Name | Submit Dispute Evidence |

**Actor:** Buyer; Seller

**Usage:** Add evidence to an open dispute.

**Activation Event:** A participant selects Submit Evidence.

**Preconditions:** The participant belongs to the escrow and the dispute remains OPEN.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer/Seller | Submit evidence and a short explanation. |
| 2 | EPS | Validate the submission and recheck that no final decision has been recorded. |
| 3 | EPS | Save the evidence with its author and submission time. |
| 4 | EPS | Reject unauthorised submissions or evidence received after the final decision. |

**Postconditions:** Accepted evidence is available for dispute review.

**U7: Propose/Withdraw Full Refund**

| Field | Description |
| --- | --- |
| Use Case Code | U7 |
| Use Case Name | Propose/Withdraw Full Refund |

**Actor:** Buyer; Seller

**Usage:** Propose or withdraw a full refund.

**Activation Event:** A participant selects Propose Refund or Withdraw Proposal.

**Preconditions:** The escrow is HELD or DELIVERED, with no open dispute or reserved payout.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer/Seller | Submit a full-refund reason, or select their pending proposal for withdrawal. |
| 2 | EPS | For a new proposal, check that no other proposal is pending; save it and notify the counterpart. |
| 3 | EPS | While the proposal is pending, block new delivery recording and ordinary Buyer release. |
| 4 | EPS | Allow only the proposer to withdraw before approval. Restore otherwise eligible actions without deleting saved delivery. |
| 5 | EPS | Reject stale requests; repeated requests return the recorded result. |

**Postconditions:** The proposal is PENDING or WITHDRAWN; no money is transferred.

**U8: Accept/Reject Refund Proposal**

| Field | Description |
| --- | --- |
| Use Case Code | U8 |
| Use Case Name | Accept/Reject Refund Proposal |

**Actor:** Buyer; Seller

**Usage:** Accept or reject the counterpart's full-refund proposal.

**Activation Event:** The counterpart responds to a proposal.

**Preconditions:** The proposal is PENDING and the escrow has no open dispute or reserved payout.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer/Seller | Review the proposal and choose Accept or Reject. |
| 2 | EPS | Recheck that the responder is the counterpart and the proposal remains eligible. |
| 3 | EPS | On acceptance, approve the proposal and reserve the full refund as REFUND_PENDING; invoke P3. |
| 4 | EPS | On rejection, mark REJECTED and restore otherwise eligible actions without reverting delivery. |
| 5 | EPS | Reject self-approval or a stale response. A repeated response returns the recorded result. |

**Postconditions:** Approval starts P3; rejection makes no payment. Only confirmed provider success produces REFUNDED.

### Buyer's Use cases Details

**B1: Create Escrow**

| Field | Description |
| --- | --- |
| Use Case Code | B1 |
| Use Case Name | Create Escrow |

**Actor:** Buyer; Merchant/Marketplace (B1.API variant)

**Usage:** Create an escrow agreement.

**Activation Event:** Buyer selects Create Escrow.

**Preconditions:** The Buyer is authenticated; the Buyer and Seller are distinct existing users.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer | Enter the Seller, GOODS/SERVICES, full VND amount, deliverable and acceptance criteria. |
| 2 | EPS | Validate the agreement and capture the current evidence policy and Seller destination. |
| 3 | EPS | Save the escrow as AWAITING_SELLER and notify the Seller. |
| 4 | EPS | Reject invalid terms or self-trading. An identical repeated creation returns the existing escrow. |
| API | Merchant | B1.API: Authenticate the Merchant client, use its bound Seller and validate the same B1 terms. Save client ownership and return the escrow reference and AWAITING_SELLER. Reject another Seller or conflicting request reuse; identical repeats return the existing escrow. |

**Postconditions:** The agreement awaits Seller acceptance; no funding has started.

**B2: Cancel Unfunded Escrow**

| Field | Description |
| --- | --- |
| Use Case Code | B2 |
| Use Case Name | Cancel Unfunded Escrow |

**Actor:** Buyer

**Usage:** Cancel an escrow before funding.

**Activation Event:** Buyer selects Cancel.

**Preconditions:** The escrow is AWAITING_SELLER or AWAITING_FUNDING; no money was received and no funding result is unresolved.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer | Confirm cancellation of their escrow. |
| 2 | EPS | Recheck ownership and funding status. |
| 3 | EPS | Set CANCELLED and record the reason. |
| 4 | EPS | Reject cancellation while funding is active or unknown. A repeated cancellation returns the existing result. |

**Postconditions:** The cancelled escrow cannot accept funding or payout.

**B3: Fund Escrow**

| Field | Description |
| --- | --- |
| Use Case Code | B3 |
| Use Case Name | Fund Escrow |

**Actor:** Buyer; Partner Bank; Payment Gateway

**Usage:** Fund the full accepted agreement through a mock provider.

**Activation Event:** Buyer selects Fund Escrow.

**Preconditions:** Seller has accepted; the escrow is AWAITING_FUNDING with no unresolved funding attempt.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer | Review the terms, accept them and choose Bank or Gateway. |
| 2 | EPS | Save a funding reference and set FUNDING_PENDING. |
| 3 | Bank/Gateway | Process the full VND funding request and return a result through P1. |
| 4 | EPS | Show the confirmed result, or keep pending if the result is uncertain. |
| 5 | EPS | Only confirmed failure with no receipt returns AWAITING_FUNDING, allowing the Buyer to retry or cancel. |

**Postconditions:** Only P1 confirmation establishes HELD. A timeout does not permit another funding attempt.

**B4: Confirm Acceptance and Request Release**

| Field | Description |
| --- | --- |
| Use Case Code | B4 |
| Use Case Name | Confirm Acceptance and Request Release |

**Actor:** Buyer; Partner Bank

**Usage:** Accept delivery and request full release to the Seller.

**Activation Event:** Buyer selects Confirm Acceptance.

**Preconditions:** The escrow is DELIVERED and its evidence policy is satisfied; no refund proposal, open dispute or payout is pending.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Buyer | Review delivery and confirm acceptance. |
| 2 | EPS | Recheck access, evidence and escrow eligibility. |
| 3 | EPS | Reserve the full amount as RELEASE_PENDING and invoke P2 through the Bank mock. |
| 4 | EPS | Show the pending or confirmed result. |
| 5 | EPS | Reject a conflicting request; a repeated acceptance returns the saved release decision. |

**Postconditions:** Release is requested once. RELEASED requires confirmed Bank settlement.

### Seller's Use cases Details

**S1: Accept/Reject Escrow Terms**

| Field | Description |
| --- | --- |
| Use Case Code | S1 |
| Use Case Name | Accept/Reject Escrow Terms |

**Actor:** Seller

**Usage:** Accept or reject a proposed escrow agreement.

**Activation Event:** Seller opens the proposed terms.

**Preconditions:** The escrow is AWAITING_SELLER and the user is its Seller.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Seller | Review the terms and choose Accept or Reject. |
| 2 | EPS | Recheck Seller access and the current state. |
| 3 | EPS | On acceptance, lock the terms and set AWAITING_FUNDING; on rejection, set CANCELLED with the reason. |
| 4 | EPS | Reject a stale change or return the previously recorded response. |

**Postconditions:** Accepted terms cannot be edited; funding is permitted only after acceptance.

**S2: Record Delivery/Service Completion**

| Field | Description |
| --- | --- |
| Use Case Code | S2 |
| Use Case Name | Record Delivery/Service Completion |

**Actor:** Seller

**Usage:** Record goods delivery or service completion.

**Activation Event:** Seller selects Record Delivery/Completion.

**Preconditions:** The escrow is HELD, with no pending refund proposal, open dispute or reserved payout.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Seller | Submit delivery information or the completed work and required evidence. |
| 2 | EPS | Check Seller access and the escrow's captured evidence policy. |
| 3 | EPS | Save completion, set DELIVERED and notify the Buyer. |
| 4 | EPS | Reject missing required evidence or an ineligible state; do not release money automatically. |

**Postconditions:** Delivery is recorded; the full amount remains held for Buyer acceptance or another eligible outcome.

### Admin's Use cases Details

**A1: Review and Resolve Dispute**

| Field | Description |
| --- | --- |
| Use Case Code | A1 |
| Use Case Name | Review and Resolve Dispute |

**Actor:** Admin

**Usage:** Resolve a dispute with one full payout decision.

**Activation Event:** Admin selects an open dispute.

**Preconditions:** Admin is authenticated; the dispute is OPEN, funds are held and no payout is reserved.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Admin | Review the agreement, evidence and payment status. |
| 2 | Admin | Choose full release or full refund and enter a reason. |
| 3 | EPS | Recheck the case; save RESOLVED and reserve the chosen payout in one state change. |
| 4 | EPS | Invoke P2 for release or P3 for refund. This decision does not require Buyer acceptance. |
| 5 | EPS | Show the pending or confirmed settlement; reject a conflicting second decision. |

**Postconditions:** The decision and payout direction are final; only provider confirmation completes the payment.

**A2: Configure Escrow Policy Parameters**

| Field | Description |
| --- | --- |
| Use Case Code | A2 |
| Use Case Name | Configure Escrow Policy Parameters |

**Actor:** Admin

**Usage:** Configure delivery-evidence requirements for new escrows.

**Activation Event:** Admin opens Escrow Policy.

**Preconditions:** Admin is authenticated with policy permission.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Admin | Review and edit the evidence-required flag for GOODS and SERVICES. |
| 2 | EPS | Validate the flags and save a new policy version. |
| 3 | EPS | Apply it only to escrows created afterwards; keep existing snapshots unchanged. |
| 4 | EPS | Record the change in the audit trail. Automatic release and milestones are not configurable. |

**Postconditions:** A valid policy version is available for new agreements.

**A3: View Basic Analytics**

| Field | Description |
| --- | --- |
| Use Case Code | A3 |
| Use Case Name | View Basic Analytics |

**Actor:** Admin

**Usage:** View basic statistics for simulated escrows.

**Activation Event:** Admin opens Analytics.

**Preconditions:** Admin is authenticated with analytics permission.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Admin | Select the period and transaction type. |
| 2 | EPS | Calculate counts and VND amounts by lifecycle state. |
| 3 | EPS | Show the observation time and simulated-data label; separate pending amounts from final outcomes. |

**Postconditions:** Statistics are displayed without changing escrow records.

**A4: View Audit Trail**

| Field | Description |
| --- | --- |
| Use Case Code | A4 |
| Use Case Name | View Audit Trail |

**Actor:** Admin

**Usage:** Inspect recorded system and escrow events.

**Activation Event:** Admin opens Audit Trail.

**Preconditions:** Admin is authenticated with audit permission.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Admin | Filter events by escrow, period or event type. |
| 2 | EPS | Return attributable events and correlation references, excluding authentication secrets. |
| 3 | EPS | Display the audit trail as read-only; show an empty result when no events match. |

**Postconditions:** Audit records remain unchanged.

**A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers**

| Field | Description |
| --- | --- |
| Use Case Code | A5 |
| Use Case Name | Reconcile Pending Transactions/Retry Confirmed-Failed Transfers |

**Actor:** Admin; Partner Bank; Payment Gateway

**Usage:** Reconcile uncertain operations and retry confirmed-failed payouts.

**Activation Event:** Admin selects an unresolved or failed payment attempt.

**Preconditions:** Admin is authenticated; the original provider and operation references are available.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | Admin | Request the status of the original operation. |
| 2 | EPS | Authenticate and match the provider result, then apply P1, P2 or P3 once. |
| 3 | EPS | For an unknown result, retain pending and allow queries only. |
| 4 | EPS | For confirmed failed funding with no receipt, return AWAITING_FUNDING; only the Buyer may fund again. |
| 5 | Admin | For a provider-confirmed failed payout with no money moved, request a retry. |
| 6 | EPS | Create one linked attempt with the same amount, direction and beneficiary. Never permit manual success or an opposite payout. |

**Postconditions:** The status is reconciled, remains pending, or has one authorised same-direction retry.

### Payment Integration's Use cases Details

**P1: Confirm Funding**

| Field | Description |
| --- | --- |
| Use Case Code | P1 |
| Use Case Name | Confirm Funding |

**Actor:** Partner Bank; Payment Gateway

**Usage:** Confirm whether the full funding amount was received.

**Activation Event:** Bank/Gateway sends a callback or answers a status query.

**Preconditions:** A saved funding attempt exists.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | EPS | Authenticate the provider and match escrow, operation, attempt, full amount and VND. |
| 2 | EPS | On confirmed receipt, record the held balance and set HELD once. |
| 3 | EPS | On confirmed failure with no receipt, return AWAITING_FUNDING. |
| 4 | EPS | For pending or unknown results, retain FUNDING_PENDING. |
| 5 | EPS | Return the stored result for duplicates. Reject mismatched or contradictory results and flag them for reconciliation. |

**Postconditions:** Funds are held only after a valid receipt; a duplicate never creates another credit.

**P2: Execute and Confirm Release**

| Field | Description |
| --- | --- |
| Use Case Code | P2 |
| Use Case Name | Execute and Confirm Release |

**Actor:** Partner Bank

**Usage:** Execute and confirm one full release to the Seller.

**Activation Event:** B4/A1 authorises release, or A5 authorises an eligible retry.

**Preconditions:** A full release decision and fixed Seller destination are saved; a retry requires confirmed failure with no money moved.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | EPS | Send the full VND amount to the Bank mock using the saved release reference. |
| 2 | Bank | Execute the mock transfer and return a callback or query result. |
| 3 | EPS | Authenticate and match the attempt, amount, currency and destination. |
| 4 | EPS | On success, set RELEASED once. On failure, keep RELEASE_PENDING and its reservation for an eligible A5 retry; on uncertainty, query only. |
| 5 | EPS | Reuse duplicate results and reject mismatches. Do not accept a new dispute or opposite payout after reservation. |

**Postconditions:** The Seller is paid once on confirmed success; otherwise the same release remains pending.

**P3: Execute and Confirm Refund**

| Field | Description |
| --- | --- |
| Use Case Code | P3 |
| Use Case Name | Execute and Confirm Refund |

**Actor:** Partner Bank; Payment Gateway

**Usage:** Execute and confirm one full refund to the original source.

**Activation Event:** U8/A1 authorises refund, or A5 authorises an eligible retry.

**Preconditions:** A full refund decision and original funding source are saved; a retry requires confirmed failure with no money moved.

**Main Event Flow**

| Index | Done by | Action |
| --- | --- | --- |
| 1 | EPS | Send the full VND refund through the original funding provider using the saved refund reference. |
| 2 | Bank/Gateway | Execute the mock refund and return a callback or query result. |
| 3 | EPS | Authenticate and match the attempt, amount, currency and original source. |
| 4 | EPS | On success, set REFUNDED once. On failure, keep REFUND_PENDING and its reservation for an eligible A5 retry; on uncertainty, query only. |
| 5 | EPS | Reuse duplicate results and reject mismatches. Do not accept a new dispute or opposite payout after reservation. |

**Postconditions:** The original source is refunded once on confirmed success; otherwise the same refund remains pending.

## Activity Diagram

### User's Use cases

![U1: Register](analysis/diagrams/activity/AD_U1.png)

![U2: Login with MFA](analysis/diagrams/activity/AD_U2.png)

![U3: Logout](analysis/diagrams/activity/AD_U3.png)

![U4: View/Track Escrows](analysis/diagrams/activity/AD_U4.png)

![U5: Open Dispute](analysis/diagrams/activity/AD_U5.png)

![U6: Submit Dispute Evidence](analysis/diagrams/activity/AD_U6.png)

![U7: Propose/Withdraw Full Refund](analysis/diagrams/activity/AD_U7.png)

![U8: Accept/Reject Refund Proposal](analysis/diagrams/activity/AD_U8.png)

### Buyer's Use cases

![B1: Create Escrow](analysis/diagrams/activity/AD_B1.png)

![B2: Cancel Unfunded Escrow](analysis/diagrams/activity/AD_B2.png)

![B3: Fund Escrow](analysis/diagrams/activity/AD_B3.png)

![B4: Confirm Acceptance and Request Release](analysis/diagrams/activity/AD_B4.png)

### Seller's Use cases

![S1: Accept/Reject Escrow Terms](analysis/diagrams/activity/AD_S1.png)

![S2: Record Delivery/Service Completion](analysis/diagrams/activity/AD_S2.png)

### Admin's Use cases

![A1: Review and Resolve Dispute](analysis/diagrams/activity/AD_A1.png)

![A2: Configure Escrow Policy Parameters](analysis/diagrams/activity/AD_A2.png)

![A3: View Basic Analytics](analysis/diagrams/activity/AD_A3.png)

![A4: View Audit Trail](analysis/diagrams/activity/AD_A4.png)

![A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers](analysis/diagrams/activity/AD_A5.png)

### Payment Integration's Use cases

![P1: Confirm Funding](analysis/diagrams/activity/AD_P1.png)

![P2: Execute and Confirm Release](analysis/diagrams/activity/AD_P2.png)

![P3: Execute and Confirm Refund](analysis/diagrams/activity/AD_P3.png)

## Sequence Diagram

Sequence diagrams show actor, boundary, control and entity interactions. Large flows continue in the referenced modules; B1.API and U4.API use the same business rules as their user-interface variants.

### User's Use cases

![U1: Register](analysis/diagrams/sequence/SD_U1.png)

![U1: Register (continued: U1_enrollment)](analysis/diagrams/sequence/SD_U1_enrollment.png)

![U2: Login with MFA](analysis/diagrams/sequence/SD_U2.png)

![U2: Login with MFA (continued: U2_mfa)](analysis/diagrams/sequence/SD_U2_mfa.png)

![U3: Logout](analysis/diagrams/sequence/SD_U3.png)

![U3: Logout (continued: U3_authorized_flow)](analysis/diagrams/sequence/SD_U3_authorized_flow.png)

![U4: View/Track Escrows](analysis/diagrams/sequence/SD_U4.png)

![U4: View/Track Escrows (continued: U4_outcomes)](analysis/diagrams/sequence/SD_U4_outcomes.png)

![U4: View/Track Escrows (continued: U4_tracking)](analysis/diagrams/sequence/SD_U4_tracking.png)

![U4.API: View/Track Escrows](analysis/diagrams/sequence/SD_U4.API.png)

![U4.API: View/Track Escrows (continued: U4.API_authorized_request)](analysis/diagrams/sequence/SD_U4.API_authorized_request.png)

![U4.API: View/Track Escrows (continued: U4.API_outcomes)](analysis/diagrams/sequence/SD_U4.API_outcomes.png)

![U5: Open Dispute](analysis/diagrams/sequence/SD_U5.png)

![U5: Open Dispute (continued: U5_outcomes)](analysis/diagrams/sequence/SD_U5_outcomes.png)

![U6: Submit Dispute Evidence](analysis/diagrams/sequence/SD_U6.png)

![U6: Submit Dispute Evidence (continued: U6_outcomes)](analysis/diagrams/sequence/SD_U6_outcomes.png)

![U7: Propose/Withdraw Full Refund](analysis/diagrams/sequence/SD_U7.png)

![U7: Propose/Withdraw Full Refund (continued: U7_outcomes)](analysis/diagrams/sequence/SD_U7_outcomes.png)

![U8: Accept/Reject Refund Proposal](analysis/diagrams/sequence/SD_U8.png)

![U8: Accept/Reject Refund Proposal (continued: U8_outcomes)](analysis/diagrams/sequence/SD_U8_outcomes.png)

![U8: Accept/Reject Refund Proposal (continued: U8_accept_refund)](analysis/diagrams/sequence/SD_U8_accept_refund.png)

### Buyer's Use cases

![B1: Create Escrow](analysis/diagrams/sequence/SD_B1.png)

![B1: Create Escrow (continued: B1_outcomes)](analysis/diagrams/sequence/SD_B1_outcomes.png)

![B1.API: Create Escrow](analysis/diagrams/sequence/SD_B1.API.png)

![B1.API: Create Escrow (continued: B1.API_authorized_request)](analysis/diagrams/sequence/SD_B1.API_authorized_request.png)

![B2: Cancel Unfunded Escrow](analysis/diagrams/sequence/SD_B2.png)

![B2: Cancel Unfunded Escrow (continued: B2_outcomes)](analysis/diagrams/sequence/SD_B2_outcomes.png)

![B3: Fund Escrow](analysis/diagrams/sequence/SD_B3.png)

![B3: Fund Escrow (continued: B3_funding)](analysis/diagrams/sequence/SD_B3_funding.png)

![B4: Confirm Acceptance and Request Release](analysis/diagrams/sequence/SD_B4.png)

![B4: Confirm Acceptance and Request Release (continued: B4_outcomes)](analysis/diagrams/sequence/SD_B4_outcomes.png)

### Seller's Use cases

![S1: Accept/Reject Escrow Terms](analysis/diagrams/sequence/SD_S1.png)

![S1: Accept/Reject Escrow Terms (continued: S1_outcomes)](analysis/diagrams/sequence/SD_S1_outcomes.png)

![S2: Record Delivery/Service Completion](analysis/diagrams/sequence/SD_S2.png)

![S2: Record Delivery/Service Completion (continued: S2_outcomes)](analysis/diagrams/sequence/SD_S2_outcomes.png)

### Admin's Use cases

![A1: Review and Resolve Dispute](analysis/diagrams/sequence/SD_A1.png)

![A1: Review and Resolve Dispute (continued: A1_decision)](analysis/diagrams/sequence/SD_A1_decision.png)

![A1: Review and Resolve Dispute (continued: A1_outcomes)](analysis/diagrams/sequence/SD_A1_outcomes.png)

![A2: Configure Escrow Policy Parameters](analysis/diagrams/sequence/SD_A2.png)

![A2: Configure Escrow Policy Parameters (continued: A2_outcomes)](analysis/diagrams/sequence/SD_A2_outcomes.png)

![A3: View Basic Analytics](analysis/diagrams/sequence/SD_A3.png)

![A3: View Basic Analytics (continued: A3_outcomes)](analysis/diagrams/sequence/SD_A3_outcomes.png)

![A4: View Audit Trail](analysis/diagrams/sequence/SD_A4.png)

![A4: View Audit Trail (continued: A4_outcomes)](analysis/diagrams/sequence/SD_A4_outcomes.png)

![A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers](analysis/diagrams/sequence/SD_A5.png)

![A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers (continued: A5_reconciliation)](analysis/diagrams/sequence/SD_A5_reconciliation.png)

![A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers (continued: A5_outcomes)](analysis/diagrams/sequence/SD_A5_outcomes.png)

![A5: Reconcile Pending Transactions/Retry Confirmed-Failed Transfers (continued: A5_retry)](analysis/diagrams/sequence/SD_A5_retry.png)

### Payment Integration's Use cases

![P1: Confirm Funding](analysis/diagrams/sequence/SD_P1.png)

![P1: Confirm Funding (continued: P1_outcomes)](analysis/diagrams/sequence/SD_P1_outcomes.png)

![P1: Confirm Funding (continued: P1_confirmed_receipt)](analysis/diagrams/sequence/SD_P1_confirmed_receipt.png)

![P2: Execute and Confirm Release](analysis/diagrams/sequence/SD_P2.png)

![P2: Execute and Confirm Release (continued: P2_settlement)](analysis/diagrams/sequence/SD_P2_settlement.png)

![P2: Execute and Confirm Release (continued: P2_outcomes)](analysis/diagrams/sequence/SD_P2_outcomes.png)

![P3: Execute and Confirm Refund](analysis/diagrams/sequence/SD_P3.png)

![P3: Execute and Confirm Refund (continued: P3_settlement)](analysis/diagrams/sequence/SD_P3_settlement.png)

![P3: Execute and Confirm Refund (continued: P3_outcomes)](analysis/diagrams/sequence/SD_P3_outcomes.png)

## Non-functional Requirements

The system must also meet the following non-functional requirements.

**Performance Requirements:**

- Target p95 response time is at most 2 seconds for internal create/query operations with 20 concurrent sessions and 1,000 simulated escrows, excluding user/provider waiting. This target has not been measured.
- Accepted operations must return a pending status and query reference when provider settlement is unresolved.

**Operational Requirements:**

- Preserve pending operations, policy snapshots and provider references after interruption so reconciliation can resume without duplicate transfers.
- Distinguish unknown outcomes from confirmed failures. Retry a payout only after confirmed failure with no money moved, preserving its direction and beneficiary.
- Keep audit records and dashboard counts consistent with recorded escrow states.

**Security Requirements:**

- Require MFA for human accounts and invalidate the session on logout. Authenticate Merchant clients separately.
- Check role, participant access and Merchant ownership on every protected operation.
- Use TLS and authenticate provider confirmations; reject mismatched amount, currency, destination or operation references.
- Keep the audit trail read-only and exclude passwords, MFA secrets and access tokens from logs.
- Process repeated or concurrent money decisions once, allowing only one final release or refund.

**Cultural and Political Requirements:**

- Use whole VND amounts and clear delivery, acceptance and evidence terms for both goods and services.
- Use synthetic data, label funds/providers as simulated and restrict personal and dispute evidence to authorised users.
- Legal claims in Planning remain unverified for real deployment; the MVP makes no claim of real-money custody or regulatory approval.

