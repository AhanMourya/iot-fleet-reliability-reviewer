# Case 20 — TransitCount — Reviewer Run

[HIGH] OTA
Finding: Post-update health check has no defined timeout
Evidence: Plan states a health check exists ("verifies network reachability and a service heartbeat") but "doesn't specify a timeout for that check."
Risk: A hung (not crashed) device post-update could sit un-rolled-back indefinitely since the check never resolves to a failure state.
Recommended mitigation: Define an explicit timeout on the post-update health check that triggers rollback if exceeded.
Confidence: HIGH
PatternID: O4

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism during normal (non-update) operation
Evidence: Plan describes a heartbeat only in the context of the post-update health check; "no device status/heartbeat mechanism during normal operation beyond the routine 3-minute publish" is stated explicitly.
Risk: A wedged device outside update windows could be indistinguishable from a healthy but quiet one.
Recommended mitigation: Extend the existing heartbeat mechanism to continuous runtime operation.
Confidence: LOW
PatternID: C5

Findings: 0 Critical, 1 High, 1 Advisory (21 of 21 patterns checked; 19 showed no gap).
