# Case 22 — PipeWatch — Reviewer Run

[CRITICAL] SECURITY
Finding: Single factory-set default password shared across all diagnostic ports
Evidence: Plan states "each unit's local diagnostic port uses a single default password set at the factory, which the commissioning team has generally not rotated."
Risk: A single leaked or guessed password compromises the diagnostic interface on any of the 400 units.
Recommended mitigation: Move to unique per-unit passwords, or a centrally managed credential rotation process even for hard-to-access remote units.
Confidence: HIGH
PatternID: S1

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states certificates are "issued at manufacturing for backend authentication" with "no expiry monitoring or renewal process."
Risk: On expiry, units would simultaneously lose backend authentication with no remote recovery if the update channel depends on the same cert.
Recommended mitigation: Add expiry monitoring and automated renewal before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[CRITICAL] SECURITY
Finding: [COMPOUND] Shared diagnostic credential combined with no certificate rotation leaves both trust anchors weak simultaneously
Evidence: Builds on the shared-password finding and the no-cert-rotation finding above.
Risk: On safety-relevant pipeline infrastructure, both the human-facing and machine-facing trust mechanisms are weak at the same time.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S4)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
