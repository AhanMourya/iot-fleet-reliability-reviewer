# Case 35 — ShelfTrace — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Client ID assignment described vaguely, without confirming unique-hardware derivation
Evidence: Plan states client/connection identifiers are "configured per branch during setup," without stating whether they're derived from a unique hardware identifier or assigned from a shared per-branch pool.
Risk: If IDs are not hardware-derived, colliding IDs within a branch could cause readers to disconnect each other.
Recommended mitigation: Confirm and document that client IDs are derived from a unique hardware identifier.
Confidence: LOW
PatternID: C3

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism beyond the routine publish interval
Evidence: No mention of a keep-alive interval or status/last-will mechanism distinct from routine publishing.
Risk: A wedged reader could be indistinguishable from a healthy but quiet one until missing scan data is noticed.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent) status topic.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 1 High, 1 Advisory (21 of 21 patterns checked; 19 showed no gap).
