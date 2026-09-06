# Case 04 — FactoryVibe — Reviewer Run

[HIGH] POWER
Finding: No watchdog or hang-detection mechanism described
Evidence: No mention of a hardware or software watchdog anywhere in the plan.
Risk: A software hang on any sensor requires physical access to the machine to power-cycle it.
Recommended mitigation: Enable a hardware watchdog timer on the sensor MCU.
Confidence: HIGH
PatternID: P3

[HIGH] POWER
Finding: No remote power-cycle capability described
Evidence: Plan states explicitly that recovering a hung unit "would require a technician to physically access the machine and power-cycle the sensor at the panel."
Risk: Any hang has no remote fallback, costing a technician visit per incident.
Recommended mitigation: Add a remotely controllable power path (e.g., via the edge gateway) for sensors.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
