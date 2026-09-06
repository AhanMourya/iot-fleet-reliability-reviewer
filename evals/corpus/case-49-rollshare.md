# Case 49 — RollShare

**Industry:** Micromobility (bike/scooter share fleet)
**Type:** seeded
**Device count:** 4000

## Deployment Plan

RollShare deploys 4,000 GPS/lock units across a bike and scooter share fleet, connected via LTE-M publishing every 30 seconds while in use via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the unit's own control board. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Every unit ships with the same factory-default administrative password for the local maintenance interface used by field technicians to service the lock mechanism, and operations staff have not established a process to rotate it per-unit or per-region. Separately, each unit also exposes a Bluetooth diagnostic mode that stays continuously active (not just during active service sessions) and is reachable by anyone with a BLE-capable phone standing near the unit.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Same factory-default administrative password shipped on every unit, no rotation process — direct shared-credential match at 4,000-unit scale. |
| S2 | HIGH | Continuously-active BLE diagnostic mode reachable by physical proximity — an exposed debug interface; High rather than Critical since exploitation requires proximity rather than internet reachability. |
| COMPOUND(S1,S2) | CRITICAL | A proximity-reachable diagnostic interface combined with a universal factory-default password gives anyone near a unit a plausible path to tampering with lock mechanisms at fleet scale. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S3–S6).
