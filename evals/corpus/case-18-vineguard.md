# Case 18 — VineGuard

**Industry:** Agriculture (viticulture)
**Type:** clean
**Device count:** 150

## Deployment Plan

VineGuard deploys 150 soil moisture and weather sensors across a vineyard estate, connected over a private LoRaWAN network to an on-site gateway, then MQTT/TLS to our backend, with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 72 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and a remote power-cycle relay per row controller. The root filesystem is read-only with an overlay, and a brownout detection circuit halts writes before voltage drops to an unsafe level for the solar/battery system. Firmware updates are staged (a test row, then the full estate) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting the ops team if a renewal attempt fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated backend API only, with individually revocable credentials per operator.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
