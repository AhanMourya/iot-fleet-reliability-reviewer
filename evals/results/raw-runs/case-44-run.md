# Case 44 — CashWatch — Reviewer Run

[CRITICAL] OTA
Finding: No update image signature verification
Evidence: Plan states explicitly "there is no cryptographic signature verification of the firmware binary beyond the transport-level HTTPS connection."
Risk: A compromised internal distribution service or corrupted firmware would be applied to ATM monitoring units as if legitimate — direct financial and physical-security relevance.
Recommended mitigation: Add on-device signature verification of firmware binaries, independent of transport security.
Confidence: HIGH
PatternID: O2

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
