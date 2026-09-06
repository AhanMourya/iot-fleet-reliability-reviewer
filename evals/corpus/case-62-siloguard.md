# Case 62 — SiloGuard

**Industry:** Agriculture (grain silo monitoring)
**Type:** seeded
**Device count:** 280

## Deployment Plan

SiloGuard deploys 280 grain moisture, temperature, and CO2 sensors across a network of grain storage silos, connected over a mix of farm WiFi and LoRaWAN to regional gateways, then MQTT/TLS to our backend with exponential backoff and jitter on reconnect. Client IDs are derived from unique hardware serials. Local buffering covers 48 hours with overflow alerting, and a status topic distinguishes hung sensors from healthy but quiet ones. Devices have a hardware watchdog with reset-loop escalation and remote power-cycle via the regional gateway. The root filesystem is read-only with an overlay, with brownout detection for the solar/battery power system. Firmware updates are staged, signature-verified, with A/B rollback on a defined health-check gate on a confirmed A/B-capable bootloader. For field technician access, each silo's local sensor hub uses a single default password set at installation, which has not been rotated across the network because the installing contractor used one standard configuration image for all sites. Certificates for backend authentication are issued at manufacturing; the plan does not describe any expiry monitoring or renewal process.

## Ground Truth

| Pattern ID | Severity | Rationale |
|---|---|---|
| S1 | CRITICAL | Single default password from a standard configuration image, unrotated across the network — direct shared-credential match; grain storage CO2/moisture sensing has real safety relevance (silo atmosphere hazards). |
| S4 | CRITICAL | No certificate expiry monitoring or renewal process described. |
| COMPOUND(S1,S4) | CRITICAL | Both trust anchors weak simultaneously across the sensor network. |

All other patterns: no expected finding (plan gives explicit adequate evidence for C1–C5, P1–P5, O1–O5, S2, S3, S5, S6).
