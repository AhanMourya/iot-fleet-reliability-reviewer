# Case 75 — PawStay

**Industry:** Pet care (daycare/boarding facility monitoring)
**Type:** clean
**Device count:** 45

## Deployment Plan

PawStay deploys 45 environmental and access-control sensors across a network of pet daycare and boarding facilities, connected over each facility's WiFi to a facilities operations gateway, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged (one facility, then the network), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each unit has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facility managers if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, facility-scoped API with individually revocable credentials per staff member.

## Ground Truth

No expected findings — all 21 patterns are explicitly addressed with adequate evidence in the plan.
