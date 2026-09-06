# Case 30 — VoltDock — Reviewer Run

[CRITICAL] OTA
Finding: No rollback or A/B update path
Evidence: Plan states firmware is pushed "as full binary replacements to the charge-controller MCU's single application partition."
Risk: A failed update takes a charging station offline until a technician visit, with real revenue impact at network scale.
Recommended mitigation: Move to A/B partitioning if the hardware generation supports it (see next finding).
Confidence: HIGH
PatternID: O1

[CRITICAL] OTA
Finding: No documented bootloader support for dual-partition updates
Evidence: Plan states explicitly: "this MCU generation's bootloader has no documented support for dual-partition (A/B) updates."
Risk: The rollback gap above cannot be closed by a future software update alone for this hardware generation.
Recommended mitigation: Treat as a hardware-selection issue for future station generations; for the current generation, minimize update frequency and maximize pre-deployment testing.
Confidence: HIGH
PatternID: O5

[CRITICAL] OTA
Finding: [COMPOUND] No rollback path combined with no bootloader support for one means this station generation is permanently limited to physical-recovery-only updates
Evidence: Builds on the no-rollback finding and the no-bootloader-support finding above.
Risk: A materially worse and permanent outcome versus either finding alone, at 900-station network scale.
Recommended mitigation: See both component findings; inform hardware selection for future generations.
Confidence: HIGH
PatternID: COMPOUND(O1,O5)

Findings: 3 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 18 showed no gap).
