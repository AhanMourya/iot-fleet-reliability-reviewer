# Case 25 — PortContain

**Industry:** Maritime shipping (container tracking)
**Type:** seeded
**Device count:** 3000

## Deployment Plan

PortContain deploys 3,000 GPS/condition tracking tags on shipping containers, connected via satellite modem while at sea and cellular while in port, publishing every 20 minutes via MQTT/TLS. Client IDs are derived from unique hardware serials. Devices have a hardware watchdog with reset-loop escalation, a remote power-cycle relay, and a battery-backed RTC. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each tag has a unique certificate with automated expiry monitoring and renewal. No debug interfaces are exposed. When a tag loses its satellite or cellular link, the onboard client retries the connection immediately and continuously on a fixed 2-second interval with no increasing delay. Readings generated while disconnected — which, given multi-week ocean transits, can be a substantial portion of a container's journey — are not stored locally; the plan states only that "the tag resumes normal reporting once connectivity returns."

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C2 | HIGH | Fixed 2-second retry with no backoff or jitter; fleet-wide-capable trigger (a satellite constellation or regional cellular outage) with a working but unmanaged recovery path. |
| C4 | HIGH | Explicitly no local buffering; given multi-week ocean transits are the normal operating mode (not an edge case), this is a routine, expected, and substantial data-loss condition, not a rare tail event. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C3, C5, P1–P5, O1–O5, S1–S6).
