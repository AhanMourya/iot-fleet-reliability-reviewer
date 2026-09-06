# Case 92 — VaultClime

**Industry:** Records management (archive/records storage climate control)
**Type:** clean
**Device count:** 50

## Deployment Plan

VaultClime deploys 50 temperature and humidity sensors across climate-controlled archive and records storage facilities, connected over each facility's dedicated network to a facilities operations gateway, publishing every 10 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for protecting irreplaceable physical archives. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the facility's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate issued at installation and a battery-backed RTC; the plan does not describe any process for monitoring certificate expiry or renewing certificates before they lapse. No debug interfaces are exposed; management is via an authenticated, facility-scoped API.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described; on expiry, sensors would simultaneously lose backend authentication, risking undetected climate excursions affecting irreplaceable physical records. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5, S6).
