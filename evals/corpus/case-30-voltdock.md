# Case 30 — VoltDock

**Industry:** EV charging infrastructure
**Type:** seeded
**Device count:** 900

## Deployment Plan

VoltDock deploys 900 networked EV charging stations across a regional charging network, connected via cellular to our backend over MQTT/TLS with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 24 hours with overflow alerting, and a status topic distinguishes hung stations from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the station's own relay board. The root filesystem is read-only with an overlay, with brownout detection for the station's grid-tied power supply. Each station has a unique certificate with automated expiry monitoring and renewal, and a battery-backed RTC. No debug interfaces are exposed. Firmware updates are pushed as full binary replacements to the charge-controller MCU's single application partition; this MCU generation's bootloader has no documented support for dual-partition (A/B) updates, so a failed update leaves the station needing a technician visit to reflash it via the service port before it can charge vehicles again.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Explicit single-partition overwrite update process with no fallback slot. |
| O5 | CRITICAL | Explicitly no documented A/B bootloader support on this MCU generation — the foreclosure case: no future software fix can add rollback capability without different hardware or physical re-provisioning of all 900 stations. |
| COMPOUND(O1,O5) | CRITICAL | The rollback gap is permanent given the hardware constraint — every future firmware update to this generation carries the same unrecoverable risk, with real revenue impact (stations offline) at network scale. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O2–O4, S1–S6).
