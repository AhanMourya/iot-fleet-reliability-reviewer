# Case 82 — FlowGuard — Reviewer Run

[CRITICAL] SECURITY
Finding: Single factory-default password unrotated across all diagnostic ports
Evidence: Plan states explicitly "each sensor's local diagnostic port uses a single default password set at the factory, which the utility's maintenance contractor has not rotated because coordinating unique passwords across 550 remote valve-pit locations was judged impractical."
Risk: A single leaked or guessed password compromises the diagnostic interface at any valve-pit location — public water infrastructure.
Recommended mitigation: Move to unique per-site passwords or a centrally managed rotation process, even across remote locations.
Confidence: HIGH
PatternID: S1

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states certificates are "issued at manufacturing" with "no expiry monitoring or renewal process."
Risk: On expiry, sensors would simultaneously lose backend authentication with no remote recovery.
Recommended mitigation: Add expiry monitoring and automated renewal before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[CRITICAL] SECURITY
Finding: [COMPOUND] Shared default password combined with no certificate rotation leaves both trust anchors weak simultaneously
Evidence: Builds on the shared-password finding and the no-cert-rotation finding above.
Risk: Both trust mechanisms weak at the same time on public-safety-relevant infrastructure.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S4)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
