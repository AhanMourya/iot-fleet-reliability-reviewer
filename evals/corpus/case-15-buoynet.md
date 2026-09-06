# Case 15 — BuoyNet

**Industry:** Marine / ocean monitoring
**Type:** clean
**Device count:** 25

## Deployment Plan

BuoyNet deploys 25 ocean monitoring buoys (temperature, salinity, wave height) off a coastal research station, connected via satellite modem publishing every 15 minutes via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 5 days with overflow alerting, and a status topic distinguishes hung buoys from healthy but quiet ones. Devices have a hardware watchdog. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery system, and there's no remote power-cycle path given the offshore deployment, but the watchdog is expected to catch the large majority of hang scenarios based on our bench testing. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each buoy has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. The plan does not describe any reset-count tracking or escalation if the watchdog ends up resetting a buoy repeatedly in a short window.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P4 | HIGH | Explicitly no remote power-cycle capability, despite the plan's compensating rationale (watchdog coverage from bench testing) — the taxonomy's evidence-missing criterion is the absence of the capability itself, not the absence of a stated reason for it. Watchdog presence is a separate pattern (P3) and doesn't substitute for P4. |
| P5 | HIGH | Watchdog is present, but no reset-loop detection or escalation described; a persistent bad state could cause repeated resets that look like intermittent connectivity rather than a clear, alertable failure. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P2, P3, O1–O5, S1–S6).
