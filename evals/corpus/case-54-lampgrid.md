# Case 54 — LampGrid

**Industry:** Municipal infrastructure (streetlight controllers)
**Type:** clean
**Device count:** 5000

## Deployment Plan

LampGrid deploys 5,000 networked streetlight controllers across a city, connected via a low-power WiFi mesh to neighborhood gateways, then MQTT/TLS to our backend, with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung controllers from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and each neighborhood gateway can remotely power-cycle any controller on its mesh. The root filesystem is read-only with an overlay, with brownout detection for the controller's power supply. Firmware updates are staged (one neighborhood, then a district, then the city) with a defined post-update health check (network reachability plus a service heartbeat, 10-minute timeout) and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each controller has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting city IT if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, department-scoped API with individually revocable credentials per city staff member.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
