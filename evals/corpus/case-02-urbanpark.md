# Case 02 — UrbanPark

**Industry:** Smart city / municipal parking
**Type:** seeded
**Device count:** 800

## Deployment Plan

UrbanPark deploys 800 in-ground parking occupancy sensors across a downtown district, communicating over a low-power WiFi mesh to neighborhood gateways, then to our backend via MQTT/TLS. Each sensor has a unique certificate provisioned at manufacturing, with expiry monitoring and 60-day-out renewal. Sensors have a hardware watchdog and a battery-backed RTC. Local buffering holds 12 hours of state-change events with overflow alerting. Client IDs are derived from each unit's hardware MAC address. On startup, the device establishes its MQTT session and begins publishing; the plan does not describe any behavior for what happens if that session drops after startup — connectivity is treated as a fixed condition of the mesh, not something the device needs to actively manage. Firmware updates are staged and signature-verified, with automatic A/B rollback on health-check failure. No debug interfaces are exposed; management is via an authenticated backend API only.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| C1 | CRITICAL | No reconnect/fallback logic described at all — a mesh-wide outage (a single common trigger) would leave sensors permanently disconnected until physically serviced, matching the rubric's canonical Critical example. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C2–C5, P1–P5, O1–O5, S1–S6). Note: C2/C3 evidence is present but moot given C1's absence of any reconnect logic to apply backoff/jitter to — scored as no-gap since the plan's stated mechanisms (jitter-ready client ID scheme) would be adequate if reconnect existed.
