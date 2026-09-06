# Case 58 — LiftGuard

**Industry:** Building infrastructure (elevator/escalator monitoring)
**Type:** clean
**Device count:** 210

## Deployment Plan

LiftGuard deploys 210 vibration, motor-current, and door-cycle sensors across elevators and escalators in a portfolio of commercial buildings, connected over each building's dedicated facilities network to a building operations gateway, publishing every 30 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for this equipment category. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets. The root filesystem is read-only with an overlay, with brownout detection for the elevator machine room's power supply. Firmware updates are staged (one building, then a region, then the portfolio) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting building engineering if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, building-scoped API. Machine rooms are generally not remotely accessible for power control due to elevator safety code restrictions on remote actuation of machine room equipment, so there is no remote power-cycle path for these sensors — recovering a hung sensor the watchdog doesn't catch requires a technician visit during a scheduled maintenance window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | Explicitly no remote power-cycle capability. The stated reason (safety code restrictions on remote actuation in machine rooms) is a legitimate regulatory constraint, not evidence the capability exists — the taxonomy's evidence-missing criterion is the absence of the capability, and a regulatory justification doesn't change that, per the SKILL.md rule that a stated reason for a gap does not close the gap. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1–S6).
