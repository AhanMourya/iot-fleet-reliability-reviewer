# Case 60 — BrewBot

**Industry:** Vending & self-service equipment
**Type:** clean
**Device count:** 1800

## Deployment Plan

BrewBot deploys 1,800 telemetry units across a coffee and snack vending machine fleet, connected via LTE-M publishing every 10 minutes via MQTT with exponential backoff and jitter on reconnect; the plan does not state whether this MQTT traffic runs over TLS. Client IDs are derived from unique hardware serials. Local buffering covers 48 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the unit's own control board. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe a status/heartbeat mechanism beyond the routine 10-minute publish.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S5 | HIGH | No mention of transport encryption for the MQTT traffic; explicitly unstated either way. |
| C5 | ADVISORY | No liveness/heartbeat mechanism beyond routine publishing; observability gap only. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P5, O1–O5, S1–S4, S6).
