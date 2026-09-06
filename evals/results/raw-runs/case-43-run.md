# Case 43 — TowerPulse — Reviewer Run

[HIGH] POWER
Finding: No watchdog timer for on-device hang recovery
Evidence: Plan states explicitly the team "relied on the backhaul link's own periodic health-check polling to notice an unresponsive sensor and schedule a technician visit, rather than any on-device automatic hang recovery."
Risk: Detection via polling is not the same as recovery — a hung sensor still requires a technician visit regardless of how quickly it's noticed.
Recommended mitigation: Add an on-device hardware watchdog for automatic hang recovery, independent of backhaul polling for detection.
Confidence: HIGH
PatternID: P3

[HIGH] POWER
Finding: No remote, per-sensor power-cycle capability
Evidence: Plan states explicitly "there is also no remote power-cycle path for an individual sensor separate from the tower site's main equipment power, which is not something field technicians can toggle per-sensor."
Risk: Any hang not caught by a watchdog (see prior finding) requires a technician visit to isolate and recover a single sensor.
Recommended mitigation: Add a per-sensor remotely controllable power path, separate from main site equipment power.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
