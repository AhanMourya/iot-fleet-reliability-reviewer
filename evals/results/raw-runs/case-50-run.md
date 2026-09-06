# Case 50 — SunField — Reviewer Run

[CRITICAL] OTA
Finding: No rollback or A/B update path
Evidence: Plan states firmware is pushed "as full binary replacements to the monitoring unit's single application partition."
Risk: A failed update requires a technician to physically visit the panel and reflash it — costly at 700-unit farm scale.
Recommended mitigation: Move to A/B partitioning if the hardware generation supports it (see next finding).
Confidence: HIGH
PatternID: O1

[CRITICAL] OTA
Finding: No documented bootloader support for dual-partition updates
Evidence: Plan states explicitly "this generation's MCU bootloader has no documented support for dual-partition (A/B) updates."
Risk: The rollback gap above cannot be closed by a future software update alone for this hardware generation.
Recommended mitigation: Treat as a hardware-selection issue for future monitoring unit generations.
Confidence: HIGH
PatternID: O5

[CRITICAL] OTA
Finding: [COMPOUND] No rollback path combined with no bootloader support for one means this generation is permanently limited to physical-recovery-only updates
Evidence: Builds on the no-rollback finding and the no-bootloader-support finding above.
Risk: A materially worse, permanent outcome at farm scale.
Recommended mitigation: See both component findings; inform hardware selection going forward.
Confidence: HIGH
PatternID: COMPOUND(O1,O5)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
