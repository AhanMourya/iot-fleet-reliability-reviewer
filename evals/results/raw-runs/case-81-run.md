# Case 81 — MileFlow — Reviewer Run

[CRITICAL] CONNECTIVITY
Finding: No reconnect/fallback logic described after initial session establishment
Evidence: Plan states the dongle "establishes its MQTT session and begins publishing" at startup, and explicitly notes "the team assumed cellular coverage would be continuous for the vast majority of trips and didn't design a reconnect path for the remainder."
Risk: A coverage gap mid-trip is a fleet-wide-capable trigger with no automatic recovery, directly affecting usage-based billing data accuracy.
Recommended mitigation: Add automatic reconnect logic with backoff and jitter, since the team already acknowledges coverage gaps occur.
Confidence: HIGH
PatternID: C1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
