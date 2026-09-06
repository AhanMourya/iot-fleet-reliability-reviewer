# Case 20 — TransitCount

**Industry:** Public transit
**Type:** clean
**Device count:** 600

## Deployment Plan

TransitCount deploys 600 passenger-occupancy counters on buses across a metropolitan transit fleet, connected via LTE, publishing occupancy counts every 3 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the vehicle's onboard telematics system. The root filesystem is read-only with an overlay, with brownout detection for the vehicle's 12V power system. Firmware updates are staged (a small pilot fleet, then a route, then the full fleet), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each counter has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated API only. A post-update health check verifies network reachability and a service heartbeat before marking an update successful, though the plan doesn't specify a timeout for that check. The plan does not describe any device status/heartbeat mechanism during normal (non-update) operation beyond the routine 3-minute publish.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O4 | HIGH | Post-update health check exists but no timeout is specified; a hung (not crashed) device could sit un-rolled-back indefinitely since the check never resolves to a failure. |
| C5 | ADVISORY | No liveness/heartbeat mechanism outside the routine publish interval; observability gap only. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P5, O1–O3, O5, S1–S6).
