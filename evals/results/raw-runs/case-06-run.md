# Case 06 — AirWatch — Reviewer Run

[HIGH] CONNECTIVITY
Finding: Reconnect uses a fixed interval with no backoff or jitter
Evidence: Plan states devices reconnect "on a fixed 3-second interval" with no increasing delay or randomization mentioned.
Risk: A park-wide WiFi outage could trigger uncoordinated simultaneous reconnect attempts across all 90 devices at once, overloading the access point at the moment of recovery.
Recommended mitigation: Add exponential backoff with jitter to the reconnect logic.
Confidence: HIGH
PatternID: C2

[ADVISORY] CONNECTIVITY
Finding: Reconnect described only as a fixed-interval retry, which reads as minimal rather than clearly adequate
Evidence: The description of the reconnect behavior is limited to "reconnects automatically on a fixed 3-second interval" — functional reconnect logic is present, but the brevity of the description leaves some doubt about robustness under sustained outages.
Risk: Low — reconnect logic does exist and will eventually restore connectivity; this is a caution about description completeness rather than a distinct failure path beyond the backoff gap already flagged above.
Recommended mitigation: No additional action beyond the backoff/jitter fix above; consider more detail in future plan revisions.
Confidence: LOW
PatternID: C1

[HIGH] CONNECTIVITY
Finding: No local buffering for data generated while disconnected
Evidence: Plan states explicitly the device "resumes normal publishing once reconnected, with no mention of what happens to data from the outage window."
Risk: Every WiFi outage is a silent, permanent data-loss window for the affected sensors.
Recommended mitigation: Add a bounded local buffer with overflow alerting.
Confidence: HIGH
PatternID: C4

Findings: 0 Critical, 2 High, 1 Advisory (21 of 21 patterns checked; 18 showed no gap).
