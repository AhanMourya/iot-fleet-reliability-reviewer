# Case 47 — WildWatch — Reviewer Run

[CRITICAL] SECURITY
Finding: Certificate shared across all sensors within an exhibit zone rather than unique per device
Evidence: Plan states explicitly "every unit deployed in a given exhibit zone... shares a single device certificate specific to that zone, rather than each sensor having its own unique certificate."
Risk: Extraction of the certificate from one sensor allows impersonating any sensor in that zone to backend services.
Recommended mitigation: Move to per-device unique certificates even within zone-based provisioning groups.
Confidence: HIGH
PatternID: S3

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
