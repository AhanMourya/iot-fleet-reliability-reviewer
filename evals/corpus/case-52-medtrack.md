# Case 52 — MedTrack

**Industry:** Healthcare (hospital equipment/asset tracking)
**Type:** clean
**Device count:** 2500

## Deployment Plan

MedTrack deploys 2,500 RFID/BLE asset tags on mobile medical equipment (infusion pumps, wheelchairs, monitors) across a hospital system, connected over each facility's dedicated clinical network to a location-tracking gateway, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung tags from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facility gateway. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Firmware updates are staged (one facility, then the system) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. No debug interfaces are exposed; management is via an authenticated, facility-scoped API with individually revocable credentials per staff member. Each tag has a unique certificate issued at provisioning and a battery-backed RTC; the plan does not describe any process for monitoring certificate expiry or renewing certificates before they lapse.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described; on expiry, tags would simultaneously lose backend authentication, disrupting equipment tracking across the hospital system. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5, S6).
