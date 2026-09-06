# Case 40 — ArenaPulse — Reviewer Run

[HIGH] SECURITY
Finding: No mention of transport encryption for MQTT traffic
Evidence: Plan states data is published "via MQTT" with no mention of TLS either way.
Risk: If unencrypted, crowd-density data could be intercepted by anyone in a position on the venue network.
Recommended mitigation: Confirm and document that MQTTS/TLS is used for all device-to-cloud communication.
Confidence: LOW
PatternID: S5

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism beyond the routine publish interval
Evidence: No mention of a keep-alive interval or status/last-will mechanism distinct from the routine per-minute publish during events.
Risk: A wedged sensor could be indistinguishable from a healthy but quiet one until missing data is noticed during an event.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent) status topic.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 1 High, 1 Advisory (21 of 21 patterns checked; 19 showed no gap).
