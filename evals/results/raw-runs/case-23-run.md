# Case 23 — AGVFleet — Reviewer Run

[HIGH] POWER
Finding: No watchdog timer for on-device hang recovery
Evidence: Plan states explicitly the team "relied on the coordination server noticing a vehicle has stopped reporting telemetry and flagging it for manual review, rather than automatic on-device hang recovery."
Risk: A hung vehicle is detected but not automatically recovered — it still requires manual intervention to resolve.
Recommended mitigation: Add an on-device hardware watchdog for automatic hang recovery, complementing (not replacing) the coordination server's detection.
Confidence: HIGH
PatternID: P3

Findings: 0 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
