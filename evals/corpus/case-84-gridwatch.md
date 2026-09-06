# Case 84 — GridWatch

**Industry:** Utilities (smart grid substation monitoring)
**Type:** seeded
**Device count:** 300

## Deployment Plan

GridWatch deploys 300 transformer and breaker-status sensors across substations on a regional power grid, connected over the utility's dedicated SCADA network to a control center gateway, publishing every 5 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the substation control unit. The root filesystem is read-only with an overlay, with brownout detection for the substation's UPS-backed power. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are staged (a pilot substation, then a region, then the grid) with a defined post-update health check. The update pipeline downloads new firmware over an internally-hosted HTTPS endpoint and applies it directly; there is no cryptographic signature check on the firmware binary itself beyond the transport-level HTTPS connection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O2 | CRITICAL | No signature verification of the firmware binary; explicit reliance on HTTPS transport alone, on critical grid infrastructure. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1, O3–O5, S1–S6).
