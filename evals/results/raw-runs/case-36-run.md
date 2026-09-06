# Case 36 — ColdCure — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate expiry monitoring or renewal process
Evidence: Plan states each sensor has "a unique certificate issued at installation" but "does not describe any process for monitoring certificate expiry or renewing certificates before they lapse."
Risk: On expiry, sensors would simultaneously lose backend authentication — for pharmaceutical cold-chain compliance monitoring, a silent authentication outage has direct regulatory and product-safety consequences.
Recommended mitigation: Add expiry monitoring and automated renewal well before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
