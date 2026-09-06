# Case 08 — HomeGuard — Reviewer Run

[CRITICAL] SECURITY
Finding: Same factory-set administrator password shipped on every unit
Evidence: Plan states explicitly: "the same factory-set administrator password for its local setup web UI... we don't currently prompt customers to change after setup completes."
Risk: A single leaked or guessed password compromises the setup UI on every one of 5,000 units.
Recommended mitigation: Require a mandatory password change during setup, generating a unique credential per unit.
Confidence: HIGH
PatternID: S1

[CRITICAL] SECURITY
Finding: Telnet enabled by default and commonly reachable from the internet
Evidence: Plan states explicitly: "we also leave a Telnet service enabled on the base station by default... this is reachable from the internet since customers' home routers commonly forward the relevant port automatically via UPnP."
Risk: Confirmed internet-facing exposure of an unauthenticated-by-default remote access service across the fleet.
Recommended mitigation: Disable Telnet by default; if remote support access is needed, use an outbound-initiated, authenticated channel instead of an inbound-reachable service.
Confidence: HIGH
PatternID: S2

[CRITICAL] SECURITY
Finding: [COMPOUND] Internet-reachable Telnet combined with a shared, unrotated password closely matches the Mirai attack pattern
Evidence: Builds on the shared-password finding and the internet-reachable-Telnet finding above.
Risk: Remote, automatable, fleet-wide compromise potential.
Recommended mitigation: Prioritize disabling default Telnet exposure and moving to unique credentials together.
Confidence: HIGH
PatternID: COMPOUND(S1,S2)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
