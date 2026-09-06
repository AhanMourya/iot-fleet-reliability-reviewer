# Case 61 — CleanRoomX

**Industry:** Semiconductor manufacturing (cleanroom environmental monitoring)
**Type:** seeded
**Device count:** 160

## Deployment Plan

CleanRoomX deploys 160 particle-count and pressure-differential sensors across a semiconductor fab's cleanroom zones, connected over the fab's dedicated facilities network to a cleanroom operations gateway, publishing every 10 seconds via MQTT/TLS. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the fab's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. On startup, each sensor establishes its MQTT session and begins publishing; the plan does not describe any behavior for re-establishing the session if it drops after startup — the facilities team has historically treated the fab's internal network as effectively always-up and didn't design for a mid-shift reconnect scenario.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C1 | CRITICAL | No reconnect/fallback logic described; a network blip (even a brief one on infrastructure "historically treated as always-up") is a fleet-wide-capable trigger with no automatic recovery — for cleanroom process-control sensing, a gap in particle-count monitoring has direct yield/quality implications. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C2–C5, P1–P5, O1–O5, S1–S6).
