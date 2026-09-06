# Case 90 — FreightCar

**Industry:** Rail freight (freight rail car condition monitoring)
**Type:** seeded
**Device count:** 850

## Deployment Plan

FreightCar deploys 850 axle-temperature and load-condition sensors across a freight rail operator's rolling stock, connected via cellular when in yard/populated areas and satellite in remote corridors, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the rail car's onboard control unit. The root filesystem is read-only with an overlay, with brownout detection for the car's battery-harvesting power system. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed as full binary replacements to the sensor's single application partition; this sensor generation's MCU bootloader has no documented support for dual-partition (A/B) updates, so a failed update requires a technician to visit the rail car (potentially at a remote yard) and physically reflash the unit via its service port.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | No rollback/A-B path — explicit single-partition overwrite. |
| O5 | CRITICAL | Explicitly no documented A/B bootloader support on this MCU generation — foreclosure case. |
| COMPOUND(O1,O5) | CRITICAL | The rollback gap is permanent for this generation; a bad push could require technician visits to remote rail yards across 850 cars. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O4, S1–S6).
