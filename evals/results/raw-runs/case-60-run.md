# Case 60 — BrewBot — Reviewer Run

[HIGH] SECURITY
Finding: No mention of transport encryption for MQTT traffic
Evidence: Plan states telemetry is published "via MQTT" with no mention of TLS either way.
Risk: If unencrypted, vending telemetry (which may include payment-adjacent transaction counts) could be intercepted by anyone in a position on the network path.
Recommended mitigation: Confirm and document that MQTTS/TLS is used for all device-to-cloud communication.
Confidence: LOW
PatternID: S5

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism beyond the routine publish interval
Evidence: No mention of a keep-alive interval or status/last-will mechanism distinct from the routine 10-minute publish.
Risk: A wedged unit could be indistinguishable from a healthy but quiet one until missing telemetry is noticed.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent) status topic.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 1 High, 1 Advisory (21 of 21 patterns checked; 19 showed no gap).
