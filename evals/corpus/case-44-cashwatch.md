# Case 44 — CashWatch

**Industry:** Banking (ATM fleet monitoring)
**Type:** seeded
**Device count:** 600

## Deployment Plan

CashWatch deploys 600 monitoring units across a regional bank's ATM fleet, tracking cash levels, mechanical status, and physical tamper sensors, connected via cellular to our backend over MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the ATM's own control board. The root filesystem is read-only with an overlay, with brownout detection for the ATM's UPS-backed power. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are staged (a branch pilot group, then the full fleet) with a defined post-update health check. The update pipeline downloads new firmware over an internal HTTPS distribution service and applies it directly to the monitoring unit; there is no cryptographic signature verification of the firmware binary beyond the transport-level HTTPS connection.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O2 | CRITICAL | No signature verification of the firmware binary; explicit reliance on HTTPS transport alone. On ATM infrastructure with direct financial and physical-security relevance, a compromised or corrupted firmware push is a serious exposure with no gate to catch it. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1, O3–O5, S1–S6).
