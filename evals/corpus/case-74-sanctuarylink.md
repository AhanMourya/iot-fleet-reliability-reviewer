# Case 74 — SanctuaryLink

**Industry:** Religious/community venues (AV & security monitoring)
**Type:** clean
**Device count:** 60

## Deployment Plan

SanctuaryLink deploys 60 AV equipment-status and door-security sensors across a network of community worship venues, connected over each venue's WiFi to a facilities operations gateway, publishing every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged (one venue, then the network), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each unit has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facilities staff if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, venue-scoped API with individually revocable credentials per volunteer coordinator.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
