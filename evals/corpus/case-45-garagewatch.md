# Case 45 — GarageWatch

**Industry:** Parking (structured garage occupancy sensors)
**Type:** seeded
**Device count:** 950

## Deployment Plan

GarageWatch deploys 950 per-space occupancy sensors across a network of parking structures, connected over each garage's dedicated WiFi mesh to a garage management gateway, publishing on state change via MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the mesh controller. The root filesystem is read-only with an overlay, with brownout detection for the sensor's power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. If a sensor's mesh connection drops, it retries immediately and continuously on a fixed 1-second interval with no increasing delay. State-change events generated while disconnected are not stored locally — the plan states the sensor simply reports its current state once reconnected, with no mention of what happens to the specific transition events missed during the outage.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C2 | HIGH | Fixed 1-second retry with no backoff or jitter; a garage-wide mesh outage affecting many sensors at once could trigger a reconnect storm at the moment of recovery. |
| C4 | HIGH | Explicitly no local buffering of state-change events; occupancy transitions during an outage are permanently lost, not just delayed. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C3, C5, P1–P5, O1–O5, S1–S6).
