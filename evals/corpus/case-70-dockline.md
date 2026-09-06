# Case 70 — DockLine

**Industry:** Marine (marina/boat slip monitoring)
**Type:** seeded
**Device count:** 380

## Deployment Plan

DockLine deploys 380 water-level, shore-power, and slip-occupancy sensors across a network of marinas, connected over each marina's dedicated WiFi to a marina operations gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the marina gateway. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed as full binary replacements to the sensor's single application partition; this sensor generation's MCU bootloader has no documented support for dual-partition (A/B) updates, so a failed update requires a technician to visit the dock and physically reflash the unit via its service port.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | No rollback/A-B path — explicit single-partition overwrite. |
| O5 | CRITICAL | Explicitly no documented A/B bootloader support on this sensor generation — foreclosure case, no future software fix possible without different hardware. |
| COMPOUND(O1,O5) | CRITICAL | The rollback gap is permanent for this generation across all marinas using it; a bad push requires technician dock visits at scale. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O4, S1–S6).
