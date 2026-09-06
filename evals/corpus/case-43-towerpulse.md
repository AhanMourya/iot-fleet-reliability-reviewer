# Case 43 — TowerPulse

**Industry:** Telecom (cell tower equipment monitoring)
**Type:** seeded
**Device count:** 500

## Deployment Plan

TowerPulse deploys 500 environmental and equipment-health sensors across cell tower sites for a regional carrier, connected over the tower's dedicated backhaul link, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. The root filesystem is read-only with an overlay, with brownout detection for the site's battery backup system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The onboard sensor firmware does not include a watchdog timer; the team has relied on the backhaul link's own periodic health-check polling to notice an unresponsive sensor and schedule a technician visit, rather than any on-device automatic hang recovery. There is also no remote power-cycle path for an individual sensor separate from the tower site's main equipment power, which is not something field technicians can toggle per-sensor.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P3 | HIGH | No watchdog timer; detection via backhaul polling is not the same as automatic recovery — a hung sensor still requires a technician visit. |
| P4 | HIGH | No remote, per-sensor power-cycle capability described; site-level power isn't a substitute for isolating a single hung sensor. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P5, O1–O5, S1–S6).
