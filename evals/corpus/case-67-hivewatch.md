# Case 67 — HiveWatch

**Industry:** Apiculture (beekeeping/apiary monitoring)
**Type:** seeded
**Device count:** 900

## Deployment Plan

HiveWatch deploys 900 hive-weight, temperature, and acoustic sensors across apiaries for a commercial beekeeping operation, connected via LoRaWAN to regional gateways, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 72 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. To simplify provisioning across the large sensor count, every sensor deployed to a given apiary location shares a single device certificate specific to that location, rather than each sensor having its own unique certificate, since per-sensor enrollment was judged too costly relative to the low per-unit value of these sensors.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S3 | CRITICAL | Certificate shared across all sensors at a given apiary location rather than unique per device — extraction from one sensor allows impersonating every sensor at that location to backend services. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1, S2, S4–S6).
