# Case 81 — MileFlow

**Industry:** Insurance (usage-based auto insurance telematics)
**Type:** seeded
**Device count:** 12000

## Deployment Plan

MileFlow deploys 12,000 OBD-port telematics dongles across a usage-based auto insurance program, connected via LTE-M publishing driving-behavior events every 30 seconds during trips via MQTT/TLS. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vehicle's OBD power. The root filesystem is read-only with an overlay, with brownout detection for the vehicle's electrical system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. On startup, each dongle establishes its MQTT session and begins publishing; the plan does not describe any behavior for re-establishing the session if it drops mid-trip — the team assumed cellular coverage would be continuous for the vast majority of trips and didn't design a reconnect path for the remainder.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C1 | CRITICAL | No reconnect/fallback logic described; a coverage gap mid-trip (acknowledged as a real, if minority, scenario) is a fleet-wide-capable trigger with no automatic recovery, directly affecting the accuracy of usage-based billing data. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C2–C5, P1–P5, O1–O5, S1–S6).
