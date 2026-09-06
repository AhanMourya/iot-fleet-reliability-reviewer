# Case 17 — FallAlert — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states each device has "a unique certificate issued at provisioning" but "does not describe any process for monitoring certificate expiry or renewing certificates before they lapse."
Risk: On expiry, devices would simultaneously lose backend authentication with no remote recovery path; for a fall-detection use case, a silent authentication outage is a materially different risk profile than for routine telemetry.
Recommended mitigation: Add expiry monitoring and automated renewal well before certificates approach their validity window's end, given the safety-critical nature of this deployment.
Confidence: HIGH
PatternID: S4

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
