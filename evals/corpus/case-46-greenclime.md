# Case 46 — GreenClime

**Industry:** Agriculture (greenhouse climate control)
**Type:** seeded
**Device count:** 200

## Deployment Plan

GreenClime deploys 200 climate control actuators (vents, shading, irrigation valves) across a network of commercial greenhouses, connected over each facility's WiFi to a local controller, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung actuators from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facility controller. The root filesystem is read-only with an overlay, with brownout detection for the facility's power supply. Each actuator has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed to all actuators in a facility simultaneously via a script that overwrites the current application binary and restarts the control service; there is no fallback partition to revert to if a bad update causes an actuator to malfunction, so recovery requires a technician to manually reflash the affected units.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Explicit single-partition overwrite update with no fallback; a bad push could leave climate actuators malfunctioning (e.g., vents stuck open or closed) across a facility with no remote recovery — direct crop-health and equipment-damage consequence. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O5, S1–S6).
