# Case 01 — ColdLink — Reviewer Run

[CRITICAL] OTA
Finding: Bootloader supports A/B partitioning, but the update tooling does not actually use it for rollback
Evidence: Plan states the bootloader is A/B-capable but "we haven't wired up the health-check failure to trigger the A/B partition swap yet, so a bad build still needs a manual re-push to revert."
Risk: A bad firmware push has no working automatic recovery despite capable hardware — every affected unit needs manual re-push, and at fleet scale this is effectively unrecoverable until someone notices and acts.
Recommended mitigation: Wire the existing health-check failure signal to trigger the A/B partition swap that the bootloader already supports.
Confidence: HIGH
PatternID: O1

[CRITICAL] OTA
Finding: No update image signature verification
Evidence: Plan states explicitly: "Update binaries aren't signed; we rely on HTTPS as the download transport for integrity."
Risk: A compromised build source or corrupted download would be applied as if legitimate, with no gate to catch it.
Recommended mitigation: Add on-device signature verification of update binaries, independent of transport security.
Confidence: HIGH
PatternID: O2

[CRITICAL] SECURITY
Finding: Shared password across the fleet for the local diagnostic web UI
Evidence: Plan states "drivers can reach a local diagnostic web UI over the trailer's WiFi using a single password shared across the whole fleet."
Risk: A single leaked or guessed password compromises the diagnostic interface on every trailer.
Recommended mitigation: Move to unique, per-device passwords (or per-technician credentials) for the diagnostic UI.
Confidence: HIGH
PatternID: S1

[CRITICAL] OTA
Finding: [COMPOUND] Unsigned builds combined with a non-functional rollback path leave a bad or malicious update with no gate and no way back
Evidence: Builds on the no-signature-verification finding and the non-functional-rollback finding above.
Risk: A bad build reaches production with nothing to catch it and no automatic recovery once installed.
Recommended mitigation: Prioritize wiring the existing A/B rollback and adding signature verification together.
Confidence: HIGH
PatternID: COMPOUND(O1,O2)

Findings: 4 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 17 showed no gap).
