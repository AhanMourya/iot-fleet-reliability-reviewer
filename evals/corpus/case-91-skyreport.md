# Case 91 — SkyReport

**Industry:** Weather monitoring (public/commercial weather station network)
**Type:** clean
**Device count:** 320

## Deployment Plan

SkyReport deploys 320 weather stations (temperature, wind, precipitation, pressure) across a regional network for a commercial weather data provider, connected via cellular publishing every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung stations from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via a cellular-triggered relay. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each station has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting operations if a renewal fails. No debug interfaces are exposed; management is via an authenticated API only. The plan does not mention a battery-backed RTC or an early-boot time-sync strategy for certificate validation.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S6 | HIGH | No mention of a battery-backed RTC or trusted early time source; a power event could leave a station unable to validate certificates until time sync completes. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S5).
