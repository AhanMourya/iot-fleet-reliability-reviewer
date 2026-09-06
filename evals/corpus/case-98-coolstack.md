# Case 98 — CoolStack

**Industry:** Data center infrastructure (liquid cooling loop monitoring)
**Type:** clean
**Device count:** 75

## Deployment Plan

CoolStack deploys 75 flow-rate, temperature, and leak-detection sensors across liquid cooling loops in a data center, connected over the facility's dedicated management network to a facilities operations gateway, publishing every 15 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 12 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters given the leak-detection role. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets. The root filesystem is read-only with an overlay, with brownout detection for the facility's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, facility-scoped API. There is no remote power-cycle mechanism described for these sensors.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | No remote power-cycle capability described; any sensor hang not caught by the watchdog requires a technician to physically access the cooling loop area to recover it, which matters for timely leak-detection coverage. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1–S6).
