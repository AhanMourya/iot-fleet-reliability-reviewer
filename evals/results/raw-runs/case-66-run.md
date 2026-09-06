# Case 66 — MashLine — Reviewer Run

[CRITICAL] OTA
Finding: No rollback or A/B update path
Evidence: Plan states updates are pushed via "a script that overwrites the current application binary and restarts the monitoring service; there is no fallback partition to revert to if a bad update disrupts a sensor mid-batch."
Risk: A bad push could disrupt process monitoring mid-fermentation with no remote recovery — direct product-quality and batch-loss consequence.
Recommended mitigation: Move to A/B (dual-bank) partitioning with automatic rollback on boot/health-check failure.
Confidence: HIGH
PatternID: O1

Findings: 1 Critical, 0 High, 0 Advisory (21 of 21 patterns checked; 20 showed no gap).
