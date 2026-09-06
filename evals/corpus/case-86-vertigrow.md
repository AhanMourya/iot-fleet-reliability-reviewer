# Case 86 — VertiGrow

**Industry:** Agriculture (vertical farming / indoor hydroponics)
**Type:** seeded
**Device count:** 240

## Deployment Plan

VertiGrow deploys 240 climate and nutrient-dosing controllers across an indoor vertical farming facility, connected over the facility's dedicated WiFi to a facility control gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung controllers from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facility gateway. The root filesystem is read-only with an overlay, with brownout detection for the facility's power supply. Each controller has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed to all controllers simultaneously via a script that overwrites the current application binary and restarts the control service; there is no fallback partition to revert to if a bad update causes a dosing controller to malfunction, so recovery requires a technician to manually reflash the affected units.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Explicit single-partition overwrite update with no fallback; a bad push could cause nutrient-dosing controllers to malfunction across the facility with no remote recovery — direct crop-loss consequence at commercial scale. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O5, S1–S6).
