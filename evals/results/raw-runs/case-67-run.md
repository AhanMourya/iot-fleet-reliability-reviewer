# Case 67 — HiveWatch — Reviewer Run

[CRITICAL] SECURITY
Finding: Certificate shared across all sensors at a given apiary location
Evidence: Plan states explicitly "every sensor deployed to a given apiary location shares a single device certificate specific to that location, rather than each sensor having its own unique certificate."
Risk: Extraction of the certificate from one sensor allows impersonating every sensor at that location to backend services.
Recommended mitigation: Move to per-sensor unique certificates even at this low per-unit cost point, or evaluate a lighter-weight per-device identity scheme if full PKI enrollment is genuinely too costly.
Confidence: HIGH
PatternID: S3

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
