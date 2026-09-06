# Case 09 — IrrigateIQ

**Industry:** Agriculture (irrigation control)
**Type:** seeded
**Device count:** 250

## Deployment Plan

IrrigateIQ deploys 250 valve controller units across several farms, each independently powered by its own small solar panel and battery at its individual valve box (no shared power circuit between units). Units connect over LoRaWAN to a farm gateway, then MQTT/TLS to our backend, with exponential backoff and jitter on reconnect and unique client IDs derived from hardware serials. Local buffering covers 48 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and a remote power-cycle relay reachable through the gateway. Firmware updates are staged, signature-verified, with A/B rollback on health-check failure. Each unit has a unique certificate with expiry monitoring and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any filesystem write-protection (read-only root, overlay, or equivalent) for the controller's local storage — power interruptions are described as "handled by the battery buffer," but the buffer is sized only for maintaining valve state, not for guaranteeing a clean shutdown sequence before the buffer itself depletes.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P1 | HIGH | No filesystem write-protection described; the battery buffer covers routine operation but not a guaranteed clean shutdown, so a depletion event could still corrupt storage. Device-level (independent power per unit, explicitly no shared circuit), so High rather than Critical per the taxonomy's default. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P2–P5, O1–O5, S1–S6).
