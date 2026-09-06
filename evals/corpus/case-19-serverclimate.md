# Case 19 — ServerClimate

**Industry:** Data center environmental monitoring
**Type:** clean
**Device count:** 80

## Deployment Plan

ServerClimate deploys 80 temperature and humidity sensors across server racks in two data center facilities, connected over the facility's dedicated management VLAN, publishing every minute via MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 6 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the rack PDU. The root filesystem is read-only with an overlay for writable state. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. Each sensor has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed; management is via an authenticated API scoped to the management VLAN. Power comes from the facility's conditioned UPS-backed circuits, and the plan does not describe any brownout/undervoltage detection on the sensor hardware itself, treating the facility's UPS infrastructure as sufficient protection against power quality issues.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| P2 | HIGH | No brownout/undervoltage detection on the device itself; facility-level UPS protects against full outages but doesn't guarantee the sensor never sees a marginal voltage condition (e.g., a PDU-level fault) that a device-level check would catch. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1, P3–P5, O1–O5, S1–S6).
