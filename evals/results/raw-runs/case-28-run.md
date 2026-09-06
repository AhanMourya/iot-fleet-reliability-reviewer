# Case 28 — StayGuard — Reviewer Run

[CRITICAL] SECURITY
Finding: Same factory-default maintenance PIN shipped on every lock
Evidence: Plan states explicitly: "the same 4-digit code shipped on every lock from the factory... properties have generally kept the factory default rather than setting a property-specific code."
Risk: A single known PIN compromises maintenance-mode override on any of 8,000 locks — a physical room-access security failure at fleet scale.
Recommended mitigation: Require a property-specific PIN to be set during installation, and disable the factory default once a property-specific code is configured.
Confidence: HIGH
PatternID: S1

[HIGH] SECURITY
Finding: Continuously-active BLE diagnostic pairing mode reachable by proximity
Evidence: Plan states the BLE diagnostic pairing mode "stays active continuously rather than only during an active maintenance session, and is reachable by anyone with a BLE-capable phone standing near the door."
Risk: Anyone briefly near a door could attempt to interact with the diagnostic interface, though exploitation requires physical proximity rather than being remotely reachable.
Recommended mitigation: Restrict BLE pairing mode to only be active during an explicitly initiated maintenance session.
Confidence: HIGH
PatternID: S2

[CRITICAL] SECURITY
Finding: [COMPOUND] Proximity-reachable diagnostic interface combined with a universal factory-default override PIN gives a plausible override path to anyone briefly near a door
Evidence: Builds on the shared-PIN finding and the always-on BLE finding above.
Risk: Materially worse combination for a physical-security product than either finding alone.
Recommended mitigation: Prioritize both fixes together.
Confidence: HIGH
PatternID: COMPOUND(S1,S2)

Findings: 3 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 17 showed no gap).
