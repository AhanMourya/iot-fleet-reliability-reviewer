# Case 89 — CartBot — Reviewer Run

[CRITICAL] SECURITY
Finding: Same factory-default administrative password shipped on every robot
Evidence: Plan states explicitly "every robot ships with the same factory-default administrative password for the local maintenance interface used by field technicians to service the robot's compartment lock and drive system, and operations staff have not established a per-unit or per-region rotation process."
Risk: A single leaked or guessed password compromises the maintenance interface — including compartment lock and drive system access — on any of 500 robots.
Recommended mitigation: Move to unique, per-robot passwords with a rotation process.
Confidence: HIGH
PatternID: S1

[HIGH] SECURITY
Finding: Continuously-active BLE diagnostic mode reachable by proximity
Evidence: Plan states the BLE diagnostic mode "stays continuously active (not just during active service sessions) and is reachable by anyone with a BLE-capable phone standing near the robot."
Risk: Anyone briefly near a robot could attempt to interact with the diagnostic interface, though exploitation requires physical proximity.
Recommended mitigation: Restrict BLE diagnostic mode to only be active during an explicitly initiated service session.
Confidence: HIGH
PatternID: S2

[CRITICAL] SECURITY
Finding: [COMPOUND] Proximity-reachable diagnostic mode combined with a universal factory-default password gives anyone near a robot a plausible path to tampering with its compartment lock or drive system
Evidence: Builds on the shared-password finding and the always-on BLE finding above.
Risk: Materially worse combination for physical tampering at 500-unit scale.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S2)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
