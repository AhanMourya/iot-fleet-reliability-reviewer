# Case 23 — AGVFleet

**Industry:** Warehouse robotics (automated guided vehicles)
**Type:** seeded
**Device count:** 60

## Deployment Plan

AGVFleet deploys 60 automated guided vehicles across a distribution warehouse, connected over the warehouse's dedicated WiFi network to a fleet coordination server, publishing telemetry every 5 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 4 hours with overflow alerting, and a status topic distinguishes hung vehicles from healthy but quiet ones. The root filesystem is read-only with an overlay, with brownout detection for the onboard battery system, and a remote power-cycle relay reachable from the coordination server. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each vehicle has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The onboard control software does not currently use a watchdog timer — the team has relied on the coordination server noticing a vehicle has stopped reporting telemetry and flagging it for manual review, rather than automatic on-device hang recovery.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P3 | HIGH | No watchdog timer described; a hung vehicle requires manual intervention (physical reset) even though the coordination server can detect the silence. Detection is not the same as recovery. |
| P5 | HIGH | No automated reset mechanism exists (see P3), so no reset-loop detection or escalation logic is described either — this becomes a live gap the moment a watchdog is added if not designed in alongside it. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P4, O1–O5, S1–S6).
