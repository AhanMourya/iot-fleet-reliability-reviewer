# Case 12 — ArtifactGuard

**Industry:** Museum / cultural heritage
**Type:** clean
**Device count:** 40

## Deployment Plan

ArtifactGuard deploys 40 climate sensors (temperature, humidity, UV) in display cases and storage rooms at a regional museum, connected over the museum's WiFi to a local gateway, publishing every 10 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 48 hours with overflow alerting, and a keep-alive/status topic distinguishes a silently hung device from a healthy one. Devices have a hardware watchdog with reset-loop escalation and a remote power-cycle relay. The root filesystem is read-only with an overlay, with brownout detection halting writes before critical voltage. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal. No debug interfaces are exposed. The plan does not mention a battery-backed RTC or any early-boot time-sync strategy for certificate validation.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S6 | HIGH | No mention of a battery-backed RTC or trusted early time source; a power event could leave a unit unable to validate certificates until time sync completes. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1–S5).
