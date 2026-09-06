# Case 07 — RouteTrack

**Industry:** Fleet / vehicle telematics
**Type:** seeded
**Device count:** 300

## Deployment Plan

RouteTrack deploys 300 GPS/telematics units in delivery vans, powered from the vehicle's 12V system with a small internal battery buffer for brief disconnects. Units connect over LTE, publishing location and diagnostic data every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 12 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vehicle telematics bus. The root filesystem is read-only with an overlay for writable state. Firmware updates are staged, signature-verified, with A/B rollback on health-check failure. No debug interfaces are exposed. Each unit has a certificate issued at manufacturing for backend authentication; the plan doesn't describe any process for renewing or rotating this certificate over the vehicle's expected multi-year service life, and doesn't mention whether the unit has a battery-backed RTC or relies on GPS/NTP time sync after each power cycle.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate rotation/renewal process described for a multi-year deployment; units provisioned in the same manufacturing run would likely expire close together with no remote recovery if the update channel depends on the same cert. |
| S6 | HIGH | No mention of a battery-backed RTC or a trusted early time source; units without one would fail cert validation after every power interruption until time sync completes. |
| COMPOUND(S4,S6) | CRITICAL | Certificate expiry combined with no reliable clock compounds the failure: a unit that loses power near the cert's expiry could boot with an ambiguous clock state right as its (unrotated) certificate becomes invalid, with no remote path to fix either. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5).
