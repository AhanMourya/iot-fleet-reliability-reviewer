# Case 76 — CellarWatch

**Industry:** Wine storage (cellar climate control)
**Type:** clean
**Device count:** 55

## Deployment Plan

CellarWatch deploys 55 temperature and humidity sensors across climate-controlled wine cellars for a distribution company, connected over each facility's WiFi to a facilities operations gateway, publishing every 10 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters for protecting high-value inventory. Devices have a hardware watchdog and remote power-cycle via the facilities gateway. The root filesystem is read-only with an overlay, with brownout detection for the power supply. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any reset-count tracking or escalation if the watchdog ends up resetting a sensor repeatedly in a short window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P5 | HIGH | Watchdog is present, but no reset-loop detection or escalation described; a persistent bad state causing repeated resets could look like intermittent connectivity rather than a clear, alertable failure — meaningful here given high-value, climate-sensitive inventory. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P4, O1–O5, S1–S6).
