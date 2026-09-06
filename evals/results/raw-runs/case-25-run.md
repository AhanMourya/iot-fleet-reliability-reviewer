# Case 25 — PortContain — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Fixed 2-second reconnect interval with no backoff or jitter
Evidence: Plan states devices retry "immediately and continuously on a fixed 2-second interval with no increasing delay."
Risk: A satellite constellation or regional cellular outage affecting many containers at once could trigger uncoordinated simultaneous reconnect storms.
Recommended mitigation: Add exponential backoff with jitter to the reconnect logic.
Confidence: HIGH
PatternID: C2

[HIGH] CONNECTIVITY
Finding: No local buffering for data generated while disconnected
Evidence: Plan states explicitly readings are not stored locally, and notes multi-week ocean transits without connectivity are the normal operating mode, not an edge case.
Risk: Given that offline periods are routine and lengthy rather than rare, this is a substantial, expected, ongoing data-loss condition for most container journeys.
Recommended mitigation: Add a bounded local buffer sized for typical transit duration, with overflow alerting.
Confidence: HIGH
PatternID: C4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
