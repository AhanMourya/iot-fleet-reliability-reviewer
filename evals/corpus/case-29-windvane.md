# Case 29 — WindVane

**Industry:** Renewable energy (wind turbine condition monitoring)
**Type:** seeded
**Device count:** 220

## Deployment Plan

WindVane deploys 220 vibration and temperature sensors across turbine nacelles at three wind farms, connected over each farm's dedicated industrial WiFi network to a SCADA gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Sensors are powered from the turbine's nacelle electronics bus; the plan does not describe any filesystem write-protection (read-only root, overlay, or equivalent) for local storage, and climbing to a nacelle to physically access a sensor is a multi-hour, weather-dependent undertaking with no remote power-cycle capability described as a fallback.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P1 | HIGH | No filesystem write-protection described; an unclean power event on the nacelle bus could corrupt local storage. Device-level (each sensor on its own turbine's bus, no shared circuit across turbines stated), so High rather than Critical. |
| P4 | HIGH | Explicitly no remote power-cycle capability, and physical access is unusually costly (multi-hour, weather-dependent nacelle climb) — the same structural gap as other cases, with a notably higher real-world remediation cost worth surfacing in Risk. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P2, P3, P5, O1–O5, S1–S6).
