# Case 21 — DeepGas

**Industry:** Mining (underground methane/gas detection)
**Type:** seeded
**Device count:** 180

## Deployment Plan

DeepGas deploys 180 methane and CO monitoring sensors throughout an underground coal mine's tunnel network, connected via a leaky-feeder radio system to surface relay points, publishing readings every 60 seconds via MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation, a remote power-cycle relay, and a battery-backed RTC. The root filesystem is read-only with an overlay, with brownout detection for the battery backup system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal. No debug interfaces are exposed. On startup, each sensor establishes its MQTT session and begins publishing; underground radio propagation is inherently unstable, and the plan does not describe any behavior for re-establishing the session if it drops after startup — the system was designed around the assumption that the leaky-feeder link, once up, stays up for the shift.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C1 | CRITICAL | No reconnect/fallback logic described; a radio propagation disruption (plausible and explicitly acknowledged as "inherently unstable") is a fleet-wide-capable trigger with no automatic recovery — for a gas-detection safety system, this is the canonical Critical pattern. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C2–C5, P1–P5, O1–O5, S1–S6).
