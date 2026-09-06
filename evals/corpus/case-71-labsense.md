# Case 71 — LabSense

**Industry:** Higher education (university research lab equipment monitoring)
**Type:** clean
**Device count:** 140

## Deployment Plan

LabSense deploys 140 temperature, humidity, and equipment-status sensors across research labs and cold storage rooms at a university, connected over the campus's dedicated research network to a facilities gateway, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for protecting research samples. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the building's UPS-backed power. Firmware updates are staged (one building, then campus-wide) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facilities IT if a renewal fails. No debug interfaces are exposed; management is via an authenticated, department-scoped API. The plan does not mention a battery-backed RTC or an early-boot time-sync strategy for certificate validation.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S6 | HIGH | No mention of a battery-backed RTC or trusted early time source; a power event could leave a sensor unable to validate certificates until time sync completes, risking undetected sample-storage excursions. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S5).
