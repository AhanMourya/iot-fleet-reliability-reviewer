# Case 24 — SkyDrop

**Industry:** Drone delivery
**Type:** seeded
**Device count:** 45

## Deployment Plan

SkyDrop operates a 45-drone delivery fleet across a suburban service area, with each drone connecting via LTE to our flight-operations backend over MQTT/TLS, exponential backoff and jitter on reconnect, and unique client IDs derived from hardware serials. Local buffering covers 2 hours of telemetry with overflow alerting, and a status heartbeat runs continuously during flight. Drones have a hardware watchdog with reset-loop escalation, and ground crew can remotely power-cycle a grounded drone via its charging dock. The root filesystem is read-only with an overlay, with brownout detection for the flight battery system. Each drone has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Flight-control firmware updates are pushed to all drones in the fleet during the nightly maintenance window; the update process downloads the new signed firmware image and writes it directly to the active flash partition, restarting the flight controller — there is no secondary partition to fall back to if the new firmware fails to pass its post-update self-test, so a bad update requires a technician to connect a maintenance cable and manually reflash the drone before it can fly again.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Explicit single-partition overwrite update with no fallback slot; a bad nightly push grounds the fleet with no remote recovery, on a safety-relevant platform where "grounded until a technician manually reflashes" has real operational cost. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O5, S1–S6).
