# Case 77 — PaveMix

**Industry:** Construction materials (concrete/asphalt plant monitoring)
**Type:** clean
**Device count:** 40

## Deployment Plan

PaveMix deploys 40 batch-mix and temperature sensors across a concrete and asphalt production plant, connected over the plant's dedicated industrial network to a plant control gateway, publishing every 30 seconds during production via MQTT/TLS with exponential backoff and jitter on reconnect. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the plant control gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan describes client/connection identifiers only as "assigned when each sensor is commissioned," without confirming whether they're derived from a unique hardware identifier, and does not describe a status/heartbeat mechanism beyond the routine 30-second publish interval during production.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C3 | HIGH | Client ID assignment described vaguely ("assigned when each sensor is commissioned," not confirmed as hardware-derived); per the rubric's vague-description principle, scored at full taxonomy default severity with reduced confidence. |
| C5 | ADVISORY | No liveness/heartbeat mechanism beyond routine publishing; observability gap only. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C2, C4, P1–P5, O1–O5, S1–S6).
