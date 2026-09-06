# Case 68 — PlowTrack

**Industry:** Municipal services (snow removal fleet telematics)
**Type:** seeded
**Device count:** 160

## Deployment Plan

PlowTrack deploys 160 telematics units across a city's snow removal fleet, powered from each vehicle's 12V system with an internal battery buffer, connected via LTE publishing every 2 minutes during active storms via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vehicle telematics bus. The root filesystem is read-only with an overlay. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. Each unit is issued a certificate at installation for backend authentication; the plan does not describe any renewal process over the vehicle's multi-year service life in the fleet (these vehicles are seasonal, sitting powered-off for most of the year between winters), and does not state whether the unit has a battery-backed RTC or depends on GPS/NTP sync after each power-on.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate rotation/renewal process for a multi-year fleet deployment; the seasonal power-off pattern makes this worse, not better, since certificates could silently expire during the off-season with no one noticing until the next storm. |
| S6 | HIGH | No confirmed reliable time source, combined with an explicitly long power-off period each year (not a brief interruption) — a strong candidate for clock-validation failure on power-up if no RTC is present. |
| COMPOUND(S4,S6) | CRITICAL | A vehicle powering on for the first storm of the season could face both an ambiguous clock state after months off and a certificate that expired unnoticed during the off-season, with no remote path to fix either during an active storm response. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5).
