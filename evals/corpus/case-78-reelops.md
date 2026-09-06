# Case 78 — ReelOps

**Industry:** Entertainment (movie theater equipment monitoring)
**Type:** clean
**Device count:** 130

## Deployment Plan

ReelOps deploys 130 projector, HVAC, and access-control sensors across a regional movie theater chain, connected over each theater's WiFi to a facilities operations gateway, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged (one theater, then a region, then the chain), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting facilities staff if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, chain-scoped API. There is no remote power-cycle mechanism for these sensors — projector booth equipment sits on a separate electrical subpanel that theater staff have chosen not to network for power control, so recovering a hung sensor requires a staff member to physically reset it during a booth check.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | Explicitly no remote power-cycle capability; the operational choice not to network the subpanel is a stated reason, but per SKILL.md's rule that a stated reason for a gap does not close the gap, this is still scored as a finding — the capability itself is absent regardless of why. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1–S6).
