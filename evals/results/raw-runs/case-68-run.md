# Case 68 — PlowTrack — Reviewer Run

[CRITICAL] SECURITY
Finding: No certificate rotation/renewal process, worsened by seasonal power-off pattern
Evidence: Plan states no renewal process is described "over the vehicle's multi-year service life," and explicitly notes "these vehicles are seasonal, sitting powered-off for most of the year between winters."
Risk: Certificates could silently expire during the off-season with no one noticing until the first storm of the next season, when the fleet is needed most.
Recommended mitigation: Add expiry monitoring and automated renewal, with specific attention to the seasonal power-off pattern (e.g., a pre-season connectivity/cert-health check before the first storm).
Confidence: HIGH
PatternID: S4

[HIGH] SECURITY
Finding: No confirmed reliable time source, combined with an explicitly long annual power-off period
Evidence: Plan states it "does not state whether the unit has a battery-backed RTC or depends on GPS/NTP sync after each power-on," with power-off lasting most of the year.
Risk: A months-long power-off is a strong candidate for clock-validation failure on power-up if no RTC is present, unlike a brief interruption.
Recommended mitigation: Confirm and, if needed, add a battery-backed RTC given the unusually long power-off duration this fleet experiences.
Confidence: MEDIUM
PatternID: S6

[CRITICAL] SECURITY
Finding: [COMPOUND] Certificate expiry with no rotation, combined with a long seasonal power-off and unconfirmed clock reliability, compounds risk at the worst possible time
Evidence: Builds on the no-rotation finding and the no-confirmed-time-source finding above.
Risk: A vehicle powering on for the first storm could face both an ambiguous clock state and a certificate that silently expired months earlier, with no remote path to fix either during active storm response.
Recommended mitigation: Address certificate rotation and a reliable time source together, prioritized ahead of the next storm season.
Confidence: MEDIUM
PatternID: COMPOUND(S4,S6)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
