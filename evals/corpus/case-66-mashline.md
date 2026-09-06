# Case 66 — MashLine

**Industry:** Beverage manufacturing (brewery/distillery process monitoring)
**Type:** seeded
**Device count:** 95

## Deployment Plan

MashLine deploys 95 temperature, pressure, and fermentation-monitoring sensors across a brewery and distillery's production lines, connected over the facility's dedicated industrial network to a process-control gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the process-control gateway. The root filesystem is read-only with an overlay, with brownout detection for the facility's power supply. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed to all sensors on a production line simultaneously via a script that overwrites the current application binary and restarts the monitoring service; there is no fallback partition to revert to if a bad update disrupts a sensor mid-batch, so recovery requires a technician to manually reflash the affected units, potentially mid-fermentation.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Explicit single-partition overwrite update with no fallback; a bad push could disrupt process monitoring mid-batch with no remote recovery — direct product-quality and batch-loss consequence. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O5, S1–S6).
