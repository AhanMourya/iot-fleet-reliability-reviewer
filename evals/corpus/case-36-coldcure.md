# Case 36 — ColdCure

**Industry:** Pharmaceutical cold storage
**Type:** clean
**Device count:** 65

## Deployment Plan

ColdCure deploys 65 temperature and humidity sensors across pharmaceutical cold-storage warehouses, connected over each facility's dedicated network to a warehouse management gateway, publishing every 2 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for cold-chain compliance. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the facility's building management system. The root filesystem is read-only with an overlay, with brownout detection for the facility's UPS-backed power. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed; management is via an authenticated, facility-scoped API. Each sensor has a unique certificate issued at installation; the plan does not describe any process for monitoring certificate expiry or renewing certificates before they lapse.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described; on expiry, sensors would simultaneously lose backend authentication — for pharmaceutical cold-chain compliance monitoring, a silent authentication outage has direct regulatory and product-safety consequences, though the taxonomy's severity default here comes from the fleet-wide-simultaneous-trigger structure, not the compliance context specifically. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S3, S5, S6).
