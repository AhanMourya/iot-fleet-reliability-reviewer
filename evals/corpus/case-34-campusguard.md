# Case 34 — CampusGuard

**Industry:** Education (school campus security/access)
**Type:** clean
**Device count:** 250

## Deployment Plan

CampusGuard deploys 250 door-access and badge-reader sensors across a school district's campuses, connected over each campus's dedicated security network to a district operations center, publishing every 30 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung devices from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and each campus's operations closet can remotely power-cycle any reader on its network. The root filesystem is read-only with an overlay, and a brownout detection circuit halts writes before voltage drops to an unsafe level. Firmware updates are staged (one campus first, then the district) with a defined post-update health check (network reachability plus a service heartbeat, 10-minute timeout) and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each reader has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting district IT if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, district-scoped API with individually revocable credentials per staff member.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
