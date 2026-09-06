# Case 24 — SkyDrop — Reviewer Run

[CRITICAL] OTA
Finding: No rollback or A/B fallback path for flight-control firmware
Evidence: Plan states firmware is written "directly to the active flash partition" with "no secondary partition to fall back to if the new firmware fails to pass its post-update self-test."
Risk: A bad nightly firmware push grounds affected drones with no remote recovery, requiring a technician to manually reflash before the drone can fly again.
Recommended mitigation: Add A/B partitioning with automatic rollback triggered by the existing post-update self-test.
Confidence: HIGH
PatternID: O1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
