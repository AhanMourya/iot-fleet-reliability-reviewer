# Case 26 — ClearFlow

**Industry:** Water utility (wastewater treatment)
**Type:** seeded
**Device count:** 70

## Deployment Plan

ClearFlow deploys 70 flow-rate and contaminant sensors across a municipal wastewater treatment plant, connected over the plant's dedicated industrial network to a SCADA integration point, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 12 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the plant's industrial control system. The root filesystem is read-only with an overlay, with brownout detection for the plant's UPS-backed power. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are staged across the plant's sensor zones with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader. The update pipeline retrieves new firmware over an internally-hosted HTTPS endpoint and applies it directly; there is currently no cryptographic signature check on the firmware binary itself beyond the transport-level HTTPS connection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O2 | CRITICAL | No signature verification of the firmware binary; explicit reliance on HTTPS transport in place of image authenticity — matches the taxonomy's explicit distinction between the two, on a plant with public-health-relevant sensing. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1, O3–O5, S1–S6).
