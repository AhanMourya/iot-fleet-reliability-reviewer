# Case 53 — FrostCase

**Industry:** Grocery retail (cold case / freezer monitoring)
**Type:** clean
**Device count:** 320

## Deployment Plan

FrostCase deploys 320 temperature sensors across refrigerated cases and freezers in a grocery chain, connected over each store's dedicated network to a store operations gateway, publishing every 5 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for food-safety compliance. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the store's building management system. The root filesystem is read-only with an overlay. Firmware updates are staged (one store, then a region, then the chain), signature-verified, with automatic A/B rollback on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated weekly expiry checks and 60-day-out renewal, alerting store operations if a renewal fails, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated, store-scoped API. Power comes from the store's standard electrical circuits with no UPS backing for the sensors specifically, and the plan does not describe any device-level brownout/undervoltage detection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P2 | HIGH | No device-level brownout/undervoltage detection described, and power is explicitly not UPS-backed for these sensors specifically, unlike some other cases in this corpus where facility conditioning was cited as a partial justification — here there isn't even that. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P3–P5, O1–O5, S1–S6).
