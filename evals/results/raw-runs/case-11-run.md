# Case 11 — AquaSense — Reviewer Run

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism beyond the routine publish interval
Evidence: No mention of a keep-alive interval or status/last-will mechanism distinct from the 5-minute routine publish.
Risk: A wedged device could be indistinguishable from a healthy but quiet one until missing data is noticed.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent) status topic.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 0 High, 1 Advisory (21 of 21 patterns checked; 20 showed no gap).
