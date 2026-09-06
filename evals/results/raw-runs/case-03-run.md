# Case 03 — VitalBand — Reviewer Run

[CRITICAL] SECURITY
Finding: Shared BLE pairing key across the entire batch of bands
Evidence: Plan states explicitly: "a shared BLE pairing key that is identical across all 500 units in this batch."
Risk: Extraction of the key from one band would allow impersonating any band to any gateway in the fleet.
Recommended mitigation: Move to unique per-device pairing keys generated at provisioning, even at added manufacturing cost.
Confidence: HIGH
PatternID: S3

[HIGH] SECURITY
Finding: Gateway-to-backend hop uses unencrypted transport
Evidence: Plan states explicitly: "the gateway-to-backend hop uses plain HTTP."
Risk: Patient vitals data is exposed to interception by anyone in a position on that network path.
Recommended mitigation: Move the gateway-to-backend hop to HTTPS/TLS.
Confidence: HIGH
PatternID: S5

[CRITICAL] SECURITY
Finding: [COMPOUND] Shared pairing key combined with an unencrypted backend hop compounds exposure of patient health data
Evidence: Builds on the shared-pairing-key finding and the unencrypted-transport finding above.
Risk: Both device-layer impersonation and backend-hop interception are live simultaneously for a health-data pilot.
Recommended mitigation: Prioritize per-device pairing keys and TLS on the backend hop together.
Confidence: MEDIUM
PatternID: COMPOUND(S3,S5)

Findings: 2 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
