# Case 72 — MeatLine

**Industry:** Food processing (meat processing plant monitoring)
**Type:** clean
**Device count:** 210

## Deployment Plan

MeatLine deploys 210 temperature and equipment-status sensors across a meat processing plant's cold rooms and production lines, connected over the plant's dedicated network to a plant operations gateway, publishing every 3 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for food-safety compliance. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the plant's building management system. The root filesystem is read-only with an overlay, with brownout detection for the plant's UPS-backed power. Firmware updates are staged (one production line, then the full plant), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each sensor has a unique certificate issued at installation and a battery-backed RTC; the plan does not describe any process for monitoring certificate expiry or renewing certificates before they lapse. No debug interfaces are exposed; management is via an authenticated, plant-scoped API.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described; on expiry, sensors would simultaneously lose backend authentication — for food-safety compliance monitoring, a silent authentication outage has direct regulatory consequence. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5, S6).
