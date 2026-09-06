# Case 89 — CartBot

**Industry:** Food delivery robotics (sidewalk delivery robot fleet)
**Type:** seeded
**Device count:** 500

## Deployment Plan

CartBot deploys 500 sidewalk delivery robots across several university and business campuses, connected via LTE-M publishing every 10 seconds during operation via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the robot's own control board. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Each robot has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Every robot ships with the same factory-default administrative password for the local maintenance interface used by field technicians to service the robot's compartment lock and drive system, and operations staff have not established a per-unit or per-region rotation process. Separately, each robot also exposes a Bluetooth diagnostic mode that stays continuously active (not just during active service sessions) and is reachable by anyone with a BLE-capable phone standing near the robot.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Same factory-default administrative password shipped on every robot, no rotation process — direct shared-credential match at 500-unit scale, with unusually high stakes given control over compartment locks and drive systems. |
| S2 | HIGH | Continuously-active BLE diagnostic mode reachable by proximity — High rather than Critical since exploitation requires physical proximity rather than internet reachability. |
| COMPOUND(S1,S2) | CRITICAL | A proximity-reachable diagnostic interface combined with a universal factory-default password gives anyone near a robot a plausible path to tampering with its compartment lock or drive system. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S3–S6).
