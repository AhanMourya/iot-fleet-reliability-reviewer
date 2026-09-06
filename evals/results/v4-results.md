# Eval Results — v4 (Batch 4: cases 61–80)

Fourth eval batch: 20 new cases (10 seeded, 10 clean), new industries —
semiconductor cleanrooms, grain storage, HVAC service fleets, casino gaming
floors, highway tolling, brewing/distilling, apiculture, snow removal
fleets, postal sortation, marinas, university labs, meat processing,
recycling sortation, religious/community venues, pet care facilities, wine
storage, concrete/asphalt production, cinemas, laundromats, and airport
passenger flow. Ground truth authored before any reviewer run, as in
Batches 1–3. `v1`, `v2`, and `v3-results.md` are all untouched.

## Direct answer to the standing question: no third instance this batch

Every compound-shaped case in this batch (case-62: S1+S4+compound,
case-68: S4+S6+compound, **case-69: S1+S2+compound — the exact shape that
broke in case-28 and case-49**, and case-70: O1+O5+compound) was checked by
hand against its own summary line before being finalized. All four
reconciled correctly. Case-69 in particular was written specifically to
re-test the exact failure shape (two standalone Criticals immediately
followed by a Critical compound finding) and came back correct: 3 actual
`[CRITICAL]` tags, summary claims 3.

**Reconciliation gate: 0 failures in Batch 4** — the first batch with a
perfect gate pass rate. Per the standing instruction, since the shape didn't
recur a third time, no SKILL.md fix is triggered. This is now 1 recurrence
(case-28, case-49) with case-69 as a direct, deliberate re-test that didn't
reproduce it — weak evidence the earlier two were a coincidence of that
specific batch's drafting rather than a systemic issue tied to the shape
itself, but not strong enough to close the question outright with only one
confirmed recurrence and one clean re-test. Continuing to watch rather than
declaring it resolved.

## Aggregate metrics — Batch 4 only (20 valid cases, 0 invalid)

| Metric | Batch 1 | Batch 2 (post-fix) | Batch 3 | Batch 4 |
|---|---|---|---|---|
| Recall | 96.4% | 96.0% | 100% | **100%** (26/26) |
| False positive rate | 3.6% | 0.0% | 0.0% | **0.0%** (0/26) |
| Clean-case FP rate | 0% | 0% | 0% | **0%** (0/10) |
| Severity accuracy | 100% (post-fix) | 100% | 100% | **100%** (26/26) |
| Reconciliation gate failures | 1 (deliberate) | 1 (genuine) | 1 (genuine, same shape as prior) | **0** |

This is the first batch with no findings to report at all — no misses, no
extra findings, no severity errors, no gate failures. Two consecutive
clean batches (3 and 4) after two batches that each surfaced a real,
fixable issue.

## Aggregate metrics — cumulative (cases 1–80, 77 valid cases)

| Metric | Result |
|---|---|
| Recall | 98.1% (101/103) |
| False positive rate | 1.0% (1/102) |
| Clean-case false-positive rate | 0% (0/39) |
| Severity accuracy | 100% (101/101) |

The two cumulative false negatives (case-09 P1, case-23 P5) and the one
false positive (case-06 C1) remain exactly as they were after Batch 2 —
no new instances of either in Batches 3 or 4, across 40 additional cases
and industries with no overlap to the originals. This is now reasonably
good evidence these three are genuinely isolated rather than systemic,
though "isolated" here still means "not yet recurred in 40 more cases,"
not "provably one-off."

## Methodology notes (carried forward)

- Not blinded — same caveat as v1–v3.
- Compound findings excluded from scoring.
- Sample size: 77 valid cases, 103 expected findings cumulative. Getting
  large enough that batch-to-batch swings are starting to mean something,
  though the corpus is still only 80% built.

## Status

Batch 4 (80/100 cases cumulative) complete and scored. `v1`, `v2`, and
`v3-results.md` are unchanged. One batch remains to reach the full
100-scenario target (Section 9).
