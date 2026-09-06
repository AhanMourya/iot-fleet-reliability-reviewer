# Case 27 — HerdTag — Reviewer Run

[CRITICAL] SECURITY
Finding: Certificate shared across an entire production batch rather than unique per device
Evidence: Plan states explicitly: "every tag in a given production batch (typically 1,000-2,000
units) is provisioned with the same device certificate, rather than a certificate unique to each
individual tag."
Risk: Extraction of the certificate from one tag would allow impersonating every tag in that
batch to backend services.
Recommended mitigation: Move to per-tag unique certificates, even if it adds provisioning cost
at this scale.
Confidence: HIGH
PatternID: S3

[HIGH] POWER
Finding: No remote power-cycle capability
Evidence: Plan states explicitly there is "no remote power-cycle mechanism," and gives a
technical rationale ("the watchdog is expected to handle the large majority of hang scenarios
given the tag's simple firmware") for why this is considered acceptable. That rationale explains
awareness of the gap; it does not change whether the capability itself is present, which it is not.
Risk: Any hang class outside the "large majority" the watchdog is expected to catch has no
remote fallback and requires physical recovery of the affected tag.
Recommended mitigation: Given the fleet's remote, physically dispersed deployment, evaluate a
low-cost remote reset trigger; if truly infeasible at this unit cost, document the accepted
residual risk explicitly rather than relying on watchdog coverage alone.
Confidence: HIGH
PatternID: P4

Findings: 1 Critical, 1 High, 0 Advisory (21 of 21 patterns checked; 19 showed no gap).
