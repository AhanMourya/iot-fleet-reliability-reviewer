# Case 03 — VitalBand

**Industry:** Healthcare wearables
**Type:** seeded
**Device count:** 500

## Deployment Plan

VitalBand is a 500-unit pilot of wrist-worn vitals monitors (heart rate, SpO2) for post-discharge patient monitoring, worn for 30 days per patient. Bands connect via BLE to a bedside/home gateway, which relays data to our backend over MQTT. The BLE link uses the gateway's standard pairing flow; data from band to gateway is not separately encrypted beyond whatever the BLE stack provides by default, and the gateway-to-backend hop uses plain HTTP, since the data volume is small and we wanted to keep gateway compute minimal. Bands reconnect to the gateway automatically with backoff if the link drops, buffer up to 8 hours of readings locally, and use a watchdog with reset-loop escalation. Firmware updates are staged and signature-verified with automatic rollback. Each band authenticates to its paired gateway using a shared BLE pairing key that is identical across all 500 units in this batch, since per-device pairing keys added meaningful cost to the manufacturing run for this pilot size. Certificates for the gateway-to-backend hop are unique per gateway with expiry monitoring.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S3 | CRITICAL | Shared BLE pairing key across all 500 bands — a single extracted key allows impersonating any band to any gateway; same structure as a shared device-identity secret even though the mechanism (BLE pairing) differs from a certificate. |
| S5 | HIGH | Gateway-to-backend hop explicitly stated as plain HTTP; real, evidenced exposure of patient vitals data in transit. |
| COMPOUND(S3,S5) | CRITICAL | Shared pairing key plus unencrypted backend hop compounds exposure: patient data could be both impersonated at the device layer and intercepted at the backend hop, for a health-data pilot where both matter more than typical telemetry. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1, S2, S4, S6).
