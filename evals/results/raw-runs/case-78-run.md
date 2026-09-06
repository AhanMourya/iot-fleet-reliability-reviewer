# Case 78 — ReelOps — Reviewer Run

[HIGH] POWER
Finding: No remote power-cycle mechanism for booth sensors
Evidence: Plan states explicitly there is "no remote power-cycle mechanism for these sensors," because "projector booth equipment sits on a separate electrical subpanel that theater staff have chosen not to network for power control." That operational choice explains the gap; it does not close it — the capability is still absent.
Risk: Any sensor hang not caught by the watchdog requires a staff member to physically reset it during a booth check, rather than being resolved remotely.
Recommended mitigation: Revisit networking the booth subpanel for power control, or accept and explicitly document the resulting recovery-time trade-off.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
