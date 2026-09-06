# Case 42 — RailSentry — Reviewer Run

[CRITICAL] SECURITY
Finding: Single factory-default technician password shared across all trackside cabinets
Evidence: Plan states explicitly the maintenance terminal "uses a single default technician password set at the factory, which has not been rotated since installation."
Risk: A single leaked or guessed password compromises the maintenance terminal on any cabinet along the corridor — safety-relevant rail infrastructure.
Recommended mitigation: Move to unique per-cabinet passwords, or a centrally managed rotation process.
Confidence: HIGH
PatternID: S1

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states certificates are "issued at manufacturing for backend authentication" with "no expiry monitoring or renewal process."
Risk: On expiry, cabinets would simultaneously lose backend authentication with no remote recovery.
Recommended mitigation: Add expiry monitoring and automated renewal before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[CRITICAL] SECURITY
Finding: [COMPOUND] Shared default password combined with no certificate rotation leaves both trust anchors weak simultaneously on safety-relevant infrastructure
Evidence: Builds on the shared-password finding and the no-cert-rotation finding above.
Risk: A compromise of either weak point has direct safety implications for rail signaling.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S4)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
