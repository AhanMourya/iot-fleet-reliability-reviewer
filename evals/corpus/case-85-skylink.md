# Case 85 — SkyLink

**Industry:** Ski resort (gondola/cable car safety monitoring)
**Type:** seeded
**Device count:** 40

## Deployment Plan

SkyLink deploys 40 cable-tension and drive-motor sensors across gondola and cable car systems at a ski resort, connected over the resort's dedicated lift-operations network to a lift control gateway, publishing every second during operation via MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the lift control gateway. The root filesystem is read-only with an overlay, with brownout detection for the lift's power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. If a sensor's connection drops, it retries immediately and continuously on a fixed 1-second interval with no increasing delay. Tension and status readings generated while disconnected are not stored locally — the plan states the sensor simply resumes normal reporting once reconnected, with no mention of what happens to the specific readings missed during the outage.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C2 | HIGH | Fixed 1-second retry with no backoff or jitter; a lift-wide network event could trigger a reconnect storm across sensors at the moment of recovery. |
| C4 | HIGH | Explicitly no local buffering of tension/status readings during an outage; on a safety-monitoring system for passenger-carrying cable transport, missed readings during any outage window are a real gap even though the sensor resumes normally afterward. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C3, C5, P1–P5, O1–O5, S1–S6).
