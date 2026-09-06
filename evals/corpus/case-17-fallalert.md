# Case 17 — FallAlert

**Industry:** Elder care (fall-detection wearables)
**Type:** clean
**Device count:** 1200

## Deployment Plan

FallAlert deploys 1,200 wrist-worn fall-detection devices for residents across a network of assisted-living facilities, connecting via BLE to a per-room gateway then MQTT/TLS to our backend, with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials, and each device pairs to its gateway using a unique per-device pairing key generated at provisioning. Local buffering covers 12 hours with overflow alerting, and a status topic with a short timeout flags a device as unreachable quickly, which matters for this use case. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the room gateway. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed; management is via an authenticated, per-facility-scoped API. Each device has a unique certificate issued at provisioning and a battery-backed RTC; the plan does not describe any process for monitoring certificate expiry or renewing certificates before they lapse.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described; on expiry, devices would simultaneously lose backend authentication, and for a fall-detection use case the safety consequence of a silent, undetected outage is severe even though the taxonomy's default severity here is driven by the fleet-wide-simultaneous-trigger structure, not the specific safety context. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5, S6).
