# Case 64 — TableWatch — Reviewer Run

[CRITICAL] OTA
Finding: No update image signature verification
Evidence: Plan states explicitly "there is no cryptographic signature check on the firmware binary itself beyond the transport-level HTTPS connection."
Risk: A compromised internal distribution point or corrupted firmware would be applied to gaming-floor sensors as if legitimate — direct financial-integrity relevance.
Recommended mitigation: Add on-device signature verification of firmware binaries, independent of transport security.
Confidence: HIGH
PatternID: O2

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
