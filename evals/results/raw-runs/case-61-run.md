# Case 61 — CleanRoomX — Reviewer Run

[CRITICAL] CONNECTIVITY
Finding: No reconnect/fallback logic described after initial session establishment
Evidence: Plan states the sensor "establishes its MQTT session and begins publishing" at startup, and explicitly notes "the facilities team has historically treated the fab's internal network as effectively always-up and didn't design for a mid-shift reconnect scenario."
Risk: Any network blip is a fleet-wide-capable trigger with no automatic recovery; for cleanroom process-control sensing, a gap in particle-count monitoring has direct yield/quality implications.
Recommended mitigation: Add automatic reconnect logic with backoff and jitter, rather than assuming continuous network availability.
Confidence: HIGH
PatternID: C1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
