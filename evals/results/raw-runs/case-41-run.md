# Case 41 — GroundLink — Reviewer Run

[CRITICAL] CONNECTIVITY
Finding: No reconnect/fallback logic described after initial session establishment
Evidence: Plan states the unit "establishes its MQTT session and begins publishing" at startup, and explicitly acknowledges "the tarmac's WiFi coverage has known dead zones near certain gates," with no described behavior for re-establishing the session after a vehicle moves out of and back into coverage.
Risk: A known, routine coverage gap is a fleet-wide-capable trigger (any vehicle passing near an affected gate) with no automatic recovery, leaving vehicles dark until manually restarted.
Recommended mitigation: Add automatic reconnect logic with backoff and jitter, since coverage gaps are an acknowledged normal operating condition, not a rare edge case.
Confidence: HIGH
PatternID: C1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
