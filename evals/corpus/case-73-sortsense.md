# Case 73 — SortSense

**Industry:** Waste & recycling (facility sorting sensors)
**Type:** clean
**Device count:** 95

## Deployment Plan

SortSense deploys 95 material-classification and jam-detection sensors across a recycling sorting facility, connected over the facility's dedicated industrial network to a sortation control gateway, publishing continuously via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-count tracking that escalates to an alert after repeated resets, and remote power-cycle via the control gateway. The root filesystem is read-only with an overlay. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Power is provided from the facility's standard industrial circuits; the plan does not describe any device-level brownout/undervoltage detection, and the facility's power quality is noted as "variable given the heavy equipment sharing the same circuits."

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P2 | HIGH | No device-level brownout/undervoltage detection described, and the plan itself flags the facility's power quality as variable due to shared heavy-equipment circuits — an explicit aggravating factor rather than a neutral absence. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P3–P5, O1–O5, S1–S6).
