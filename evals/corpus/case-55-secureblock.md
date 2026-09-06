# Case 55 — SecureBlock

**Industry:** Corrections (correctional facility environmental/access sensors)
**Type:** clean
**Device count:** 400

## Deployment Plan

SecureBlock deploys 400 environmental and door-status sensors across a correctional facility's housing units, connected over the facility's dedicated, air-gapped-from-internet security network to a central operations gateway, publishing every 15 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facility's operations gateway. The root filesystem is read-only with an overlay, with brownout detection for the facility's UPS-backed power. Firmware updates are staged (one housing unit, then the full facility) with a defined post-update health check (network reachability plus a service heartbeat, 10-minute timeout) and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facility IT if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, role-scoped API with individually revocable credentials per operations staff member, and the operations network has no path to the public internet by design.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
