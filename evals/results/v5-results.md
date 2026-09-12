# Eval Results — v5 (Batch 5: cases 81–100) — Full 100-Case Corpus Complete

Fifth and final eval batch: 20 new cases (10 seeded, 10 clean), new
industries — usage-based insurance telematics, municipal water
distribution, EMS/ambulance fleets, smart grid substations, ski
gondolas/cable cars, vertical farming, landfill gas monitoring, passenger
ferries, sidewalk delivery robots, freight rail cars, weather stations,
records archives, textile manufacturing, coworking spaces, playground
safety, car dealership lots, consumer cold storage rental, data center
liquid cooling, public restroom facilities, and theme park queues. Ground
truth authored before any reviewer run, as in all prior batches.
`v1`–`v4-results.md` are all untouched. **This completes the 100-case
corpus target from Project Plan V2 Section 9.**

## Direct answer to the standing question: the shape did not recur a third time

Two compound-shaped cases this batch exactly matched the case-28/case-49
failure shape's family:

- **case-82** (S1+S4+compound) — hand-verified: 3 actual `[CRITICAL]` tags,
  summary claims 3. Reconciles.
- **case-89** (S1+S2+compound — the *exact* shape from case-28 and
  case-49) — hand-verified: 2 actual `[CRITICAL]` tags + 1 `[HIGH]`,
  summary claims 2 Critical + 1 High. Reconciles.

All four compound-shaped cases in this batch (82, 88, 89, 90) were checked
by hand before finalizing, per the standing instruction. **Zero
reconciliation gate failures in Batch 5** — the second consecutive
perfect-gate batch. Combined with Batch 4's clean pass and this batch's two
direct re-tests of the exact case-28/49 shape, there's now reasonable
(though not conclusive) evidence that the two earlier failures were
batch-specific drafting slips rather than a systemic issue tied to that
finding shape. No fix was triggered, consistent with the standing rule
(recurrence, not suspicion, is the trigger) — but this is explicitly
flagged in the Known Limitations section below rather than treated as
closed, since "hasn't recurred in 2 more direct tests" is meaningfully
different from "proven not to be a pattern."

## Aggregate metrics — Batch 5 only (20 valid cases, 0 invalid)

| Metric | Result |
|---|---|
| Recall | 100% (26/26) |
| False positive rate | 0.0% (0/26) |
| Clean-case false-positive rate | 0% (0/10) |
| Severity accuracy | 100% (26/26) |
| Reconciliation gate failures | 0 |

Third batch in a row (3, 4, 5) with a perfectly clean scorecard.

## Full cumulative results — all 100 cases

| Metric | Result |
|---|---|
| Cases scored | 97 valid / 100 (3 excluded by the reconciliation gate) |
| Recall | **97.4%** (127/130 expected findings detected) |
| False positive rate | **0.8%** (1/128 findings raised was unexpected) |
| Clean-case false-positive rate | **0%** (0/49 valid clean cases had any unexpected finding) |
| Severity accuracy on true positives | **100%** (127/127) |

**Batch-by-batch trend:**

| Batch | Cases | Recall | FP rate | Severity accuracy | Gate failures |
|---|---|---|---|---|---|
| 1 (1–20) | 20 | 96.4% → 96.4%\* | 3.6% | 96.3% → 100%\* | 1 (deliberate) |
| 2 (21–40) | 20 | 88.0% → 96.0%\* | 0.0% | 100% | 1 (genuine) |
| 3 (41–60) | 20 | 100% | 0.0% | 100% | 1 (genuine, same shape as B2) |
| 4 (61–80) | 20 | 100% | 0.0% | 100% | 0 |
| 5 (81–100) | 20 | 100% | 0.0% | 100% | 0 |

\* Before/after in-batch SKILL.md fixes (case-16 severity/confidence fix
after Batch 1; case-27/case-33 compensating-rationale fix after Batch 2).
Post-fix numbers are what's reflected in the cumulative totals above.

**Two SKILL.md fixes were made across the five batches** (Severity/
Confidence independence after Batch 1; "a stated reason for a gap does not
close the gap" after Batch 2), both diagnosed from real reviewer errors,
both verified by isolated single/dual-case re-runs before being trusted,
both documented as addenda without altering original batch numbers. No
further SKILL.md-visibility issues surfaced in Batches 3, 4, or 5 despite
specific, deliberate stress-testing (case-58's regulatory-justification
variant, case-78's operational-choice variant) — three consecutive clean
batches after the second fix is a reasonably strong signal that this
specific class of defect has been addressed, though "reasonably strong"
still isn't "proven."

## Known Limitations

*(Drafted here for inclusion in the project's eventual top-level README —
this section documents real, open issues at project completion, not
resolved-and-forgotten history.)*

**Three unresolved detection errors, unchanged since they first appeared:**

- **case-09 (IrrigateIQ) — false negative on P1**, first found in Batch 1.
  The reviewer missed a power-loss-safe-storage gap because the plan's
  language ("handled by the battery buffer") reads as reassuring on a
  surface pass, and only close reading reveals the buffer covers routine
  operation, not a guaranteed clean shutdown. Did not recur in 80
  subsequent cases, including several with similar "handled by X" phrasing
  patterns — but "hasn't recurred" is not the same as "understood and
  fixed." No SKILL.md change has been made for this specific failure mode.

- **case-23 (AGVFleet) — false negative on P5**, first found in Batch 2.
  The reviewer correctly caught P3 (no watchdog) in the same case but
  didn't follow through to P5 (no reset-loop protection, which is only
  meaningful once an automatic reset mechanism exists) — the same
  subsumption logic that worked correctly in structurally similar cases
  elsewhere in the corpus (case-04, case-15, case-63, case-83, all of
  which correctly paired P3/P4 findings) didn't fire here. No clear root
  cause was identified. This remains the least-understood open issue in
  the project — it's not clear whether it's a one-off execution slip or a
  narrower version of a real gap that just hasn't been hit again.

- **case-06 (AirWatch) — false positive on C1**, first found in Batch 1.
  The reviewer correctly found two real gaps (C2, C4) in this case but
  also raised an unwarranted, low-confidence, Advisory-severity finding
  second-guessing C1, even though reconnect logic is explicitly present.
  Reads as an abundance-of-caution artifact. Did not recur in any of the
  99 other cases.

**One suspected-but-unconfirmed pattern, explicitly left open:**

- **The case-28/case-49 reconciliation-miscount shape.** Two summary-line
  arithmetic errors (Batches 2 and 3) shared an identical structure: two
  standalone Critical findings immediately followed by a third Critical
  compound finding, with the actual Critical count miscounted by exactly
  one. Five more cases with this same shape appeared in Batches 4 and 5
  (case-62, case-68, case-69 — an exact structural match to case-28/49 —
  case-70, case-82, case-89, case-90), all hand-verified correct. The
  standing rule was: fix only on a third recurrence, not on suspicion. A
  third recurrence never came. This is reported as **an open question, not
  a resolved one** — a sample of "5 more correct in a row" after 2 failures
  is consistent with either "it was genuinely a coincidence of early
  drafting" or "it's a low-frequency issue that needs more than 100 cases
  to surface a third time." No SKILL.md change was made. Future work on
  this project (additional eval cases, or production usage generating real
  reviewer runs) should keep watching for this specific shape rather than
  treating it as closed.

**Structural limitations of this eval, unchanged from earlier batches:**

- **Not blinded.** The same author (working across a single continuous
  session) wrote both the ground truth and the reviewer runs for
  all 100 cases. Every batch's results file has flagged this. It's the
  single biggest reason these numbers should be read as "a structured,
  good-faith self-check" rather than "an independent validation." A truly
  blinded eval — ground truth authored by one party, reviewer runs
  produced independently by someone or something with no access to it —
  is the natural next step before treating these percentages as a
  trustworthy external benchmark.
- **Compound findings are excluded from all recall/FP/severity
  calculations.** They exist in both ground truth and run files for
  narrative completeness but were never part of the scored 21-pattern
  base.
- **Corpus construction bias.** All 100 plans were written by the same
  author in the same style, using similar sentence patterns for similar
  gaps (e.g., "the plan does not describe any X" recurs constantly). Real
  deployment plans from actual users will vary far more in structure,
  vocabulary, and how directly they state things. The 97.4% cumulative
  recall should not be read as a prediction of real-world performance.
- **PatternID tagging is an eval-only mechanism** (documented in
  `harness.py`), not part of the production SKILL.md output format shown
  to end users.

## Status

**The 100-case eval corpus (Project Plan V2 Section 9) is complete.**
`v1` through `v4-results.md` remain unchanged; this file adds the final
batch and the full cumulative picture rather than superseding the earlier
files. Per Section 9's versioning requirement, no existing results file has
ever been overwritten across this project — v1 through v5 each represent a
real, timestamped snapshot of the reviewer's measured performance as the
taxonomy, rubric, SKILL.md, and corpus all evolved together.

Remaining project work (per Project Plan V2, not part of this eval): usage
instrumentation (Section 10) and the structured config-parsing roadmap item
(Section 11, "v1.5") are both still unstarted, by design — this batch
completes only the eval corpus and harness, not the full project plan.
