# Case 35 — ShelfTrace

**Industry:** Public libraries (RFID asset tracking)
**Type:** clean
**Device count:** 20

## Deployment Plan

ShelfTrace deploys 20 RFID reader gateways across branches of a public library system to track equipment and high-value materials, connected over each branch's WiFi to our backend via MQTT/TLS with exponential backoff and jitter on reconnect. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via a smart plug at each branch. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each reader has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe a status/heartbeat mechanism beyond the routine publish interval, and describes client/connection identifiers only as "configured per branch during setup," without confirming whether they're derived from a unique hardware identifier or assigned from a shared per-branch pool.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C3 | HIGH | Client ID assignment described vaguely ("configured per branch," not confirmed as hardware-derived); per the rubric's vague-description principle, scored at full taxonomy default severity with reduced confidence, not a lower severity. |
| C5 | ADVISORY | No liveness/heartbeat mechanism beyond routine publishing; observability gap only. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C2, C4, P1–P5, O1–O5, S1–S6).
