# Case 28 — StayGuard

**Industry:** Hospitality (hotel room smart locks/occupancy)
**Type:** seeded
**Device count:** 8000

## Deployment Plan

StayGuard is a smart lock and room-occupancy sensor system deployed across an 8,000-room hotel chain, with each lock connecting to the property's WiFi and publishing status via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation, a battery-backed RTC, and remote power-cycle via the property's door controller network. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each lock is provisioned during installation with the property's standard maintenance-mode PIN — the same 4-digit code shipped on every lock from the factory — which front-desk and housekeeping staff use to override a lock if a guest is having trouble, and properties have generally kept the factory default rather than setting a property-specific code. Separately, each lock exposes a Bluetooth pairing mode for firmware diagnostics that stays active continuously rather than only during an active maintenance session, and is reachable by anyone with a BLE-capable phone standing near the door.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Same factory-default maintenance PIN shipped on every lock, generally never rotated — direct shared-credential match, with unusually high real-world stakes (physical room access). |
| S2 | HIGH | Continuously-active BLE diagnostic pairing mode, reachable by proximity rather than restricted to an active maintenance session — an exposed debug interface; scored High rather than Critical since exploitation requires physical proximity rather than being internet-reachable, per the rubric's exposure-confirmation distinction. |
| COMPOUND(S1,S2) | CRITICAL | A proximity-reachable diagnostic interface combined with a universal factory-default override PIN gives anyone briefly near a door a plausible path to overriding the lock — the combination is materially worse than either finding in isolation for a physical-security product. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S3–S6).
