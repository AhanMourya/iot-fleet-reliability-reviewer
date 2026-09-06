# Case 10 — MeterPilot

**Industry:** Energy / utility
**Type:** seeded
**Device count:** 1000

## Deployment Plan

MeterPilot is a 1,000-unit smart electricity meter pilot, mains-powered with a small internal capacitor for graceful shutdown, connected via a mix of cellular and powerline communication to a regional data collector, then MQTT/TLS to our backend. Reconnect uses exponential backoff and jitter, client IDs are derived from unique hardware serials, and local buffering covers 24 hours with overflow alerting. Devices have a hardware watchdog with reset-loop escalation and are remotely power-cyclable via the collector. The root filesystem is read-only with an overlay. Each meter has a unique certificate with expiry monitoring and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed as full binary replacements to the meter's single application partition; the metering MCU in this hardware generation does not have a documented dual-partition (A/B) bootloader, so there is no fallback slot to revert to if an update fails — a bad update requires a technician visit to reflash the meter via its physical maintenance port.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | No rollback/A-B path — explicit single-partition overwrite update. |
| O5 | CRITICAL | Explicitly states the hardware generation's bootloader has no documented A/B support — this is the foreclosure case: no future software update can retrofit rollback capability without different hardware or physical re-provisioning. |
| COMPOUND(O1,O5) | CRITICAL | O1's gap can never be closed in software given O5's hardware constraint — the combination means this meter generation is permanently limited to physical-recovery-only updates, a materially worse and specifically evidenced outcome than either finding alone. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O4, S1–S6).
