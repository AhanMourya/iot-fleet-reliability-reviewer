# Case 59 — SudsLine

**Industry:** Car wash equipment monitoring
**Type:** clean
**Device count:** 75

## Deployment Plan

SudsLine deploys 75 monitoring units across automated car wash bays for a regional chain, connected over each location's WiFi to a facility operations gateway, publishing every minute during operating hours via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facility gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are staged across locations, signature-verified, with an automatic A/B rollback path on a confirmed A/B-capable bootloader; a post-update health check verifies network reachability and a service heartbeat before marking an update successful, though the plan doesn't specify a timeout for that check.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O4 | HIGH | Post-update health check exists but no timeout specified; a hung (not crashed) device post-update could sit un-rolled-back indefinitely since the check never resolves to a failure. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O3, O5, S1–S6).
