# Case 58 — LiftGuard — Reviewer Run

[HIGH] POWER
Finding: No remote power-cycle capability for elevator/escalator sensors
Evidence: Plan states explicitly "there is no remote power-cycle path for these sensors," citing that "machine rooms are generally not remotely accessible for power control due to elevator safety code restrictions on remote actuation of machine room equipment." That's a legitimate regulatory constraint explaining why the gap exists, but it doesn't change whether the capability itself is present — it isn't, so this is scored as a finding rather than excused by the explanation.
Risk: Any sensor hang not caught by the watchdog requires a technician visit during a scheduled maintenance window to recover, with no faster remote fallback available given the code restriction.
Recommended mitigation: This gap may not be closeable given the regulatory constraint — the practical mitigation is likely to strengthen watchdog/reset-loop coverage (already present) to minimize reliance on remote power-cycling, and to document the accepted residual recovery-time risk explicitly rather than leaving it implicit.
Confidence: HIGH
PatternID: P4

Findings: 0 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
