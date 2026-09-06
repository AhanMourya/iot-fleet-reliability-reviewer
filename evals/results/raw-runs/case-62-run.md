# Case 62 — SiloGuard — Reviewer Run

[CRITICAL] SECURITY
Finding: Single default password from a standard configuration image, unrotated across the network
Evidence: Plan states explicitly the sensor hub "uses a single default password set at installation, which has not been rotated across the network because the installing contractor used one standard configuration image for all sites."
Risk: A single leaked or guessed password compromises the diagnostic interface at any silo site; grain storage CO2/moisture sensing has real safety relevance.
Recommended mitigation: Move to unique per-site passwords, or a centrally managed rotation process, even when sites share a base configuration image.
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
Risk: Both the human-facing and machine-facing trust mechanisms are weak at the same time across the sensor network.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S4)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
