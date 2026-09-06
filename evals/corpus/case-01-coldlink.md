# Case 01 — ColdLink

**Industry:** Cold-chain logistics
**Type:** seeded
**Device count:** 150

## Deployment Plan

ColdLink deploys 150 temperature/humidity loggers in refrigerated trailers, connected via LTE cellular. Devices publish readings every 2 minutes over MQTT/TLS. The cellular modem reconnects with exponential backoff and jitter after drops. Client IDs are derived from each modem's IMEI, guaranteeing uniqueness. Devices buffer up to 24 hours of readings locally with alerting if the buffer overflows. A hardware watchdog resets hung devices, with reset-count tracking that triggers an alert after 3 resets in an hour. A relay tied to the trailer's telematics unit allows remote power-cycling. Firmware updates are staged (5% → 25% → 100%) with a 10-minute post-update health check gate. The onboard MCU has a documented A/B-capable bootloader, but our current update tooling only writes the new binary to the active partition and restarts the service — we haven't wired the health-check failure to trigger an A/B partition swap yet, so a bad build still needs a manual re-push to revert. Update binaries aren't signed; we rely on HTTPS as the download transport for integrity. Each unit has a unique X.509 certificate issued at provisioning, with automated expiry monitoring and renewal. Devices have a battery-backed RTC. For field troubleshooting, drivers can reach a local diagnostic web UI over the trailer's WiFi using a single password shared across the whole fleet.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| O1 | CRITICAL | Bootloader supports A/B, but the update tooling doesn't use it — a bad push still requires manual recovery; no working rollback path as actually implemented. |
| O2 | CRITICAL | No signature verification; HTTPS integrity is not equivalent to source authentication. |
| S1 | CRITICAL | Single shared diagnostic-UI password across the fleet — direct match to S1 (human-facing admin credential). |
| COMPOUND(O1,O2) | CRITICAL | Unsigned build with no working rollback path — a bad or malicious build reaches production with no gate and no way back except manual re-push. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O3–O5, S2–S6).
