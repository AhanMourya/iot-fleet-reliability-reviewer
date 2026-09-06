# Case 82 — FlowGuard

**Industry:** Municipal water utility (fresh water distribution/leak detection)
**Type:** seeded
**Device count:** 550

## Deployment Plan

FlowGuard deploys 550 pressure and flow sensors across a municipal fresh water distribution network, connected over a mix of licensed radio and cellular backhaul to a water utility SCADA gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the SCADA gateway. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. For field technician access, each sensor's local diagnostic port uses a single default password set at the factory, which the utility's maintenance contractor has not rotated because coordinating unique passwords across 550 remote valve-pit locations was judged impractical. Certificates for backend authentication are issued at manufacturing; the plan does not describe any expiry monitoring or renewal process.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Single factory-default password, unrotated, shared across all 550 units' diagnostic ports — direct shared-credential match on public water infrastructure. |
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described. |
| COMPOUND(S1,S4) | CRITICAL | Both human-facing and machine-facing trust anchors weak simultaneously on infrastructure with public-safety relevance. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S2, S3, S5, S6).
