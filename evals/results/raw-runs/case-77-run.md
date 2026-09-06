# Case 77 — PaveMix — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Client ID assignment described vaguely, without confirming unique-hardware derivation
Evidence: Plan states client identifiers are "assigned when each sensor is commissioned," without stating whether they're derived from a unique hardware identifier.
Risk: If not hardware-derived, colliding IDs could cause sensors to disconnect each other.
Recommended mitigation: Confirm and document that client IDs are derived from a unique hardware identifier.
Confidence: LOW
PatternID: C3

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism beyond the routine publish interval
Evidence: No mention of a keep-alive interval or status/last-will mechanism distinct from the routine 30-second publish during production.
Risk: A wedged sensor could be indistinguishable from a healthy but quiet one until missing data is noticed.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent) status topic.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 1 High, 1 Advisory (21 of 21 patterns checked; 19 showed no gap).
