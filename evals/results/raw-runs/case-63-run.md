# Case 63 — ServiceVan — Reviewer Run

[HIGH] POWER
Finding: No watchdog timer for on-device hang recovery
Evidence: Plan states explicitly the dispatch team "relied on noticing a van's unit has stopped reporting and calling the technician to check on it," with no on-device automatic hang recovery.
Risk: Detection by dispatch is not the same as recovery — a hung unit still requires a technician to intervene.
Recommended mitigation: Add an on-device hardware watchdog for automatic hang recovery.
Confidence: HIGH
PatternID: P3

[HIGH] POWER
Finding: No remote power-cycle mechanism
Evidence: Plan states explicitly "recovering a hung unit currently means a technician manually unplugging and replugging it from the vehicle's accessory power."
Risk: Any hang not caught by a watchdog (see prior finding) requires manual physical intervention by a technician.
Recommended mitigation: Add a remotely triggerable power relay for the unit, independent of manual accessory-power unplugging.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
