# Case 41 — GroundLink

**Industry:** Aviation (airport ground support equipment)
**Type:** seeded
**Device count:** 130

## Deployment Plan

GroundLink deploys 130 telemetry units on baggage tugs, belt loaders, and pushback tractors across a regional airport's ground operations, connected over the airport's dedicated operations WiFi to a fleet management gateway, publishing every 15 seconds via MQTT/TLS. Client IDs are derived from unique hardware serials. Local buffering covers 8 hours with overflow alerting, and a status topic distinguishes hung units from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the gateway. The root filesystem is read-only with an overlay, with brownout detection for the vehicle's electrical system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each unit has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. On startup, each unit establishes its MQTT session and begins publishing; the tarmac's WiFi coverage has known dead zones near certain gates, and the plan does not describe any behavior for re-establishing the session if it drops after startup once a vehicle moves out of coverage and back in.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C1 | CRITICAL | No reconnect/fallback logic described; a known, acknowledged coverage gap (tarmac WiFi dead zones) is a routine, fleet-wide-capable trigger with no automatic recovery once vehicles move back into coverage. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C2–C5, P1–P5, O1–O5, S1–S6).
