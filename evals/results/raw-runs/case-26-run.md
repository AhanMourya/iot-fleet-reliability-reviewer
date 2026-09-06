# Case 26 — ClearFlow — Reviewer Run

[CRITICAL] OTA
Finding: No update image signature verification
Evidence: Plan states explicitly the update pipeline "retrieves new firmware over an internally-hosted HTTPS endpoint and applies it directly; there is currently no cryptographic signature check on the firmware binary itself beyond the transport-level HTTPS connection."
Risk: A compromised internal build/hosting source or corrupted transfer would be applied to plant sensors as if legitimate, on infrastructure with public-health-relevant sensing.
Recommended mitigation: Add on-device signature verification of firmware binaries, independent of transport security.
Confidence: HIGH
PatternID: O2

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
