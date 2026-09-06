# Case 87 — MethSense

**Industry:** Waste management (landfill gas monitoring)
**Type:** seeded
**Device count:** 130

## Deployment Plan

MethSense deploys 130 methane and landfill gas sensors across active and closed landfill cells, connected over a mix of licensed radio and cellular backhaul to a site operations gateway, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. No debug interfaces are exposed. To simplify provisioning across the large sensor count, every sensor deployed to a given landfill cell shares a single device certificate specific to that cell, rather than each sensor having its own unique certificate, since per-sensor enrollment was judged too costly relative to the deployment timeline.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S3 | CRITICAL | Certificate shared across all sensors within a landfill cell rather than unique per device — extraction from one sensor allows impersonating every sensor in that cell to backend services, on a gas-detection safety system. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S1, S2, S4–S6).
