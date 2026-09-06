# Case 47 — WildWatch

**Industry:** Zoos & aquariums (enclosure environmental monitoring)
**Type:** seeded
**Device count:** 110

## Deployment Plan

WildWatch deploys 110 water quality, temperature, and air quality sensors across enclosures at a zoo and aquarium campus, connected over the campus's dedicated WiFi to a facilities gateway, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. To simplify provisioning across the large number of enclosure sensors, every unit deployed in a given exhibit zone (aquatics, mammals, reptiles) shares a single device certificate specific to that zone, rather than each sensor having its own unique certificate, since zone-level identity was judged sufficient for the facility's monitoring needs.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S3 | CRITICAL | Certificate shared across all sensors within a zone rather than unique per device — extraction from one sensor allows impersonating any sensor in that zone (potentially dozens of units) to backend services. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1, S2, S4–S6).
