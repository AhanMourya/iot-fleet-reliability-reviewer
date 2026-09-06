# Case 45 — GarageWatch — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Fixed 1-second reconnect interval with no backoff or jitter
Evidence: Plan states sensors retry "immediately and continuously on a fixed 1-second interval with no increasing delay."
Risk: A garage-wide mesh outage could trigger a reconnect storm across many sensors at once when connectivity returns.
Recommended mitigation: Add exponential backoff with jitter to the reconnect logic.
Confidence: HIGH
PatternID: C2

[HIGH] CONNECTIVITY
Finding: No local buffering of state-change events generated while disconnected
Evidence: Plan states explicitly the sensor "simply reports its current state once reconnected, with no mention of what happens to the specific transition events missed during the outage."
Risk: Occupancy transitions during an outage are permanently lost rather than delayed, degrading data accuracy for billing/availability displays.
Recommended mitigation: Add a bounded local buffer of state-change events with overflow alerting.
Confidence: HIGH
PatternID: C4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
