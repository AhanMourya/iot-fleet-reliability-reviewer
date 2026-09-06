# Case 08 — HomeGuard

**Industry:** Home security (DIY / consumer)
**Type:** seeded
**Device count:** 5000

## Deployment Plan

HomeGuard is a consumer DIY security kit (door/window sensors, a base station) shipping to 5,000 households in its initial run. The base station connects to the customer's home WiFi and communicates with our backend over MQTT/TLS, with exponential backoff and jitter on reconnect, unique client IDs per unit, local buffering of 24 hours with overflow alerting, a hardware watchdog, and a battery-backed RTC. Firmware updates are staged and signature-verified with A/B rollback. Each base station ships with the same factory-set administrator password for its local setup web UI (used during initial WiFi configuration), which we don't currently prompt customers to change after setup completes. For remote support, we also leave a Telnet service enabled on the base station by default so our support team can connect directly if a customer calls in with connectivity issues — this is reachable from the internet since customers' home routers commonly forward the relevant port automatically via UPnP.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Same factory-set admin password shipped on every unit, never prompted to rotate — direct match to the canonical Mirai-pattern shared-credential case. |
| S2 | CRITICAL | Telnet enabled by default and explicitly stated as commonly internet-reachable via UPnP — this is the confirmed-internet-facing-exposure case that escalates S2 from its High default to Critical per the rubric's own worked example. |
| COMPOUND(S1,S2) | CRITICAL | An internet-reachable Telnet service combined with a shared, unrotated password is close to the literal Mirai attack pattern — remote, automatable, fleet-wide compromise. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S3–S6).
