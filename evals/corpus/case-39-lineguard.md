# Case 39 — LineGuard

**Industry:** Automotive manufacturing (assembly line quality sensors)
**Type:** clean
**Device count:** 140

## Deployment Plan

LineGuard deploys 140 torque and alignment sensors across an automotive assembly line, connected over the plant's dedicated industrial network to a line-control gateway, publishing every second during operation via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 8 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the line-control gateway. The root filesystem is read-only with an overlay for writable state. Firmware updates are staged (one line, then the full plant), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Power is provided from the plant's conditioned industrial power distribution; the plan does not describe any device-level brownout/undervoltage detection, treating the plant's power conditioning as sufficient protection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P2 | HIGH | No device-level brownout/undervoltage detection described; facility-level power conditioning reduces but doesn't eliminate the chance of a marginal voltage event reaching an individual sensor (e.g., a local PDU fault), which a device-level check would catch. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P3–P5, O1–O5, S1–S6).
