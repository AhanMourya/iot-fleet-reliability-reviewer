# Case 04 — FactoryVibe

**Industry:** Industrial / manufacturing
**Type:** seeded
**Device count:** 120

## Deployment Plan

FactoryVibe deploys 120 vibration and temperature sensors on production-line motors and conveyors across two plants, powered from the machines' 24V control circuits. Sensors connect over the plant WiFi network to a local edge gateway, then to our cloud backend via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 6 hours of readings with overflow alerting. The root filesystem uses a read-only image with an overlay for writable state, so unclean power loss (routine on a factory floor with unplanned shutdowns) doesn't corrupt storage. Firmware updates are staged, signature-verified, and use A/B rollback with a defined health-check gate. Each sensor has a unique certificate with expiry monitoring, and a battery-backed RTC. No debug interfaces are exposed. The plan does not mention any watchdog or hang-detection mechanism, and does not mention any way to remotely power-cycle a sensor if it becomes unresponsive — recovering a hung unit would require a technician to physically access the machine and power-cycle the sensor at the panel.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P3 | HIGH | No watchdog or hang-detection mechanism described; device-level, requires physical intervention to recover a hang. |
| P4 | HIGH | No remote power-cycle capability described; explicitly stated that recovery requires a technician on-site. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P5, O1–O5, S1–S6).
