# Case 16 — SiteTrack

**Industry:** Construction
**Type:** clean
**Device count:** 400

## Deployment Plan

SiteTrack deploys 400 equipment-tracking tags on tools and heavy equipment across active construction sites, connected over a mix of site WiFi and cellular, publishing location every 5 minutes via MQTT with exponential backoff and jitter on reconnect; the plan does not state whether this MQTT traffic is sent over TLS or plain. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung tags from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the site gateway. The root filesystem is read-only with an overlay, with brownout detection for the battery system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each tag has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Client/connection identifiers for the MQTT sessions are described only as "assigned during provisioning," without stating whether they're derived from a guaranteed-unique hardware identifier or a sequentially assigned value from a shared pool.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C3 | HIGH | Client ID assignment described vaguely ("assigned during provisioning") without confirming derivation from a unique hardware identifier; per the rubric's vague-description principle, treated as unverified rather than adequate. |
| S5 | HIGH | No mention of transport encryption (TLS/MQTTS) for the MQTT traffic; explicitly unstated either way. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1, C2, C4, C5, P1–P5, O1–O5, S1–S4, S6).
