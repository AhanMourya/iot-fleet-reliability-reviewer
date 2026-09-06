# Case 11 — AquaSense

**Industry:** Aquaculture
**Type:** clean
**Device count:** 60

## Deployment Plan

AquaSense deploys 60 water-quality sensors (dissolved oxygen, pH, temperature) across fish farm tanks at a single facility, connected over the facility's WiFi to a local gateway, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and a remote power-cycle relay per tank controller. The root filesystem is read-only with an overlay for writable state, and a brownout detection circuit halts writes before voltage drops below safe levels. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate, and the board's bootloader is confirmed A/B-capable. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated backend API only. The plan does not describe any device status/heartbeat mechanism beyond the routine 5-minute publish interval.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C5 | ADVISORY | No liveness/heartbeat mechanism beyond routine publishing; observability gap only, no active failure path evidenced. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P5, O1–O5, S1–S6).
