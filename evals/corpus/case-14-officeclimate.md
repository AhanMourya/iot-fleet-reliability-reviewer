# Case 14 — OfficeClimate

**Industry:** Commercial real estate (office HVAC/occupancy)
**Type:** clean
**Device count:** 300

## Deployment Plan

OfficeClimate deploys 300 combined occupancy and HVAC sensors across a portfolio of office buildings, connected over building WiFi to a per-building gateway, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and an MQTT Last Will and Testament status topic distinguishes a hung device from a disconnected one. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and each floor's gateway can remotely power-cycle any sensor on its network. The root filesystem is read-only with an overlay, and a brownout detection circuit halts writes before voltage drops to an unsafe level. Firmware updates are staged (one building, then a region, then all buildings) with a defined post-update health check (network reachability plus a service heartbeat, 10-minute timeout) and automatic A/B rollback on a confirmed A/B-capable bootloader. Update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting on-call if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated VPN-scoped API only, with unique credentials issued per building operations team.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
