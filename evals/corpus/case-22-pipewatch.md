# Case 22 — PipeWatch

**Industry:** Oil & gas (pipeline monitoring)
**Type:** seeded
**Device count:** 400

## Deployment Plan

PipeWatch deploys 400 pressure and leak-detection sensors along a regional pipeline network, connected via a mix of licensed radio and cellular backhaul to a regional SCADA gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the SCADA gateway. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. For field technician access during commissioning and maintenance, each unit's local diagnostic port uses a single default password set at the factory, which the commissioning team has generally not rotated because coordinating unique passwords across 400 remote, hard-to-access units seemed impractical. Certificates are issued at manufacturing for backend authentication; the plan does not describe any expiry monitoring or renewal process for them.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Single factory-set default password, unrotated, shared across all 400 units' diagnostic ports — direct shared-credential match. |
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described for units issued at manufacturing. |
| COMPOUND(S1,S4) | CRITICAL | A shared, unrotated diagnostic credential combined with no certificate rotation process means both the human-facing and machine-facing trust anchors for this fleet are simultaneously weak, on safety-relevant pipeline infrastructure. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S2, S3, S5, S6).
