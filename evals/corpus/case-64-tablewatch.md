# Case 64 — TableWatch

**Industry:** Gaming (casino gaming floor sensors)
**Type:** seeded
**Device count:** 450

## Deployment Plan

TableWatch deploys 450 chip-tray and table-status sensors across a casino gaming floor, connected over the casino's dedicated security network to a floor operations gateway, publishing continuously via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the floor gateway. The root filesystem is read-only with an overlay, with brownout detection for the UPS-backed power. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are staged (a small pilot area, then the full floor) with a defined post-update health check. The update pipeline downloads new firmware over an internally-hosted HTTPS distribution point and applies it directly to the sensor; there is no cryptographic signature check on the firmware binary itself beyond the transport-level HTTPS connection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O2 | CRITICAL | No signature verification of the firmware binary; explicit reliance on HTTPS transport alone, on gaming-floor infrastructure with direct financial-integrity relevance. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1, O3–O5, S1–S6).
