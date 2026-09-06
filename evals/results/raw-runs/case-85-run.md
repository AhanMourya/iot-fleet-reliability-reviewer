# Case 85 — SkyLink — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Fixed 1-second reconnect interval with no backoff or jitter
Evidence: Plan states sensors retry "immediately and continuously on a fixed 1-second interval with no increasing delay."
Risk: A lift-wide network event could trigger a reconnect storm across sensors at the moment of recovery.
Recommended mitigation: Add exponential backoff with jitter to the reconnect logic.
Confidence: HIGH
PatternID: C2

[HIGH] CONNECTIVITY
Finding: No local buffering of tension/status readings generated while disconnected
Evidence: Plan states explicitly the sensor "simply resumes normal reporting once reconnected, with no mention of what happens to the specific readings missed during the outage."
Risk: Missed safety-relevant tension/status readings during an outage are permanently lost, on a passenger-carrying cable transport system.
Recommended mitigation: Add a bounded local buffer of readings with overflow alerting.
Confidence: HIGH
PatternID: C4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
