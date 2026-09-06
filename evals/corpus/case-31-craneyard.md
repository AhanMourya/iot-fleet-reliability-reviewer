# Case 31 — CraneYard

**Industry:** Ports (container yard crane sensors)
**Type:** clean
**Device count:** 55

## Deployment Plan

CraneYard deploys 55 load and position sensors across gantry cranes at a container terminal, connected over the terminal's dedicated industrial WiFi to a yard operations gateway, publishing every 10 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 12 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and a remote power-cycle relay per crane. The root filesystem is read-only with an overlay, with brownout detection for the crane's onboard power system. Firmware updates are staged (one crane, then a section of the yard, then the full fleet), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting operations if a renewal attempt fails. No debug interfaces are exposed; management is via an authenticated API scoped to the terminal's operations VLAN, with individually revocable credentials per operator. The plan does not mention a battery-backed RTC or any early-boot time-sync strategy for certificate validation.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S6 | HIGH | No mention of a battery-backed RTC or trusted early time source; a power event could leave a sensor unable to validate certificates until time sync completes. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S5).
