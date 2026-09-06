# Case 50 — SunField

**Industry:** Renewable energy (solar farm panel monitoring)
**Type:** seeded
**Device count:** 700

## Deployment Plan

SunField deploys 700 panel-level monitoring units across a utility-scale solar farm, connected over the farm's dedicated industrial network to a SCADA gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the SCADA gateway. The root filesystem is read-only with an overlay, with brownout detection for the panel's power-harvesting circuit. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed as full binary replacements to the monitoring unit's single application partition; this generation's MCU bootloader has no documented support for dual-partition (A/B) updates, so a failed update requires a technician to physically visit the panel and reflash the unit via its service port.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | No rollback/A-B path — explicit single-partition overwrite. |
| O5 | CRITICAL | Explicitly no documented A/B bootloader support on this MCU generation — foreclosure case, no future software fix possible without different hardware. |
| COMPOUND(O1,O5) | CRITICAL | The rollback gap is permanent for this generation; at 700-unit farm scale, a bad push could require technician visits to a large fraction of the array. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O4, S1–S6).
