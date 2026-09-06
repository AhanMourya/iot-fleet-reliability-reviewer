# Case 40 — ArenaPulse

**Industry:** Sports & entertainment venues (crowd density sensors)
**Type:** clean
**Device count:** 300

## Deployment Plan

ArenaPulse deploys 300 crowd-density and foot-traffic sensors across a multi-purpose sports arena, connected over the venue's WiFi to a facilities operations gateway, publishing every minute during events via MQTT with exponential backoff and jitter on reconnect; the plan does not state whether this MQTT traffic runs over TLS. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the venue's facilities network. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe a status/heartbeat mechanism beyond the routine per-minute publish during events.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S5 | HIGH | No mention of transport encryption for the MQTT traffic; explicitly unstated either way. |
| C5 | ADVISORY | No liveness/heartbeat mechanism beyond routine publishing during events; observability gap only. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P5, O1–O5, S1–S4, S6).
