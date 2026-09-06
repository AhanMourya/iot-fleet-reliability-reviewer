# Case 07 — RouteTrack — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate rotation/renewal process for a multi-year deployment
Evidence: Plan states units are issued a certificate "at manufacturing" with no mention of any renewal or rotation process over the vehicle's expected multi-year service life.
Risk: Units from the same manufacturing run would likely approach expiry around the same time, simultaneously losing backend authentication with no remote recovery if the update channel depends on the same cert.
Recommended mitigation: Add expiry monitoring and an automated renewal process well before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[HIGH] SECURITY
Finding: No mention of a reliable time source for certificate validation
Evidence: Plan explicitly states it "doesn't mention whether the unit has a battery-backed RTC or relies on GPS/NTP time sync after each power cycle."
Risk: A unit that loses power could boot with an incorrect clock and fail certificate validation until time sync completes.
Recommended mitigation: Confirm and, if needed, add a battery-backed RTC or a trusted early time-sync step.
Confidence: MEDIUM
PatternID: S6

[CRITICAL] SECURITY
Finding: [COMPOUND] Certificate expiry with no rotation, combined with no confirmed reliable clock, compounds recovery difficulty after a power event near expiry
Evidence: Builds on the no-rotation finding and the no-time-source finding above.
Risk: A unit losing power near its certificate's expiry could face both an ambiguous clock state and an already-invalid certificate, with no remote path to fix either.
Recommended mitigation: Address certificate rotation and a reliable time source together.
Confidence: MEDIUM
PatternID: COMPOUND(S4,S6)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
