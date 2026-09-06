# Case 65 — TollFlow

**Industry:** Transportation infrastructure (highway tolling sensors)
**Type:** seeded
**Device count:** 220

## Deployment Plan

TollFlow deploys 220 vehicle-detection and license-plate-capture sensors across highway tolling gantries, connected over a dedicated fiber-and-cellular-backup network to a regional tolling data center, publishing every event via MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the gantry's control cabinet. The root filesystem is read-only with an overlay, with brownout detection for the cabinet's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. If a sensor's connection drops, it retries immediately and continuously on a fixed 2-second interval with no increasing delay. Toll events generated while disconnected are not stored locally — the plan states the sensor simply resumes normal reporting once reconnected, with no mention of what happens to vehicle-passage events missed during the outage window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C2 | HIGH | Fixed 2-second retry with no backoff or jitter; a fiber/cellular backup failover event affecting multiple gantries could trigger a reconnect storm. |
| C4 | HIGH | Explicitly no local buffering; missed toll events during an outage are permanently lost, with direct revenue and enforcement implications. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C3, C5, P1–P5, O1–O5, S1–S6).
