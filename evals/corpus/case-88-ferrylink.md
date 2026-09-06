# Case 88 — FerryLink

**Industry:** Maritime (passenger ferry equipment monitoring)
**Type:** seeded
**Device count:** 60

## Deployment Plan

FerryLink deploys 60 engine and hull-condition sensors across a regional passenger ferry fleet, powered from each vessel's electrical system with an internal battery buffer, connected via a mix of cellular and satellite backup publishing every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vessel's operations network. The root filesystem is read-only with an overlay. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. Each unit is issued a certificate at installation for backend authentication; the plan does not describe any renewal process over the vessel's multi-year service life, and does not state whether the unit has a battery-backed RTC or depends on GPS/NTP sync following each power interruption (vessels are powered down overnight when docked).

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate rotation/renewal process for a multi-year fleet deployment. |
| S6 | HIGH | No confirmed reliable time source, with routine nightly power-downs explicitly described — every overnight dock period is a potential trigger for a clock-validation failure if no RTC is present. |
| COMPOUND(S4,S6) | CRITICAL | Certificate expiry combined with routine nightly power cycling and unconfirmed clock reliability compounds risk on passenger-carrying vessels where a silent authentication outage could delay safety-relevant condition reporting. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5).
