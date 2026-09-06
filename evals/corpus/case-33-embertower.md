# Case 33 — EmberTower

**Industry:** Forestry (wildfire detection towers)
**Type:** clean
**Device count:** 50

## Deployment Plan

EmberTower deploys 50 smoke and thermal-imaging detection units on remote forestry lookout towers, connected via satellite modem publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 5 days (accounting for expected satellite interruptions) with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Given the remote tower locations, there is no remote power-cycle mechanism — recovering a wedged unit the watchdog doesn't catch requires a ranger service visit, which the team has accepted as a residual risk for this pilot given the terrain.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | Explicitly no remote power-cycle capability; the taxonomy's evidence-missing criterion is the absence of the capability, not the absence of a rationale for it — a documented risk acceptance doesn't change the severity, only potentially the response the plan owner chooses to take. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1–S6).
