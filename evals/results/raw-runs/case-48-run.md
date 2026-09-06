# Case 48 — RentalFleet — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate rotation/renewal process for a multi-year fleet deployment
Evidence: Plan states units are issued a certificate "at installation" with "no renewal process" described "over the vehicle's multi-year service life in the fleet."
Risk: Units installed in the same batch would likely approach expiry together, simultaneously losing backend authentication.
Recommended mitigation: Add expiry monitoring and automated renewal before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[HIGH] SECURITY
Finding: No confirmed reliable time source, with routine power interruptions
Evidence: Plan states explicitly it "does not state whether the unit has a battery-backed RTC or depends on GPS/NTP time sync following each power interruption (routine, given vehicles are frequently switched off)."
Risk: Every routine power-off is a potential trigger for a clock-validation failure if no RTC is present, not a rare event.
Recommended mitigation: Confirm and, if needed, add a battery-backed RTC given how routine power interruptions are for this fleet.
Confidence: MEDIUM
PatternID: S6

[CRITICAL] SECURITY
Finding: [COMPOUND] Certificate expiry with no rotation, combined with routine power interruptions and unconfirmed clock reliability, compounds recovery difficulty
Evidence: Builds on the no-rotation finding and the no-confirmed-time-source finding above.
Risk: A vehicle switched off near a certificate's expiry could return with both an ambiguous clock state and an expiring/expired cert.
Recommended mitigation: Address certificate rotation and a reliable time source together.
Confidence: MEDIUM
PatternID: COMPOUND(S4,S6)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
