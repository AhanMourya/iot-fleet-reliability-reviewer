# Case 42 — RailSentry

**Industry:** Railways (track/signal monitoring)
**Type:** seeded
**Device count:** 340

## Deployment Plan

RailSentry deploys 340 track-condition and signal-status sensors along a regional rail corridor, connected via a mix of trackside fiber and cellular backup to a control center, publishing every 10 seconds via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the trackside cabinet's control unit. The root filesystem is read-only with an overlay, with brownout detection for the cabinet's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each trackside cabinet's local maintenance terminal uses a single default technician password set at the factory, which has not been rotated since installation because coordinating a password change across the corridor's cabinets was deprioritized during initial rollout. Certificates for backend authentication are issued at manufacturing; the plan does not describe any expiry monitoring or renewal process.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Single factory-default technician password, unrotated, shared across all trackside cabinets — direct shared-credential match on safety-relevant rail infrastructure. |
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described. |
| COMPOUND(S1,S4) | CRITICAL | Both human-facing and machine-facing trust anchors are weak simultaneously on infrastructure where a compromise has direct safety implications for rail signaling. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S2, S3, S5, S6).
