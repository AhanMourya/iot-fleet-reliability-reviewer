# Case 10 — MeterPilot — Reviewer Run

[CRITICAL] OTA
Finding: No rollback or A/B update path
Evidence: Plan states explicitly: firmware is "pushed as full binary replacements to the meter's single application partition."
Risk: A bad update requires a technician visit to physically reflash the meter, with no remote recovery.
Recommended mitigation: Move to A/B partitioning if the hardware supports it (see next finding).
Confidence: HIGH
PatternID: O1

[CRITICAL] OTA
Finding: Hardware bootloader has no documented A/B support
Evidence: Plan states explicitly: "the metering MCU in this hardware generation does not have a documented dual-partition (A/B) bootloader."
Risk: The rollback gap above cannot be closed by a future software update alone — only by different hardware or physical re-provisioning of all 1,000 meters.
Recommended mitigation: Treat this as a hardware selection issue for future meter generations; for the current generation, minimize update frequency and maximize pre-deployment testing rigor to compensate.
Confidence: HIGH
PatternID: O5

[CRITICAL] OTA
Finding: [COMPOUND] No rollback path combined with a bootloader that cannot support one means this meter generation is permanently limited to physical-recovery-only updates
Evidence: Builds on the no-rollback finding and the no-bootloader-support finding above.
Risk: A materially worse and permanent outcome versus either finding alone.
Recommended mitigation: See both component findings; this combination should inform hardware selection for the next meter generation.
Confidence: HIGH
PatternID: COMPOUND(O1,O5)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
