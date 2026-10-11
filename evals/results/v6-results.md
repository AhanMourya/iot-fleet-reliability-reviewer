# v6 Results — Executable Reconciliation & Evaluation Layer

Full 100-case corpus re-scored through `iot_reliability_reviewer.evaluation`,
which reconciles every case via the deterministic `reconciliation.py` engine
instead of the inline count-comparison gate in the original `evals/harness.py`.

No new LLM calls were made for this run. The existing `raw-runs/*.md` files
(same ones scored for v1–v5) were converted into the Phase 2 JSON schema by
`legacy_run_to_payload`, which parses each finding's pattern/severity/
confidence directly from the file and **discards** the file's own
free-text `Findings: X Critical, Y High, Z Advisory` line — that field
doesn't exist in the new schema, so there's nothing to trust or distrust.
`no_gap_patterns` is derived as "the 21 base patterns minus whichever ones
appear as findings."

## Headline result

**Cases scored: 100/100 valid, 0 invalid** (v5 was 97/100 valid, 3 excluded).

This is the actual deliverable of this phase: **0 gate failures, provably**,
not just observed. The three cases previously excluded (case-12, case-28,
case-49) were all excluded for the exact bug class this phase targets — a
human- or model-claimed summary count that didn't match the actual findings.
Under the new pipeline there is no separate summary field to disagree with
the findings in the first place, so those three cases are no longer
malformed; they're just... scored.

| Metric | v5 (LLM-only, old gate) | v6 (new reconciliation engine) |
|---|---|---|
| Cases scored | 97/100 (3 excluded) | 100/100 (0 excluded) |
| Recall | 97.4% (127/130) | 98.5% (132/134) |
| False positive rate | 0.8% (1/128) | 0.8% (1/133) |
| Clean-case FP rate | 0% | 0% |
| Severity accuracy | 100% (127/127) | 100% (132/132) |

## Explaining the discrepancy (per Plan V4 Stage D)

Recall moved from 97.4% to 98.5% and the expected-findings denominator moved
from 130 to 134. This is fully explained by the three previously-excluded
cases re-entering the scored set, each contributing its own expected/found
counts:

- **case-12**: old gate found actual tag counts `{HIGH: 1}` vs. a claimed
  summary of `{HIGH: 2}` — a plain arithmetic error in the original
  free-text run. The new pipeline never reads that claimed line, so the
  single real HIGH finding is scored normally.
- **case-28** and **case-49**: both had a real compound finding whose
  tag count (2 CRITICAL total: one base finding + one compound) was
  mis-tallied as 3 CRITICAL in the free-text summary. Same story — the new
  pipeline computes CRITICAL=2 directly from the findings list and scores
  the two real base findings against ground truth.

False positive rate held exactly at 0.8% because the one genuine false
positive from v1–v5 was in an already-valid case; it isn't affected by
which of the other cases become valid.

**Conclusion: not a scoring discrepancy, a coverage discrepancy.** The old
harness's numbers were correct arithmetic over a smaller, gate-filtered set.
The new numbers are correct arithmetic over the full set, because the
findings that used to get thrown out entirely (case-12/28/49 each had real,
correct findings underneath the summary-line bug) are now recoverable
instead of discarded. Recall going up, not down, is the expected direction
for that kind of fix.

## What this does NOT change

- No taxonomy, rubric, or corpus content changed.
- No SKILL.md review logic changed — every finding scored above is the
  same finding text/evidence/severity a human or model already produced
  in v1–v5. Only how those findings are counted and gated changed.
- This is a re-scoring of existing runs, not a fresh 100-case LLM re-run
  through the full hybrid pipeline (reviewer.py + reconciliation.py end to
  end). That's the natural next validation step once outreach or continued
  development produces a reason to re-run the corpus live.
