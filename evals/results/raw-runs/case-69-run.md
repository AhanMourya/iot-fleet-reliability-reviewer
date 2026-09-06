# Case 69 — SortLine — Reviewer Run

[CRITICAL] SECURITY
Finding: Same factory-default password kept unchanged across all 320 diagnostic interfaces
Evidence: Plan states explicitly "every sensor's local diagnostic interface uses the same default password set at the factory, which the maintenance team has kept unchanged because a single memorized password made shift-to-shift troubleshooting simpler."
Risk: A single leaked or guessed password compromises the diagnostic interface on any of 320 sensors.
Recommended mitigation: Move to unique per-sensor passwords or a centrally managed credential vault accessible per-shift without requiring a single shared secret.
Confidence: HIGH
PatternID: S1

[CRITICAL] SECURITY
Finding: Telnet service enabled continuously and reachable via a routed path to the internet
Evidence: Plan states explicitly the Telnet service "stays enabled continuously and is reachable from the facility's general IT network, which itself has a routed (non-isolated) path to the corporate network and, from there, the internet."
Risk: This is confirmed internet-reachable exposure of an unauthenticated-by-default remote access service, even though the path is indirect via IT network routing rather than a direct port-forward.
Recommended mitigation: Disable Telnet by default, isolate the facility's OT network from the routed corporate/internet path, or both.
Confidence: HIGH
PatternID: S2

[CRITICAL] SECURITY
Finding: [COMPOUND] Internet-reachable Telnet combined with a shared, unrotated password closely mirrors the Mirai attack pattern
Evidence: Builds on the shared-password finding and the internet-reachable-Telnet finding above.
Risk: Remote, automatable compromise potential across facility infrastructure that could disrupt package sortation at scale.
Recommended mitigation: Prioritize disabling default Telnet exposure and moving to unique credentials together.
Confidence: HIGH
PatternID: COMPOUND(S1,S2)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
