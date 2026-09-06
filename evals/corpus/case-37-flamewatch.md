# Case 37 — FlameWatch

**Industry:** Commercial fire/life-safety systems
**Type:** clean
**Device count:** 500

## Deployment Plan

FlameWatch deploys 500 networked smoke and heat detectors across a portfolio of commercial office buildings, connected over each building's dedicated life-safety network to a building fire panel gateway, publishing status every 30 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a detector as unreachable quickly. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and each floor's fire panel can remotely power-cycle any detector on its network. The root filesystem is read-only with an overlay, with brownout detection for the life-safety circuit's battery-backed power. Firmware updates are staged (one building, then a region, then the full portfolio) with a defined post-update health check (network reachability plus a service heartbeat, 10-minute timeout) and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each detector has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting building engineering if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, building-scoped API with individually revocable credentials per engineering staff member.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
