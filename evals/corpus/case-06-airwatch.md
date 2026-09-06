# Case 06 — AirWatch

**Industry:** Environmental monitoring (public parks)
**Type:** seeded
**Device count:** 90

## Deployment Plan

AirWatch deploys 90 air quality sensors (PM2.5, NO2, ozone) across public parks in a mid-sized city, connected via WiFi to municipal park network access points, publishing every 10 minutes over MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation, a battery-backed RTC, and a remote power-cycle relay at each mounting pole. Firmware updates are staged, signature-verified, with A/B rollback on health-check failure. Each device has a unique certificate with expiry monitoring. No debug interfaces are exposed. If a device's WiFi connection drops, the client library reconnects automatically on a fixed 3-second interval; the plan does not describe any increasing delay or randomization for this retry. Readings generated while disconnected are not stored locally — the plan states the device simply resumes normal publishing once reconnected, with no mention of what happens to data from the outage window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C2 | HIGH | Fixed 3-second reconnect interval with no backoff or jitter described; fleet-wide-capable trigger (park-wide WiFi outage) with a working but unmanaged recovery path. |
| C4 | HIGH | Explicitly no local buffering — data from any outage window is lost with no mention of alerting on the loss. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C3, C5, P1–P5, O1–O5, S1–S6).
