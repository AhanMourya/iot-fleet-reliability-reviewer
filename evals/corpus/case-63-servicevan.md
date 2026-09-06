# Case 63 — ServiceVan

**Industry:** HVAC service fleet (mobile van telematics)
**Type:** seeded
**Device count:** 85

## Deployment Plan

ServiceVan deploys 85 telematics and equipment-status units across an HVAC service company's van fleet, connected via LTE publishing every 3 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. The root filesystem is read-only with an overlay, with brownout detection for the vehicle's electrical system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The onboard telematics firmware does not include a watchdog timer; the dispatch team has relied on noticing a van's unit has stopped reporting and calling the technician to check on it. There is also no remote power-cycle mechanism for the unit — recovering a hung unit currently means a technician manually unplugging and replugging it from the vehicle's accessory power.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P3 | HIGH | No watchdog timer; dispatch noticing a silent van is detection, not automatic recovery — a technician still has to intervene. |
| P4 | HIGH | No remote power-cycle mechanism described; explicitly requires manual unplug/replug by the technician. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P5, O1–O5, S1–S6).
