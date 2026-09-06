# Case 94 — DeskPulse

**Industry:** Coworking spaces (environmental & access monitoring)
**Type:** clean
**Device count:** 220

## Deployment Plan

DeskPulse deploys 220 occupancy, environmental, and door-access sensors across a network of coworking locations, connected over each location's WiFi to a facilities operations gateway, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged (one location, then the network), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each unit has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facilities staff if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, location-scoped API with individually revocable credentials per site manager.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
