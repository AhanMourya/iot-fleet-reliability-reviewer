# Case 83 — MedResponse

**Industry:** Emergency medical services (ambulance fleet telematics)
**Type:** seeded
**Device count:** 70

## Deployment Plan

MedResponse deploys 70 vehicle and equipment-status telematics units across a regional ambulance fleet, connected via LTE publishing every 10 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. The root filesystem is read-only with an overlay, with brownout detection for the vehicle's electrical system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The onboard telematics firmware does not include a watchdog timer; dispatch has relied on noticing a unit has stopped reporting and radioing the crew to check on it manually. There is also no remote power-cycle mechanism for the unit — recovering a hung unit requires a crew member to manually power-cycle it, which during an active call is not always immediately practical.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P3 | HIGH | No watchdog timer; dispatch noticing a silent unit is detection, not automatic recovery, and on an EMS platform the delay before someone can safely check on it has real operational cost. |
| P4 | HIGH | No remote power-cycle mechanism described; explicitly requires manual crew intervention, which is not always immediately practical during an active call. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P5, O1–O5, S1–S6).
