# Case 56 — CropWing

**Industry:** Agriculture (crop-spraying drone fleet)
**Type:** clean
**Device count:** 25

## Deployment Plan

CropWing operates a 25-drone crop-spraying fleet across several farming operations, with each drone connecting via LTE to our flight-operations backend over MQTT/TLS, exponential backoff and jitter on reconnect, and unique client IDs derived from hardware serials. Local buffering covers 2 hours of telemetry with overflow alerting, and a status heartbeat runs continuously during flight. Drones have a hardware watchdog, and ground crew can remotely power-cycle a grounded drone via its charging dock. The root filesystem is read-only with an overlay, with brownout detection for the flight battery system. Flight-control firmware updates are staged (a single drone, then the full fleet) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each drone has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any reset-count tracking or escalation if the watchdog ends up resetting a drone repeatedly in a short window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P5 | HIGH | Watchdog is present, but no reset-loop detection or escalation described; a persistent bad state causing repeated resets mid-operation is a meaningful gap on a platform where an unrecovered hang during flight has direct safety implications. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P4, O1–O5, S1–S6).
