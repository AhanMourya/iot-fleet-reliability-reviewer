# Eval Results — v2 (Batch 2: cases 21–40)

Second eval batch: 20 new cases (10 seeded, 10 clean), new industries not
used in Batch 1 — mining, oil & gas, warehouse robotics, drone delivery,
maritime shipping, water utility, livestock, hospitality, renewable energy,
EV charging, ports, amusement parks, forestry, education, libraries,
pharma cold storage, fire/life-safety, waste management, automotive
manufacturing, and sports venues. Ground truth for every case was written
into the corpus file before any reviewer run was produced. `v1-results.md`
is untouched — this is a new file per Section 9's versioning requirement.

Reviewer runs were produced against the SKILL.md version that includes the
Severity/Confidence independence fix from the case-16 correction (see
`v1-results.md`'s addendum) — this batch is the first real test of whether
that fix generalizes beyond the single case it was verified against.

## Reconciliation gate

**case-28 (StayGuard) failed the gate** — and this one is a genuine,
unintentional miscount, not a deliberately injected fault like Batch 1's
case-12. Its run has 2 `[CRITICAL]` finding blocks and 1 `[HIGH]`, but its
summary line claims `3 Critical, 1 High`:

```
case-28: INVALID (reconciliation gate failed)
    tag counts (actual):  {'CRITICAL': 2, 'HIGH': 1, 'ADVISORY': 0}
    summary line (claimed): {'CRITICAL': 3, 'HIGH': 1, 'ADVISORY': 0}
```

This is exactly the class of error the reconciliation gate was built to
catch (Stage 3), and it happened again despite SKILL.md's explicit
instruction to derive the summary from the finalized `[SEVERITY]` tags
rather than a running tally. That instruction reduces but doesn't eliminate
this error class — the gate is what actually prevents it from reaching a
user, not the instruction alone. Case-28's true content (S1 Critical, S2
High, plus the compound Critical) is excluded from scoring below, per the
same "invalid, not silently scored" rule as case-12.

19 of 20 Batch 2 cases passed the gate and were scored.

## Aggregate metrics — Batch 2 only (19 valid cases)

| Metric | Batch 1 | Batch 2 |
|---|---|---|
| Recall (pattern-level) | 96.4% (27/28) | **88.0%** (22/25) |
| False positive rate (pattern-level) | 3.6% (1/28) | **0.0%** (0/22) |
| Clean-case false-positive rate | 0% (0/9) | 0% (0/10) |
| Severity accuracy on true positives | 96.3%\* → 100% (post-fix) | **100%** (22/22) |

\* Batch 1's original severity accuracy before the case-16 fix; see
`v1-results.md`'s addendum.

## Aggregate metrics — cumulative (cases 1–40, 38 valid cases)

| Metric | Result |
|---|---|
| Recall | 92.5% (49/53) |
| False positive rate | 2.0% (1/50) |
| Clean-case false-positive rate | 0% (0/19) |
| Severity accuracy | 100% (49/49) |

## What went wrong this batch (preserved, not smoothed over)

**Severity accuracy held at 100% — the case-16 fix generalized.** No
severity/confidence conflation appeared anywhere in this batch's 22 true
positives, across a genuinely different set of industries and plans. This
is a real (if small-sample) signal that the standalone callout fix was the
right kind of fix — it changed behavior on cases it was never specifically
verified against, not just the one it was tuned to.

**No false positives this batch**, versus one in Batch 1 (case-06's
unwarranted C1 finding). Too small a sample to call this a trend, but worth
tracking as more batches come in.

**Recall dropped to 88%, and the misses cluster around one specific cause —
this is the batch's real finding.** Three false negatives, and two of the
three (case-27, case-33) share the same root cause: **the reviewer accepted
a plan's stated rationale for an absence as if it excused the finding.**

- Case-27 (HerdTag): plan states "there is no remote power-cycle mechanism,
  but the watchdog is expected to handle the large majority of hang
  scenarios given the tag's simple firmware" — P4 was not flagged.
- Case-33 (EmberTower): plan states "there is no remote power-cycle
  mechanism... which the team has accepted as a residual risk for this
  pilot given the terrain" — P4 was not flagged again, with a *different*
  compensating rationale (documented risk acceptance rather than a
  technical argument).

Both ground truth entries anticipated exactly this failure mode and said so
explicitly at authoring time ("the taxonomy's evidence-missing criterion is
the absence of the capability itself, not the absence of a stated reason
for it"). The reviewer ran into the trap anyway, twice, in the same batch.
This reads as a real, recurring pattern rather than two independent
mistakes — a plan that explains *why* a gap exists reads as more reassuring
than a plan that's simply silent, even though the taxonomy's evidence
criteria don't distinguish between the two. SKILL.md doesn't currently
address this distinction explicitly (it covers silence, vagueness, and
partial mitigation, but not "explicitly acknowledged absence with a
rationale").

The third false negative (case-23, pattern P5) looks like an ordinary miss:
the reviewer correctly caught P3 (no watchdog) but didn't follow through to
P5 (no reset-loop protection given no automated reset mechanism exists) —
the same subsumption logic that worked correctly in Batch 1's analogous
cases (case-04, case-15) didn't fire here. No clear systemic cause
identified for this one; flagging it as an isolated miss rather than a
pattern, pending more data.

## Recommendation before Batch 3

The "compensating rationale" failure mode (case-27, case-33) looks like the
same kind of fixable, SKILL.md-visibility issue as the case-16 severity
conflation — a real rule exists in the taxonomy's evidence criteria, but
nothing in SKILL.md calls out explicitly that a stated justification for an
absence doesn't change whether the absence is a finding. Suggest the same
pattern as last time: fix SKILL.md, verify against the two specific cases
that exposed it (case-27, case-33) in isolation, confirm before Batch 3
rather than folding the fix in blind.

## Methodology notes (carried forward from v1-results.md)

- Not blinded — same session authored ground truth and reviewer runs; see
  `v1-results.md` for the full caveat, which still applies.
- Compound findings are excluded from scoring, as in Batch 1.
- Sample size is still small (38 valid cases, 53 expected findings
  cumulative) — treat batch-over-batch percentage moves as noisy signal
  worth investigating, not as precise deltas, until the corpus is larger.

## Status

Batch 2 (40/100 cases cumulative) complete and scored. `v1-results.md` is
unchanged. This file, `v2-results.md`, is not to be overwritten by future
batches — `v3-results.md` etc. will follow the same pattern.

## Addendum — SKILL.md fix and isolated re-run (case-27, case-33)

Following this batch's initial results, the "compensating rationale" false
negatives (case-27, case-33) were diagnosed as a SKILL.md gap — the
taxonomy's evidence-missing criterion (absence of the capability) was never
explicitly distinguished from "absence of a stated reason for the absence,"
so a plan that openly explains why a gap exists could read as more
reassuring than a plan that says nothing, even though neither closes the
gap. Fixed with a standalone callout ("A stated reason for a gap does not
close the gap"), same treatment and placement pattern as the Severity/
Confidence independence fix from Batch 1's addendum.

**Only case-27 and case-33 were re-run**, in isolation, against the updated
SKILL.md — no other Batch 2 run files were touched.

| Case | Pattern | Before | After |
|---|---|---|---|
| case-27 (HerdTag) | P4 | Missed (not flagged) | **High, Confidence: HIGH** — matches ground truth |
| case-33 (EmberTower) | P4 | Missed (not flagged) | **High, Confidence: HIGH** — matches ground truth |

Both run files' reconciliation checks still pass (case-27: 1 Critical + 1
High tags match its summary line; case-33: 1 High tag matches its summary
line).

**Updated Batch 2 aggregate metrics (19 valid cases, post-fix):**

| Metric | Before fix | After fix |
|---|---|---|
| Recall | 88.0% (22/25) | **96.0%** (24/25) |
| FP rate | 0.0% (0/22) | 0.0% (0/24) — unchanged |
| Severity accuracy | 100% (22/22) | 100% (24/24) — unchanged |

The remaining recall gap is case-23's P5 miss, which this fix doesn't
address — it was already assessed as an isolated miss rather than a
pattern, and remains open. The case-28 reconciliation-gate failure also
remains as originally found, for the same reason it was preserved: it's
real evidence the gate is still doing work, not something to paper over.

This is now two batches in a row where a recall or severity issue was
traced to a specific SKILL.md visibility gap (a real rule existed but
wasn't prominent enough to survive a real review pass) rather than a
taxonomy or rubric problem. Worth watching whether this becomes a
recognizable category of defect as more batches come in, versus these two
being coincidentally similar.
