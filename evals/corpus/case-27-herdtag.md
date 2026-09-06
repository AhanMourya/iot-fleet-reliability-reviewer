# Case 27 — HerdTag

**Industry:** Livestock (cattle ear-tag tracking)
**Type:** seeded
**Device count:** 6000

## Deployment Plan

HerdTag deploys 6,000 solar-powered ear-tag tracking devices across several ranches, connected via LoRaWAN to farm gateways, then MQTT/TLS to our backend, with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 72 hours with overflow alerting, and a status topic distinguishes hung tags from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. To keep unit cost low at this scale, every tag in a given production batch (typically 1,000–2,000 units) is provisioned with the same device certificate, rather than a certificate unique to each individual tag, since per-tag enrollment was judged too costly for a low-margin agricultural product. There is no remote power-cycle mechanism, but the watchdog is expected to handle the large majority of hang scenarios given the tag's simple firmware.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S3 | CRITICAL | Certificate shared across an entire production batch (1,000-2,000 units) rather than unique per device — extraction from one tag would allow impersonating every tag in that batch to backend services. |
| P4 | HIGH | Explicitly no remote power-cycle capability, regardless of the compensating watchdog rationale given — the taxonomy's evidence-missing criterion is the absence of the capability itself. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, P5, O1–O5, S1, S2, S4–S6).
