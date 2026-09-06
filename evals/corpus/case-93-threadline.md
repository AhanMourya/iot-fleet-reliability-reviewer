# Case 93 — ThreadLine

**Industry:** Textile manufacturing (garment factory monitoring)
**Type:** clean
**Device count:** 165

## Deployment Plan

ThreadLine deploys 165 machine-status and environmental sensors across a textile and garment production facility, connected over the facility's dedicated industrial network to a plant operations gateway, publishing every 30 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the plant gateway. The root filesystem is read-only with an overlay. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Power is provided from the facility's standard industrial circuits shared with heavy sewing and cutting machinery; the plan does not describe any device-level brownout/undervoltage detection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P2 | HIGH | No device-level brownout/undervoltage detection described, on circuits explicitly shared with heavy machinery — a plausible source of voltage sag that a device-level check would catch. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P3–P5, O1–O5, S1–S6).
