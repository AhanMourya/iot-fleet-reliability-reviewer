# Case 49 — RollShare — Reviewer Run

[CRITICAL] SECURITY
Finding: Same factory-default administrative password shipped on every unit
Evidence: Plan states explicitly "every unit ships with the same factory-default administrative password for the local maintenance interface... operations staff have not established a process to rotate it per-unit or per-region."
Risk: A single leaked or guessed password compromises the maintenance interface on any of 4,000 units.
Recommended mitigation: Move to unique, per-unit passwords with a rotation process.
Confidence: HIGH
PatternID: S1

[HIGH] SECURITY
Finding: Continuously-active BLE diagnostic mode reachable by proximity
Evidence: Plan states the BLE diagnostic mode "stays continuously active (not just during active service sessions) and is reachable by anyone with a BLE-capable phone standing near the unit."
Risk: Anyone briefly near a unit could attempt to interact with the diagnostic interface, though exploitation requires physical proximity.
Recommended mitigation: Restrict BLE diagnostic mode to only be active during an explicitly initiated service session.
Confidence: HIGH
PatternID: S2

[CRITICAL] SECURITY
Finding: [COMPOUND] Proximity-reachable diagnostic mode combined with a universal factory-default password gives anyone near a unit a plausible tampering path
Evidence: Builds on the shared-password finding and the always-on BLE finding above.
Risk: Materially worse combination for lock/mechanical tampering at fleet scale.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S2)

Findings: 3 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 17 showed no gap).
