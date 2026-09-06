# Case 88 — FerryLink — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate rotation/renewal process for a multi-year vessel deployment
Evidence: Plan states units are issued a certificate "at installation" with "no renewal process" described "over the vessel's multi-year service life."
Risk: Units installed in the same batch would likely approach expiry together, simultaneously losing backend authentication.
Recommended mitigation: Add expiry monitoring and automated renewal before certificates approach their validity window's end.
Confidence: HIGH
PatternID: S4

[HIGH] SECURITY
Finding: No confirmed reliable time source, with routine nightly power-downs
Evidence: Plan states explicitly it "does not state whether the unit has a battery-backed RTC or depends on GPS/NTP sync following each power interruption (vessels are powered down overnight when docked)."
Risk: Every overnight power-down is a potential trigger for a clock-validation failure if no RTC is present — not a rare event but a nightly one.
Recommended mitigation: Confirm and, if needed, add a battery-backed RTC given how routine these power interruptions are.
Confidence: MEDIUM
PatternID: S6

[CRITICAL] SECURITY
Finding: [COMPOUND] Certificate expiry with no rotation, combined with routine nightly power cycling and unconfirmed clock reliability, compounds risk on passenger-carrying vessels
Evidence: Builds on the no-rotation finding and the no-confirmed-time-source finding above.
Risk: A vessel powering on each morning could face both an ambiguous clock state and an expiring/expired cert, potentially delaying safety-relevant condition reporting.
Recommended mitigation: Address certificate rotation and a reliable time source together.
Confidence: MEDIUM
PatternID: COMPOUND(S4,S6)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
