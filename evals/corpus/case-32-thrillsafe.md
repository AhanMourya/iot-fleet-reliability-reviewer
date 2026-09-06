# Case 32 — ThrillSafe

**Industry:** Amusement parks (ride safety sensors)
**Type:** clean
**Device count:** 30

## Deployment Plan

ThrillSafe deploys 30 stress and vibration sensors on major rides across an amusement park, connected over the park's dedicated safety-systems network to a ride-control gateway, publishing every second during operation via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 8 hours with overflow alerting, and a status topic with a short timeout flags a sensor as unreachable quickly, which matters given the safety context. Devices have a hardware watchdog and remote power-cycle via the ride-control gateway. The root filesystem is read-only with an overlay, with brownout detection for the sensor's power supply. Firmware updates are staged (a single ride, then all rides of that type, then the full park) with a defined post-update health check and automatic A/B rollback on a confirmed A/B-capable bootloader; update binaries are signed and verified on-device. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any reset-count tracking or escalation if the watchdog ends up resetting a sensor repeatedly in a short window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P5 | HIGH | Watchdog is present, but no reset-loop detection or escalation described; a persistent bad state could cause repeated resets that read as intermittent rather than a clear, alertable failure — worth flagging precisely because this is a safety-relevant sensor category even though the taxonomy's severity default here is structural, not context-driven. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C4, P1–P4, O1–O5, S1–S6).
