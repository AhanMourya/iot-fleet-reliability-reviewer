# Case 96 — LotWatch

**Industry:** Automotive retail (car dealership lot inventory tracking)
**Type:** clean
**Device count:** 30

## Deployment Plan

LotWatch deploys 30 GPS/inventory tracking units across a car dealership's vehicle lot, connected via LTE-M publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog and remote power-cycle via the unit's own control board. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any reset-count tracking or escalation if the watchdog ends up resetting a unit repeatedly in a short window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P5 | HIGH | Watchdog is present, but no reset-loop detection or escalation described; a persistent bad state causing repeated resets could look like intermittent connectivity rather than a clear, alertable failure. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P4, O1–O5, S1–S6).
