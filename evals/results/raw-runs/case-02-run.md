# Case 02 — UrbanPark — Reviewer Run

[CRITICAL] CONNECTIVITY
Finding: No reconnect/fallback logic described after initial connection
Evidence: Plan states the device "establishes its MQTT session and begins publishing" at startup, and explicitly notes "the plan does not describe any behavior for what happens if that session drops after startup."
Risk: A mesh-wide outage (a single common trigger across the district) would leave sensors permanently disconnected with no automatic recovery, requiring physical service per unit.
Recommended mitigation: Add automatic reconnect logic with backoff and jitter, distinct from the initial connection-establishment step.
Confidence: HIGH
PatternID: C1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
