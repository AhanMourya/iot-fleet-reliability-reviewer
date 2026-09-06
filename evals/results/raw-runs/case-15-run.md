# Case 15 — BuoyNet — Reviewer Run

[HIGH] POWER
Finding: No remote power-cycle capability offshore
Evidence: Plan states explicitly there's "no remote power-cycle path given the offshore deployment," despite noting watchdog coverage is expected to handle most hangs based on bench testing.
Risk: Any hang class the watchdog doesn't catch requires a vessel trip to the buoy's location.
Recommended mitigation: The compensating rationale (watchdog coverage) doesn't substitute for this capability gap — consider a satellite-triggered remote reset option, or explicitly accept this as a documented residual risk.
Confidence: HIGH
PatternID: P4

[HIGH] POWER
Finding: No reset-loop detection or escalation described
Evidence: No mention of reset-count tracking or an escalation path if the watchdog resets a buoy repeatedly in a short window.
Risk: A persistent bad state could cause repeated resets that look like intermittent connectivity rather than an alertable failure.
Recommended mitigation: Add reset-count tracking with an alert after N resets in a defined window.
Confidence: MEDIUM
PatternID: P5

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
