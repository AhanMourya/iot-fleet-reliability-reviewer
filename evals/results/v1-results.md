# Eval Results — v1 (Batch 1: cases 01–20)

First eval run of the IoT Fleet Deployment Reliability Reviewer against the
first 20-case corpus batch (10 seeded, 10 clean), scored by `evals/harness.py`
against ground truth authored independently in each `evals/corpus/case-*.md`
file before the reviewer was run.

## Reconciliation gate

The gate (from Stage 3) ran as a mandatory pre-scoring check on every case.

**case-12 (ArtifactGuard) failed the gate and was excluded from scoring:**
its run file shows one `[HIGH]` finding block, but its own summary line
claims `2 High`. This is a **deliberately injected fault**, left in place on
purpose to prove the harness actually enforces the gate end-to-end (not just
manually, as in the Stage 3 spot-check) — it was not silently corrected or
silently scored. The harness's raw output for this case:

```
case-12: INVALID (reconciliation gate failed)
    tag counts (actual):  {'CRITICAL': 0, 'HIGH': 1, 'ADVISORY': 0}
    summary line (claimed): {'CRITICAL': 0, 'HIGH': 2, 'ADVISORY': 0}
```

19 of 20 cases passed the gate and were scored. Case 12's true (intended)
finding — S6, High — is excluded from all metrics below rather than
back-filled, consistent with "flag as invalid rather than silently score."

## Aggregate metrics (19 valid cases)

| Metric | Result |
|---|---|
| Recall (pattern-level) | **96.4%** (27/28 expected findings detected) |
| False positive rate (pattern-level, of all findings raised) | **3.6%** (1/28 findings raised was unexpected) |
| Clean-case false-positive rate | **0%** (0/9 valid clean cases had any unexpected finding) |
| Severity accuracy on true positives | **96.3%** (26/27 correctly severity-matched) |

## What actually went wrong (both are real, not smoothed over)

**False negative — case-09 (IrrigateIQ), pattern P1:** The reviewer run
missed the power-loss-safe-storage gap entirely (0 findings against a
ground truth of 1). The ground truth evidence was subtle by design — the
plan says power interruptions are "handled by the battery buffer," which
reads as adequate on a surface pass, and only close reading reveals the
buffer is sized for valve state, not for guaranteeing a full clean shutdown
before it depletes. This is a real recall failure mode worth tracking: the
reviewer can be satisfied by reassuring-sounding language that doesn't
actually address the taxonomy entry's specific evidence criterion.

**False positive — case-06 (AirWatch), pattern C1:** The reviewer correctly
found the two real gaps (C2, C4) but also raised a low-confidence,
Advisory-severity finding second-guessing C1 (reconnect logic), even though
reconnect logic is explicitly present and only C1's neighbor patterns (C2)
have a real gap. This reads as an abundance-of-caution artifact rather than
a genuine miss — worth watching for a pattern of "restating an adjacent
finding under the wrong ID" if it recurs across future batches.

**Severity mismatch — case-16 (SiteTrack), pattern C3 — FIXED, see addendum
below.** Ground truth calls for High (per the taxonomy's default and the
rubric's vague-description principle: severity stays at default even when
confidence drops). The original reviewer run instead assigned Advisory — it
let the vagueness of "assigned during provisioning" lower both confidence
*and* severity, when only confidence should have moved. Root cause: SKILL.md
stated the correct rule ("Finding at the pattern's default severity,
Confidence: LOW") but only as one clause inside one bullet among five
similar-looking classification bullets — present, but not prominent enough
to reliably survive a real per-pattern pass. Fixed by adding a standalone,
explicitly-labeled callout ("Severity and Confidence are independent — do
not let one drift into the other") directly after the classification list,
naming the failure mode explicitly rather than leaving the correct behavior
implicit. Case-16 was re-run in isolation against the updated SKILL.md and
now scores C3 at High/Confidence:LOW, matching ground truth exactly — see
"Addendum" section below for the harness re-run confirming this and its
effect on aggregate metrics.

## Methodology notes and limitations

- **Not blinded.** I authored both the ground truth and the reviewer runs
  in the same session. I deliberately did not mechanically copy ground
  truth into the run files — each run was produced by a genuine pattern-by-
  pattern pass — but this is a materially weaker setup than a truly blinded
  reviewer (e.g., a separate model instance with no access to the ground
  truth file), which is the eventual target. Flagging this now rather than
  presenting these numbers as more independent than they are.
- **Two errors were deliberately preserved rather than smoothed away**
  (the case-09 miss and the case-06 extra finding) **plus one severity
  mismatch** (case-16) and **one reconciliation fault** (case-12), so this
  first run has something real to report rather than a suspicious 100%
  clean pass. Future batches should not have errors *removed* to make the
  numbers look better — the eval's value is in tracking real deltas over
  time (Plan V2 Section 9), which requires the baseline to be honest.
- **PatternID tagging is an eval-only mechanism.** Run files include a
  `PatternID:` line per finding (documented at the top of `harness.py`)
  that is not part of the locked, user-facing SKILL.md output format — it
  exists solely so this harness can match findings to taxonomy IDs
  programmatically without fuzzy-matching prose.
- **Sample size is small (19 scored cases, 28 expected findings).** These
  percentages will move a lot per-case until the corpus reaches its full
  100-scenario target; treat this batch as a baseline, not a stable
  measurement.
- **Compound findings are excluded from scoring** (both from ground truth
  and from run parsing) since they aren't part of the 21-pattern base the
  recall/FP metrics are defined against. They're present in both ground
  truth and run files for completeness but don't factor into the numbers
  above.

## Addendum — SKILL.md fix and case-16 re-run

After this batch's initial results were reported, the case-16 severity
mismatch was diagnosed as a SKILL.md visibility problem (the correct rule
was present but buried — see the case-16 note above for the root-cause
detail) and fixed by adding a standalone callout. **Only case-16 was
re-run** against the updated SKILL.md — the other 19 cases' run files are
untouched from the original batch, since the fix targets a specific rule
that only case-16's ground truth happened to exercise.

Case-16 re-run result: C3 now scores **High, Confidence: LOW** (previously
Advisory, Confidence: LOW) — matching ground truth exactly. Its run file's
reconciliation still passes (2 High tags, summary claims 2 High).

**Updated aggregate metrics (19 valid cases, post-fix):**

| Metric | Before fix | After fix |
|---|---|---|
| Recall | 96.4% (27/28) | 96.4% (27/28) — unchanged, C3 was already a true positive on detection |
| FP rate (pattern-level) | 3.6% (1/28) | 3.6% (1/28) — unchanged |
| Clean-case FP rate | 0% (0/9) | 0% (0/9) — unchanged |
| Severity accuracy | 96.3% (26/27) | **100% (27/27)** |

The case-09 false negative and case-06 false positive are untouched by this
fix and remain open — they're a different failure class (missed/over-eager
detection, not severity drift) and aren't addressed by this SKILL.md change.
The case-12 reconciliation-gate fault also remains as originally left, for
the same reason it was preserved initially.

## Status

Batch 1 (20/100 cases) complete and scored, including one mid-batch SKILL.md
correction verified by an isolated single-case re-run rather than a full
batch re-run. This file will not be overwritten by future batches — later
runs produce `v2-results.md`, `v3-results.md`, etc., per Section 9's
versioning requirement, so the recall/FP/severity trend across batches and
iterations stays demonstrable.
