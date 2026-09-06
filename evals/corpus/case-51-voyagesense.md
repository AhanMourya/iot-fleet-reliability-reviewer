# Case 51 — VoyageSense

**Industry:** Cruise lines (shipboard equipment monitoring)
**Type:** clean
**Device count:** 90

## Deployment Plan

VoyageSense deploys 90 mechanical and environmental sensors across engine rooms and HVAC systems on a cruise ship, connected over the vessel's dedicated shipboard network to an onboard operations gateway, publishing every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 48 hours (accounting for expected periods with no satellite uplink at sea) with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the ship's operations network. The root filesystem is read-only with an overlay, with brownout detection for the vessel's power system. Firmware updates are staged (one deck, then the full vessel) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting ship's engineering if a renewal fails. No debug interfaces are exposed; management is via an authenticated, vessel-scoped API. The plan does not mention a battery-backed RTC or an early-boot time-sync strategy independent of satellite connectivity.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S6 | HIGH | No mention of a battery-backed RTC or a time source independent of satellite connectivity; a power event during a period without satellite uplink could leave a sensor unable to validate certificates. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S5).
