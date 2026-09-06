# Case 48 — RentalFleet

**Industry:** Car rental (fleet telematics)
**Type:** seeded
**Device count:** 1200

## Deployment Plan

RentalFleet deploys 1,200 telematics units across a car rental company's fleet, powered from each vehicle's 12V system with an internal battery buffer, connected via LTE publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vehicle telematics bus. The root filesystem is read-only with an overlay. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. Each unit is issued a certificate at installation for backend authentication; the plan does not describe any renewal process over the vehicle's multi-year service life in the fleet, and does not state whether the unit has a battery-backed RTC or depends on GPS/NTP time sync following each power interruption (routine, given vehicles are frequently switched off).

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate rotation/renewal process for a multi-year fleet deployment; units installed in the same batch would likely approach expiry together. |
| S6 | HIGH | No confirmed reliable time source, and power interruptions (vehicle being switched off) are explicitly routine rather than rare — every such interruption is a potential trigger for a clock-validation failure if no RTC is present. |
| COMPOUND(S4,S6) | CRITICAL | Certificate expiry combined with routine power interruptions and no confirmed clock reliability compounds risk: a vehicle switched off near the cert's expiry window could return with both an ambiguous clock state and an expiring/expired cert. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5).
