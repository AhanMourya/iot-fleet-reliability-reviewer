# Case 05 — ShelfSense — Reviewer Run

[CRITICAL] OTA
Finding: No update image signature verification
Evidence: Plan states explicitly: "we rely on the download being over a trusted, encrypted connection and haven't added a separate cryptographic signature check on the firmware binary itself."
Risk: A compromised build or corrupted download would be applied to devices as if legitimate, across up to 2,000 units.
Recommended mitigation: Add on-device signature verification of firmware binaries before applying.
Confidence: HIGH
PatternID: O2

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
