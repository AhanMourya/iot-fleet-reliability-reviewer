# Case 16 — SiteTrack — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Client ID assignment described vaguely, with no confirmation of unique-hardware derivation
Evidence: Plan states client identifiers are "assigned during provisioning" without stating whether
they're derived from a guaranteed-unique hardware identifier or a sequentially assigned value from a
shared pool. The description is present but insufficient to verify uniqueness is actually enforced.
Risk: If IDs are not hardware-derived, colliding IDs across the 400-tag fleet would cause devices to
repeatedly disconnect each other, appearing as intermittent connectivity problems.
Recommended mitigation: Confirm and document that client IDs are derived from a unique hardware
identifier (e.g., a device serial or MAC address) rather than a sequential or shared-pool value.
Confidence: LOW
PatternID: C3

[HIGH] SECURITY
Finding: No mention of transport encryption for MQTT traffic
Evidence: Plan states location is published "via MQTT" with no mention of TLS/MQTTS either way.
Risk: If unencrypted, tracking data could be intercepted by anyone in a position on the network path.
Recommended mitigation: Confirm and document that MQTTS/TLS is used for all device-to-cloud communication.
Confidence: LOW
PatternID: S5

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
