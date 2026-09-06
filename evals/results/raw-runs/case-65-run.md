# Case 65 — TollFlow — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Fixed 2-second reconnect interval with no backoff or jitter
Evidence: Plan states sensors retry "immediately and continuously on a fixed 2-second interval with no increasing delay."
Risk: A fiber/cellular backup failover event affecting multiple gantries could trigger a reconnect storm at the moment of recovery.
Recommended mitigation: Add exponential backoff with jitter to the reconnect logic.
Confidence: HIGH
PatternID: C2

[HIGH] CONNECTIVITY
Finding: No local buffering of toll events generated while disconnected
Evidence: Plan states explicitly the sensor "simply resumes normal reporting once reconnected, with no mention of what happens to vehicle-passage events missed during the outage window."
Risk: Missed toll events during an outage are permanently lost, with direct revenue and enforcement implications.
Recommended mitigation: Add a bounded local buffer of toll events with overflow alerting.
Confidence: HIGH
PatternID: C4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
