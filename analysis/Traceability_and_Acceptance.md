# EPS - Traceability and Acceptance

This support document defines coverage and future acceptance scenarios. It is not an executed test report. It remains outside Chapter 3, preserving Sections 3.1-3.5.

## Functional coverage

| Requirement | Capability | Use cases | Activities | Logical sequences | Business rules |
| --- | --- | --- | --- | --- | --- |
| FR01 | Account registration and authentication | U1, U2, U3 | AD-U1, AD-U2, AD-U3 | SD-U1, SD-U2, SD-U3 | BR03, BR25 |
| FR02 | Escrow agreement lifecycle | B1, B1.API, B2, S1 | AD-B1, AD-B2, AD-S1 | SD-B1, SD-B1.API, SD-B2, SD-S1 | BR01, BR02, BR04, BR05, BR23 |
| FR03 | Funding through two mock methods | B3, P1 | AD-B3, AD-P1 | SD-B3, SD-P1 | BR01, BR05, BR07, BR08, BR18, BR19, BR21, BR23, BR27 |
| FR04 | Held balance and transaction tracking | U4, P1, U4.API | AD-U4, AD-P1 | SD-U4, SD-P1, SD-U4.API | BR01, BR08, BR09 |
| FR05 | Delivery and Buyer-approved full release | S2, B4, P2 | AD-S2, AD-B4, AD-P2 | SD-S2, SD-B4, SD-P2 | BR01, BR10, BR11, BR17, BR20, BR22, BR27 |
| FR06 | Consensual full refund | U7, U8, P3 | AD-U7, AD-U8, AD-P3 | SD-U7, SD-U8, SD-P3 | BR01, BR12, BR13, BR17, BR20, BR22, BR27 |
| FR07 | Dispute evidence and Admin resolution | U5, U6, A1, P2, P3 | AD-U5, AD-U6, AD-A1, AD-P2, AD-P3 | SD-U5, SD-U6, SD-A1, SD-P2, SD-P3 | BR14, BR15, BR16, BR17, BR20 |
| FR08 | Versioned evidence policy | A2, B1, S2, B4 | AD-A2, AD-B1, AD-S2, AD-B4 | SD-A2, SD-B1, SD-S2, SD-B4 | BR04, BR06, BR10 |
| FR09 | Basic administrative analytics | A3 | AD-A3 | SD-A3 | BR26 |
| FR10 | Read-only audit inspection | A4 | AD-A4 | SD-A4 | BR21, BR25 |
| FR11 | Asynchronous payment integration and reconciliation | P1, P2, P3, A5 | AD-P1, AD-P2, AD-P3, AD-A5 | SD-P1, SD-P2, SD-P3, SD-A5 | BR08, BR17, BR18, BR19, BR20, BR21, BR22, BR25, BR27 |
| FR12 | Restricted Merchant create/query API | B1.API, U4.API | AD-B1, AD-U4 | SD-B1.API, SD-U4.API | BR03, BR04, BR24 |

B1.API/U4.API share B1/U4 activity contracts and have dedicated Merchant sequence views. Continuations belong to the same logical sequence and do not increase the use-case count.

## Acceptance criteria by requirement

### FR01 - Account registration and authentication

- Registration does not provision an Admin or Merchant client.
- A user session is issued only after both factors succeed; logout invalidates the session.

### FR02 - Escrow agreement lifecycle

- The two participant identities are distinct and valid.
- Terms and the creation-time policy snapshot become immutable on Seller acceptance.
- Buyer can cancel only when no funding operation is pending and no money has been received.

### FR03 - Funding through two mock methods

- Initiation creates FUNDING_PENDING, not HELD.
- Only an authenticated, matched provider receipt for the full VND amount creates HELD.
- Confirmed failure with no money received returns to AWAITING_FUNDING; unknown results remain pending.

### FR04 - Held balance and transaction tracking

- One successful full funding receipt is recorded per escrow.
- A held amount is never represented as released or refunded until the corresponding provider success is confirmed.
- The escrow detail distinguishes lifecycle state from attempt result and pending proposal/dispute.

### FR05 - Delivery and Buyer-approved full release

- Seller completion alone does not release funds.
- Ordinary Buyer release requires DELIVERED, policy evidence satisfaction, no pending refund proposal and no open dispute.
- The full amount is released once through Partner Bank mock to the agreed Seller destination.

### FR06 - Consensual full refund

- A pending proposal blocks new Seller delivery recording and Buyer release without changing HELD/DELIVERED; rejection/withdrawal restores otherwise eligible actions without reverting an existing delivery record.
- Counterpart approval atomically sets APPROVED and REFUND_PENDING.
- Confirmed full refund goes to the original funding source.

### FR07 - Dispute evidence and Admin resolution

- Opening the single dispute invalidates a pending refund proposal.
- Admin records a reason and exactly one payout direction.
- The decision resolves the dispute and starts a pending payout; there is no appeal or second dispute in the MVP.

### FR08 - Versioned evidence policy

- Default GOODS evidence is optional and SERVICES evidence is required.
- The configurable value is an evidence-required boolean per transaction type.
- Changes affect only future escrows and cannot introduce automatic release, deadlines or milestones.

### FR09 - Basic administrative analytics

- Dashboard figures reconcile with the authorised escrow records used by the view.
- A pending transfer is not counted as a completed release/refund.
- There are no invented revenue, FX or real-bank balance measures.

### FR10 - Read-only audit inspection

- Events identify actor/service, escrow or operation, event, time, result and correlation reference.
- Read access does not permit update or deletion of audit events.
- Password, MFA secret, access token and full client secret are excluded.

### FR11 - Asynchronous payment integration and reconciliation

- Duplicate or delayed messages do not duplicate funding or payout.
- Timeouts and unknown results remain pending with query-only reconciliation.
- Confirmed failed payouts retain RELEASE_PENDING/REFUND_PENDING and the original payout decision for a controlled same-direction retry.
- Admin cannot manually mark an operation successful.

### FR12 - Restricted Merchant create/query API

- Merchant client identity, owner and Seller binding are derived from trusted client configuration.
- Merchant creates and queries only; it cannot fund, accept delivery, propose/approve refunds, open disputes or resolve them.
- API creation follows the same terms, policy, validation and duplicate-submission rules as UI creation; pending states are queryable.

## Diagram inventory

| Code | Activity source | Main sequence source | Continuation IDs |
| --- | --- | --- | --- |
| U1 | diagrams/activity/AD_U1.drawio | diagrams/sequence/SD_U1.drawio | U1_enrollment |
| U2 | diagrams/activity/AD_U2.drawio | diagrams/sequence/SD_U2.drawio | U2_mfa |
| U3 | diagrams/activity/AD_U3.drawio | diagrams/sequence/SD_U3.drawio | U3_authorized_flow |
| U4 | diagrams/activity/AD_U4.drawio | diagrams/sequence/SD_U4.drawio | U4_outcomes, U4_tracking |
| U5 | diagrams/activity/AD_U5.drawio | diagrams/sequence/SD_U5.drawio | U5_outcomes |
| U6 | diagrams/activity/AD_U6.drawio | diagrams/sequence/SD_U6.drawio | U6_outcomes |
| U7 | diagrams/activity/AD_U7.drawio | diagrams/sequence/SD_U7.drawio | U7_outcomes |
| U8 | diagrams/activity/AD_U8.drawio | diagrams/sequence/SD_U8.drawio | U8_outcomes, U8_accept_refund |
| B1 | diagrams/activity/AD_B1.drawio | diagrams/sequence/SD_B1.drawio | B1_outcomes |
| B2 | diagrams/activity/AD_B2.drawio | diagrams/sequence/SD_B2.drawio | B2_outcomes |
| B3 | diagrams/activity/AD_B3.drawio | diagrams/sequence/SD_B3.drawio | B3_funding |
| B4 | diagrams/activity/AD_B4.drawio | diagrams/sequence/SD_B4.drawio | B4_outcomes |
| S1 | diagrams/activity/AD_S1.drawio | diagrams/sequence/SD_S1.drawio | S1_outcomes |
| S2 | diagrams/activity/AD_S2.drawio | diagrams/sequence/SD_S2.drawio | S2_outcomes |
| A1 | diagrams/activity/AD_A1.drawio | diagrams/sequence/SD_A1.drawio | A1_decision, A1_outcomes |
| A2 | diagrams/activity/AD_A2.drawio | diagrams/sequence/SD_A2.drawio | A2_outcomes |
| A3 | diagrams/activity/AD_A3.drawio | diagrams/sequence/SD_A3.drawio | A3_outcomes |
| A4 | diagrams/activity/AD_A4.drawio | diagrams/sequence/SD_A4.drawio | A4_outcomes |
| A5 | diagrams/activity/AD_A5.drawio | diagrams/sequence/SD_A5.drawio | A5_reconciliation, A5_outcomes, A5_retry |
| P1 | diagrams/activity/AD_P1.drawio | diagrams/sequence/SD_P1.drawio | P1_outcomes, P1_confirmed_receipt |
| P2 | diagrams/activity/AD_P2.drawio | diagrams/sequence/SD_P2.drawio | P2_settlement, P2_outcomes |
| P3 | diagrams/activity/AD_P3.drawio | diagrams/sequence/SD_P3.drawio | P3_settlement, P3_outcomes |
| B1.API | diagrams/activity/AD_B1.drawio | diagrams/sequence/SD_B1.API.drawio | B1.API_authorized_request |
| U4.API | diagrams/activity/AD_U4.drawio | diagrams/sequence/SD_U4.API.drawio | U4.API_authorized_request, U4.API_outcomes |

## Basic acceptance matrix

The 16 paths cover GOODS/SERVICES x BANK/GATEWAY x BUYER_RELEASE/CONSENSUAL_REFUND/ADMIN_RELEASE/ADMIN_REFUND. Every path uses the full amount and synthetic data, and ends only on a verified mock provider success.

| ID | Transaction type | Funding | Outcome | Final state |
| --- | --- | --- | --- | --- |
| AT01 | GOODS | BANK | BUYER_RELEASE | RELEASED |
| AT02 | GOODS | BANK | CONSENSUAL_REFUND | REFUNDED |
| AT03 | GOODS | BANK | ADMIN_RELEASE | RELEASED |
| AT04 | GOODS | BANK | ADMIN_REFUND | REFUNDED |
| AT05 | GOODS | GATEWAY | BUYER_RELEASE | RELEASED |
| AT06 | GOODS | GATEWAY | CONSENSUAL_REFUND | REFUNDED |
| AT07 | GOODS | GATEWAY | ADMIN_RELEASE | RELEASED |
| AT08 | GOODS | GATEWAY | ADMIN_REFUND | REFUNDED |
| AT09 | SERVICES | BANK | BUYER_RELEASE | RELEASED |
| AT10 | SERVICES | BANK | CONSENSUAL_REFUND | REFUNDED |
| AT11 | SERVICES | BANK | ADMIN_RELEASE | RELEASED |
| AT12 | SERVICES | BANK | ADMIN_REFUND | REFUNDED |
| AT13 | SERVICES | GATEWAY | BUYER_RELEASE | RELEASED |
| AT14 | SERVICES | GATEWAY | CONSENSUAL_REFUND | REFUNDED |
| AT15 | SERVICES | GATEWAY | ADMIN_RELEASE | RELEASED |
| AT16 | SERVICES | GATEWAY | ADMIN_REFUND | REFUNDED |

### AT01 - GOODS / BANK / BUYER_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. Seller records delivery information (evidence optional under the default policy); verify DELIVERED with no automatic payout.
5. Buyer explicitly accepts delivery and requests full release; verify RELEASE_PENDING.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, S2, B4, P2, U4.

### AT02 - GOODS / BANK / CONSENSUAL_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant proposes full refund; verify the counterpart approves it, proposal APPROVED and lifecycle REFUND_PENDING.
5. Authenticate and match the final original BANK refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original BANK funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U7, U8, P3, U4.

### AT03 - GOODS / BANK / ADMIN_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full RELEASE; verify dispute RESOLVED and lifecycle RELEASE_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P2, U4.

### AT04 - GOODS / BANK / ADMIN_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full REFUND; verify dispute RESOLVED and lifecycle REFUND_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final original BANK refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original BANK funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P3, U4.

### AT05 - GOODS / GATEWAY / BUYER_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. Seller records delivery information (evidence optional under the default policy); verify DELIVERED with no automatic payout.
5. Buyer explicitly accepts delivery and requests full release; verify RELEASE_PENDING.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, S2, B4, P2, U4.

### AT06 - GOODS / GATEWAY / CONSENSUAL_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant proposes full refund; verify the counterpart approves it, proposal APPROVED and lifecycle REFUND_PENDING.
5. Authenticate and match the final original GATEWAY refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original GATEWAY funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U7, U8, P3, U4.

### AT07 - GOODS / GATEWAY / ADMIN_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full RELEASE; verify dispute RESOLVED and lifecycle RELEASE_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P2, U4.

### AT08 - GOODS / GATEWAY / ADMIN_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full REFUND; verify dispute RESOLVED and lifecycle REFUND_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final original GATEWAY refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original GATEWAY funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P3, U4.

### AT09 - SERVICES / BANK / BUYER_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. Seller records the service work product with required evidence; verify DELIVERED with no automatic payout.
5. Buyer explicitly accepts delivery and requests full release; verify RELEASE_PENDING.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, S2, B4, P2, U4.

### AT10 - SERVICES / BANK / CONSENSUAL_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant proposes full refund; verify the counterpart approves it, proposal APPROVED and lifecycle REFUND_PENDING.
5. Authenticate and match the final original BANK refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original BANK funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U7, U8, P3, U4.

### AT11 - SERVICES / BANK / ADMIN_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full RELEASE; verify dispute RESOLVED and lifecycle RELEASE_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P2, U4.

### AT12 - SERVICES / BANK / ADMIN_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full BANK mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full REFUND; verify dispute RESOLVED and lifecycle REFUND_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final original BANK refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original BANK funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P3, U4.

### AT13 - SERVICES / GATEWAY / BUYER_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. Seller records the service work product with required evidence; verify DELIVERED with no automatic payout.
5. Buyer explicitly accepts delivery and requests full release; verify RELEASE_PENDING.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, S2, B4, P2, U4.

### AT14 - SERVICES / GATEWAY / CONSENSUAL_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant proposes full refund; verify the counterpart approves it, proposal APPROVED and lifecycle REFUND_PENDING.
5. Authenticate and match the final original GATEWAY refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original GATEWAY funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U7, U8, P3, U4.

### AT15 - SERVICES / GATEWAY / ADMIN_RELEASE

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full RELEASE; verify dispute RESOLVED and lifecycle RELEASE_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final Partner Bank release confirmation for the full amount.

Expected results:

- Final lifecycle RELEASED; exactly one terminal money outcome.
- The full amount reaches the locked Seller destination through Partner Bank in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P2, U4.

### AT16 - SERVICES / GATEWAY / ADMIN_REFUND

Preconditions: Two distinct registered users with valid MFA sessions; pre-provisioned Admin for dispute branches; mock providers configured; default evidence policy captured at creation.

1. Create a valid escrow for two distinct users and capture the default evidence policy.
2. Seller accepts the immutable terms.
3. Buyer initiates full GATEWAY mock funding; verify FUNDING_PENDING until a matched success confirmation establishes HELD.
4. One participant opens the single dispute; both participants submit evidence while OPEN.
5. Admin reviews evidence, records a reason and decides full REFUND; verify dispute RESOLVED and lifecycle REFUND_PENDING without requiring Buyer acceptance.
6. Authenticate and match the final original GATEWAY refund confirmation for the full amount.

Expected results:

- Final lifecycle REFUNDED; exactly one terminal money outcome.
- The full amount reaches the original GATEWAY funding source in the mock ledger; no remaining simulated held balance.
- State, attempt, provider operation and audit records agree; duplicate final confirmation does not move money again.

Use-case coverage: B1, S1, B3, P1, U5, U6, A1, P3, U4.

## Focused exception and concurrency scenarios

### NEG01 - Seller rejects or Buyer safely cancels

Setup/action: Reject at AWAITING_SELLER; separately cancel at AWAITING_SELLER and AWAITING_FUNDING with no active/unknown funding.

Expected: CANCELLED; no provider funding/payout call; later accept/fund actions are rejected.

Rules: BR05, BR23.

### NEG02 - Funding before Seller acceptance

Setup/action: Buyer attempts funding at AWAITING_SELLER.

Expected: Rejected with unchanged state and no provider call.

Rules: BR05, BR07.

### NEG03 - Confirmed failed funding and safe retry/cancellation

Setup/action: Start funding; provider confirms failure with no money received; retry in one case and cancel in another.

Expected: Return to AWAITING_FUNDING. A new attempt is allowed, or cancellation yields CANCELLED; failed attempt is retained in audit.

Rules: BR19, BR23.

### NEG04 - Unknown funding outcome

Setup/action: Withhold funding result, time out, then request another funding attempt and cancellation.

Expected: Keep FUNDING_PENDING; both requests rejected; A5 queries the existing attempt. A later matched success establishes HELD once.

Rules: BR07, BR18, BR23.

### NEG05 - Mismatched or unauthenticated callback

Setup/action: Submit wrong provider authentication and mismatched operation/attempt/amount/currency messages.

Expected: No money-state transition; record rejection/correlation for investigation; only a correct matched current receipt can establish success.

Rules: BR08, BR21.

### NEG06 - Duplicate user request and callback

Setup/action: Repeat funding/payout initiation and success callback, including concurrent delivery of exact duplicates.

Expected: A repeated accepted action returns its recorded outcome and creates no extra transfer; receipt processed once; one terminal money outcome.

Rules: BR17, BR20, BR21.

### NEG07 - Late/stale callback after retry

Setup/action: Confirm an attempt failed with no money moved, start an allowed retry, then replay an old-attempt message.

Expected: Old message cannot overwrite the retry or terminal state; consistent duplicates are ignored. Contradictory old-attempt results are flagged for reconciliation, not used to create a second money outcome.

Rules: BR19, BR21.

### NEG08 - Delivery and policy checks

Setup/action: Record Seller completion without required evidence; attempt Buyer release before delivery; attempt Seller-triggered automatic payout.

Expected: Invalid completion/release is rejected and no payout occurs. Valid Seller completion creates DELIVERED only; explicit Buyer acceptance is still required.

Rules: BR06, BR10, BR11.

### NEG09 - Refund freeze, rejection and withdrawal

Setup/action: In a HELD escrow, propose refund and attempt Seller delivery recording; reject/withdraw the proposal and retry delivery. In a separate DELIVERED escrow, propose refund and attempt Buyer release; reject/withdraw the proposal and retry release. Race delivery recording against a new proposal in an additional HELD case.

Expected: While PENDING, both new Seller delivery recording and ordinary Buyer release are blocked. REJECTED/WITHDRAWN restores otherwise eligible actions, retaining HELD/DELIVERED and any existing delivery record. In the delivery/proposal race, the atomic order is respected: proposal first blocks delivery; delivery first records DELIVERED, after which an eligible proposal may still freeze release. No automatic payout occurs.

Rules: BR10, BR12, BR13.

### NEG10 - Wrong person responds to refund

Setup/action: Proposer attempts self-approval/self-rejection; counterpart attempts withdrawal; outsider attempts any response.

Expected: All invalid responses are rejected; pending proposal and money state are unchanged.

Rules: BR13, BR24.

### NEG11 - Dispute invalidates pending refund

Setup/action: Create a pending refund proposal, open a dispute, then submit a stale approval.

Expected: Proposal becomes INVALIDATED and dispute OPEN atomically; stale approval is rejected, no refund payout is started.

Rules: BR14, BR17.

### NEG12 - Concurrent Buyer release versus refund proposal

Setup/action: Issue Buyer acceptance/release and a refund proposal against DELIVERED concurrently.

Expected: Only one valid atomic gate wins. If proposal wins, release is blocked; if release wins, proposal is rejected and RELEASE_PENDING persists.

Rules: BR11, BR12, BR17.

### NEG13 - Concurrent release, refund approval and dispute

Setup/action: Create the valid starting condition for each pair: release/dispute without a proposal; refund-approval/dispute with a pending proposal; release/refund-approval with a pending proposal.

Expected: For release/dispute and refund-approval/dispute, exactly one eligible transition commits. With an existing pending proposal, ordinary release is already ineligible. No run accepts opposite payouts or opens a dispute after payout acceptance.

Rules: BR11, BR13, BR14, BR17.

### NEG14 - Conflicting Admin decisions

Setup/action: Two Admin requests concurrently resolve the same OPEN dispute in opposite directions.

Expected: Exactly one reasoned decision is recorded and one pending direction is accepted; stale opposite request is rejected.

Rules: BR16, BR17, BR20.

### NEG15 - Unknown payout result and controlled failed retry

Setup/action: For both payout directions, time out then request retry; separately obtain explicit failed/no-money confirmation and retry through A5.

Expected: Unknown result stays pending and is query-only. Confirmed failed attempt enables one controlled same-direction retry; original beneficiary, amount and decision remain fixed. Admin cannot mark success or switch payout direction.

Rules: BR18, BR19, BR20, BR22.

### NEG16 - Terminal and accepted-payout protection

Setup/action: At each pending/terminal payout state, attempt a new dispute, opposite payout, cancellation or refund proposal.

Expected: All such requests are rejected; the saved payout direction and final result cannot be reversed.

Rules: BR20, BR23.

### NEG17 - Merchant ownership and role separation

Setup/action: Use a valid Merchant client to create for an unbound Seller, query another Merchant's escrow, set owner fields or invoke participant/Admin actions.

Expected: Reject all out-of-scope calls without protected data/state changes; valid create/query for owned bound-Seller escrows remains available.

Rules: BR03, BR04, BR24.

### NEG18 - MFA failure and logout reuse

Setup/action: Try wrong/missing factors for user/Admin login, then reuse a session after logout.

Expected: No session on factor failure; post-logout protected request is rejected; no authentication secrets appear in logs.

Rules: BR03, BR25.

### NEG19 - Outsider and wrong participant access

Setup/action: Attempt view, funding, Seller acceptance/completion, evidence, refund response and Admin resolution using unauthorised identities.

Expected: Every action is checked against the required role and escrow ownership; no protected data or state mutation is exposed.

Rules: BR02, BR24, BR25.

### NEG20 - Policy change after creation

Setup/action: Create one GOODS and SERVICES escrow, change evidence settings as Admin, then create new escrows and execute the old/new delivery paths.

Expected: Old policy snapshots remain unchanged; only new escrows use changed evidence settings. No config value enables automatic release.

Rules: BR06, BR10, BR11.

### NEG21 - Evidence after resolution or second dispute

Setup/action: Resolve a dispute, then submit evidence or open another dispute; also attempt a decision without a reason.

Expected: All are rejected; resolved evidence/decision is retained and no second payout occurs.

Rules: BR14, BR15, BR16.

### NEG22 - Restart during provider wait

Setup/action: Interrupt each pending operation after provider submission and before local result handling; recover and reconcile.

Expected: State, provider reference, amount/destination, accepted decision and orthogonal records persist; reconciliation resolves without duplicate money movement.

Rules: BR18, BR19, BR21.

### NEG23 - Agreement self-trade and invalid amount

Setup/action: Create with same Buyer/Seller, zero/negative/fractional amount or non-VND currency; edit accepted terms.

Expected: Reject invalid create/edit; valid accepted agreement remains immutable.

Rules: BR01, BR02, BR04, BR05.

### NEG24 - Audit and analytics consistency

Setup/action: Inspect state transitions and dashboard after mixed pending/success/failure scenarios; attempt Admin audit edit/delete.

Expected: Dashboard matches observed mock records, pending differs from completed, audit is read-only and secret-free.

Rules: BR25, BR26.

## Non-functional acceptance

### Performance

| ID | Requirement | Acceptance criterion | Verification |
| --- | --- | --- | --- |
| NFR-P01 | Internal create/query response-time target. | Proposed, not measured: p95 <= 2 seconds for internal escrow create/query under 20 concurrent sessions and 1,000 simulated escrows. Exclude human interaction and external-provider wait; report the create and query samples and percentiles separately. | Run a documented demo workload with valid authorised requests, 20 sessions and a seeded set of 1,000 mock escrows; calculate p95 from recorded request durations. Do not claim a pass before running the workload. |
| NFR-P02 | Pending results are returned without waiting for a final transfer. | When a mock provider withholds its final result, the accepted operation is observable as the appropriate PENDING lifecycle with a query reference; no synchronous screen/API response falsely reports final success. | Withhold funding/release/refund completion and inspect the response plus subsequent query. |

### Operational

| ID | Requirement | Acceptance criterion | Verification |
| --- | --- | --- | --- |
| NFR-O01 | Recoverable pending operations. | After an interruption/restart between provider submission and result processing, every accepted pending operation retains its escrow, immutable decision, provider/attempt reference, amount, destination, policy snapshot, proposal and dispute state. Reconciliation can recover the provider outcome without a duplicate transfer. | Interrupt each of funding/release/refund after submission; restart, query and reconcile with the mock provider. |
| NFR-O02 | Unknown outcomes and failed attempts remain distinguishable. | For all three money operations, unknown outcomes offer query-only reconciliation. A retry is available only after explicit provider confirmation of failure with no money moved. Payout retry preserves direction and beneficiary; no manual-success control exists. | Inspect pending detail and exercise unknown, confirmed-failed and confirmed-success mock responses. |
| NFR-O03 | Traceable and internally consistent demo records. | Every accepted state-changing money action and reconciliation has an attributable audit event and correlation reference; dashboard counts/amounts agree with the underlying records at the stated observation time. | Replay the acceptance scenarios and reconcile state, held/pending/final totals and audit events. |

### Security

| ID | Requirement | Acceptance criterion | Verification |
| --- | --- | --- | --- |
| NFR-S01 | User MFA and session invalidation. | No active Buyer, Seller or Admin session is issued when either password or second-factor verification fails; logout makes the previous session unusable on the next protected request. | Exercise wrong password, absent/wrong second factor, successful MFA and logout/reuse cases. |
| NFR-S02 | Authorisation on every protected operation. | All protected use cases reject unauthenticated or wrong-role/wrong-escrow callers with no protected data or state changes. Merchant create/query is restricted to the authenticated client's ownership and bound Seller; Merchant cannot invoke participant/Admin actions. | Run each protected action as its owner, other participant where relevant, outsider, Merchant and non-Admin. |
| NFR-S03 | Authenticated protected channels and provider confirmations. | Use TLS for deployed HTTP channels; authenticate Merchant OAuth clients and provider confirmations. Tampered identity, amount, currency, operation, provider or attempt reference cannot establish HELD/RELEASED/REFUNDED. | Inspect channel configuration and submit unsigned, wrongly authenticated and mismatched mock callbacks. |
| NFR-S04 | Secret-free read-only audit access. | Audit access is read-only for Admin. Logs and audit views contain no passwords, MFA seeds/codes, access tokens or full client secrets; application users cannot edit/delete audit events. | Inspect representative authentication, API, provider and Admin audit records and attempt unauthorised mutations. |
| NFR-S05 | Atomic and idempotent money decisions. | In every specified duplicate/concurrency scenario, at most one full funding success and one terminal payout direction are accepted for an escrow; no duplicate provider transfer is submitted because of a repeated user request or callback. | Run concurrent release/refund/dispute and repeated callback/request scenarios using recorded provider operations. |

### Cultural and Political

| ID | Requirement | Acceptance criterion | Verification |
| --- | --- | --- | --- |
| NFR-C01 | Consistent VND and comprehensible terms. | All agreement, confirmation, provider and analytics amounts identify VND and use whole-VND values consistently. Before acceptance/funding, users can read the delivery/work, acceptance and evidence conditions applicable to that escrow. | Inspect GOODS and SERVICES scenarios through create, accept, fund, delivery and result views. |
| NFR-C02 | Privacy and simulation transparency. | The demo uses synthetic participant/payment data, labels funds and providers as simulated, and restricts personal and dispute evidence data to authorised participants/Admin. No output claims real-money custody or verified regulatory compliance. | Review demo data, participant/outsider access and wording throughout the Analysis and demonstration. |
| NFR-C03 | Planning legal claims are not treated as verified compliance. | Any legal/regulatory statements inherited from Planning are marked as unverified for real deployment. This Analysis makes no current-law conclusion; real-money rollout requires a separately sourced legal/regulatory review outside the MVP. | Review the chapter and alignment notes for unsupported legal assertions; do not treat a document review as a compliance certification. |

## Completion criteria

- FR01-FR12 have use-case, rule and diagram coverage; the same 22 codes and five groups are retained.
- Bank-only release and original-source refund hold for both funding methods.
- PENDING proposals freeze new delivery and ordinary release; a dispute invalidates the pending proposal.
- At most one dispute, one accepted payout direction and one final money outcome exist per escrow.
- Unknown is query-only; failed funding returns to Buyer control; failed payout keeps its reservation and permits only confirmed-failure same-direction retry.
- All 16 basic paths and 24 focused scenarios have explicit expected results and remain unexecuted until an implementation exists.
- Performance targets and legal statements are not presented as measured or certified findings.
