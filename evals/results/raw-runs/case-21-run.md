# Case 21 — DeepGas — Reviewer Run

[CRITICAL] CONNECTIVITY
Finding: No reconnect/fallback logic described after initial session establishment
Evidence: Plan states the sensor "establishes its MQTT session and begins publishing" at startup, and explicitly notes the system "was designed around the assumption that the leaky-feeder link, once up, stays up for the shift," with underground radio propagation described as "inherently unstable."
Risk: A radio propagation disruption (explicitly acknowledged as plausible) is a fleet-wide-capable trigger with no automatic recovery — for a gas-detection safety system, sensors going dark with no reconnect is a serious operational and safety gap.
Recommended mitigation: Add automatic reconnect logic with backoff and jitter, rather than relying on the link staying continuously up.
Confidence: HIGH
PatternID: C1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
