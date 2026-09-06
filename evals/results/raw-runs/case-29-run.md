# Case 29 — WindVane — Reviewer Run

[HIGH] POWER
Finding: No filesystem write-protection described
Evidence: No mention of read-only root, overlay, or equivalent write protection for local storage; sensors are powered from the turbine's nacelle electronics bus with no stated protection against an unclean power event.
Risk: A power interruption on the nacelle bus could corrupt local storage, requiring a multi-hour, weather-dependent nacelle climb to physically service.
Recommended mitigation: Convert the root filesystem to read-only with an overlay for writable paths.
Confidence: MEDIUM
PatternID: P1

[HIGH] POWER
Finding: No remote power-cycle capability
Evidence: Plan states explicitly "no remote power-cycle capability described as a fallback," and that physical access requires a "multi-hour, weather-dependent" climb.
Risk: Any hang not caught by the watchdog requires an unusually costly physical service trip.
Recommended mitigation: Given the access cost, prioritize a remote-triggerable reset mechanism (even a simple relay) over relying on watchdog coverage alone.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 2 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
