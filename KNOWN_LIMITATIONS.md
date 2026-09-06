<!--
This file is staged content for the "Known Limitations" section of the
project's eventual top-level README (per Project Plan V2 Section 2's
framing: the taxonomy, rubric, and evals are first-class artifacts, and an
honest limitations section belongs with them, not as a footnote written
after the fact). Drop this section in verbatim, or adapt wording to fit
the surrounding README, but do not drop content to make the project read
as more finished than the eval history actually shows.

Source: evals/results/v5-results.md, written at 100-case corpus completion.
-->

## Known Limitations

Three unresolved detection errors, unchanged since they first appeared:

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

One suspected-but-unconfirmed pattern, explicitly left open:

- **The case-28/case-49 reconciliation-miscount shape.** Two summary-line
  arithmetic errors (Batches 2 and 3) shared an identical structure: two
  standalone Critical findings immediately followed by a third Critical
  compound finding, with the actual Critical count miscounted by exactly
  one. Five more cases with this same shape appeared in Batches 4 and 5
  (case-62, case-68, case-69 — an exact structural match to case-28/49 —
  case-70, case-82, case-89, case-90), all hand-verified correct. The
  standing rule was: fix only on a third recurrence, not on suspicion. A
  third recurrence never came. This is reported as an open question, not a
  resolved one — a sample of "5 more correct in a row" after 2 failures is
  consistent with either "it was genuinely a coincidence of early
  drafting" or "it's a low-frequency issue that needs more than 100 cases
  to surface a third time." No SKILL.md change was made. Anyone continuing
  this project (more eval cases, or production usage generating real
  reviewer runs) should keep watching for this specific shape rather than
  treating it as closed.

Structural limitations of this eval itself:

- **Not blinded.** The same author (a single Claude instance, across one
  extended session) wrote both the ground truth and the reviewer runs for
  all 100 corpus cases. This is the single biggest reason these eval
  numbers should be read as a structured, good-faith self-check rather
  than an independent validation. A genuinely blinded eval — ground truth
  authored by one party, reviewer runs produced by a separate model
  instance or a human with no access to it — is the natural next step
  before treating these percentages as a trustworthy external benchmark.
- **Compound findings are excluded from all recall/false-positive/severity
  calculations.** They appear in both ground truth and run files for
  narrative completeness but were never part of the scored 21-pattern
  base.
- **Corpus construction bias.** All 100 plans were written by the same
  author in the same style, using similar sentence patterns for similar
  gaps (e.g., "the plan does not describe any X" recurs constantly). Real
  deployment plans from actual users will vary far more in structure,
  vocabulary, and how directly they state things. The corpus's 97.4%
  cumulative recall should not be read as a prediction of real-world
  performance.
- **The eval-only `PatternID:` annotation** used by `evals/harness.py` to
  match findings to taxonomy IDs is not part of the production SKILL.md
  output format shown to end users — see `evals/harness.py`'s docstring.
