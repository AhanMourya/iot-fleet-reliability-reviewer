# Case 87 — MethSense — Reviewer Run

[CRITICAL] SECURITY
Finding: Certificate shared across all sensors within a landfill cell
Evidence: Plan states explicitly "every sensor deployed to a given landfill cell shares a single device certificate specific to that cell, rather than each sensor having its own unique certificate."
Risk: Extraction of the certificate from one sensor allows impersonating every sensor in that cell to backend services, on a gas-detection safety system.
Recommended mitigation: Move to per-sensor unique certificates even within cell-based provisioning groups.
Confidence: HIGH
PatternID: S3

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
