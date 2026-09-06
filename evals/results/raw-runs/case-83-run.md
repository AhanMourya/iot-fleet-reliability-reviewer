# Case 83 — MedResponse — Reviewer Run

[HIGH] POWER
Finding: No watchdog timer for on-device hang recovery
Evidence: Plan states dispatch "relied on noticing a unit has stopped reporting and radioing the crew to check on it manually," with no on-device automatic hang recovery.
Risk: Detection via dispatch is not the same as recovery — a hung unit still requires crew intervention.
Recommended mitigation: Add an on-device hardware watchdog for automatic hang recovery.
Confidence: HIGH
PatternID: P3

[HIGH] POWER
Finding: No remote power-cycle mechanism
Evidence: Plan states explicitly "recovering a hung unit requires a crew member to manually power-cycle it, which during an active call is not always immediately practical."
Risk: Any hang not caught by a watchdog requires manual intervention that may be delayed during active EMS calls.
Recommended mitigation: Add a remotely triggerable power relay for the unit, independent of crew manual intervention.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
