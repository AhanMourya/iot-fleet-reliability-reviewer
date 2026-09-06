# Case 05 — ShelfSense

**Industry:** Retail
**Type:** seeded
**Device count:** 2000

## Deployment Plan

ShelfSense is a 2,000-unit smart-shelf inventory sensor rollout across 40 grocery stores, using weight-sensing shelf strips connected over in-store WiFi to a per-store gateway, then MQTT/TLS to our backend. Client IDs are derived from unique hardware serials, and reconnect uses exponential backoff with jitter. Local buffering covers 4 hours with overflow alerting. Each device has a unique certificate with expiry monitoring and a battery-backed RTC. Devices have a hardware watchdog with reset-loop escalation, and a per-store gateway can remotely power-cycle any shelf strip on its network. No debug interfaces are exposed to the store network. Firmware updates are staged across stores (one store first, then a region, then all stores) with a defined post-update health check. The update pipeline downloads new firmware over HTTPS and applies it directly; we rely on the download being over a trusted, encrypted connection and haven't added a separate cryptographic signature check on the firmware binary itself.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O2 | CRITICAL | No signature verification of the firmware binary; explicit statement that HTTPS transport is relied on instead — matches the taxonomy's explicit distinction between transport security and image authenticity. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1, O3–O5, S1–S6).
