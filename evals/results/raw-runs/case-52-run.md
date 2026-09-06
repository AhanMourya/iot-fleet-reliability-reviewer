# Case 52 — MedTrack — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states each tag has "a unique certificate issued at provisioning" but "does not describe any process for monitoring certificate expiry or renewing certificates before they lapse."
Risk: On expiry, tags would simultaneously lose backend authentication, disrupting equipment tracking across the hospital system.
Recommended mitigation: Add expiry monitoring and automated renewal well before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
