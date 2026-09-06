# Case 13 — SnowWatch

**Industry:** Outdoor / ski resort (snowpack monitoring)
**Type:** clean
**Device count:** 35

## Deployment Plan

SnowWatch deploys 35 snowpack and avalanche-risk sensors across backcountry terrain near a ski resort, connected via satellite modem (given the remote terrain) publishing every 30 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 72 hours (accounting for expected satellite link interruptions during storms) with overflow alerting, and a status topic distinguishes hung devices from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Given the terrain, there is no remote power-cycle mechanism — recovering a wedged unit that the watchdog doesn't catch would require a backcountry service trip.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | Explicitly no remote power-cycle capability; watchdog handles most hangs, but any hang class it misses requires physical (backcountry) access. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1–S6).
