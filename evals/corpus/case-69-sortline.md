# Case 69 — SortLine

**Industry:** Postal & logistics (package sorting facility)
**Type:** seeded
**Device count:** 320

## Deployment Plan

SortLine deploys 320 barcode-scanning and jam-detection sensors across a regional package sorting facility, connected over the facility's dedicated industrial network to a sortation control gateway, publishing continuously via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the control gateway. The root filesystem is read-only with an overlay, with brownout detection for the facility's power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Every sensor's local diagnostic interface uses the same default password set at the factory, which the maintenance team has kept unchanged because a single memorized password made shift-to-shift troubleshooting simpler across the facility's 320 units. Separately, each sensor also exposes a Telnet-based remote diagnostic service that stays enabled continuously and is reachable from the facility's general IT network, which itself has a routed (non-isolated) path to the corporate network and, from there, the internet.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Same factory-default password kept unchanged across all 320 sensors — direct shared-credential match. |
| S2 | CRITICAL | Telnet service enabled continuously and reachable via a routed path from the general IT network to the internet — this is the confirmed-internet-reachable case that escalates S2 from its High default to Critical per the rubric's own worked example, even though the path is indirect (via IT network routing) rather than a direct port-forward. |
| COMPOUND(S1,S2) | CRITICAL | An internet-reachable Telnet service combined with a shared, unrotated password closely mirrors the Mirai attack pattern, on facility infrastructure that could disrupt package sortation at scale if compromised. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S3–S6).
