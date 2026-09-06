# Eval Results — v3 (Batch 3: cases 41–60)

Third eval batch: 20 new cases (10 seeded, 10 clean), new industries —
aviation ground support, railways, telecom, banking/ATM, structured
parking, greenhouse agriculture, zoos/aquariums, car rental, micromobility,
solar farms, cruise lines, hospital asset tracking, grocery cold chain,
municipal streetlights, corrections, agricultural drones, golf course
irrigation, elevator/escalator monitoring, car washes, and vending. Ground
truth authored before any reviewer run, as in Batches 1–2. `v1-results.md`
and `v2-results.md` are untouched.

## Direct answer to the standing question: no third "buried rule" instance this batch

Case-58 (LiftGuard) was deliberately written to stress-test the compensating-
rationale fix from the v2 addendum with a **third, materially different**
justification style: not a technical argument ("the watchdog should catch
most hangs") and not a documented risk acceptance ("the team has accepted
this"), but a **regulatory/safety-code constraint** (elevator machine rooms
can't have remote power actuation by code). This is the kind of rationale
most likely to tempt a reviewer into treating the absence as legitimately
closed rather than merely explained, since it's not a shortcut or an
oversight — it's a real constraint. The reviewer run still correctly flagged
P4, explicitly noting in `Evidence` that the regulatory reason explains the
gap without closing it. **No new SKILL.md visibility gap surfaced this
batch.** Recall, FP rate, and severity accuracy are all clean — see below.

## Reconciliation gate

**case-49 (RollShare) failed the gate** — 2 `[CRITICAL]` finding blocks and
1 `[HIGH]`, but its summary line claims `3 Critical, 1 High`:

```
case-49: INVALID (reconciliation gate failed)
    tag counts (actual):  {'CRITICAL': 2, 'HIGH': 1, 'ADVISORY': 0}
    summary line (claimed): {'CRITICAL': 3, 'HIGH': 1, 'ADVISORY': 0}
```

Worth flagging directly: **this is the same exact miscount shape as Batch
2's case-28** (2 Critical + 1 High actual, claimed as 3 Critical + 1 High) —
both cases follow the identical structure (a shared-credential finding, a
proximity/exposure finding, plus a compound finding tying them together).
That's a real, specific, reproducible pattern rather than two unrelated
slips: whatever is producing this off-by-one seems to correlate with this
particular finding shape (two standalone Criticals immediately followed by
a third Critical compound finding), not with reconciliation counting in
general — every other multi-compound case in the corpus (case-01, case-07,
case-08, case-10, case-22, case-30, case-42, case-48, case-50) reconciled
correctly. Not fixing this now since it's a narrower, lower-confidence
signal than the last two SKILL.md issues (only 2 data points, both
S1+S2+compound-shaped), but flagging it explicitly rather than letting it
pass as noise — worth revisiting if a third instance of this specific shape
appears.

19 of 20 Batch 3 cases passed the gate and were scored.

## Aggregate metrics — Batch 3 only (19 valid cases)

| Metric | Batch 1 | Batch 2 (final, post-fix) | Batch 3 |
|---|---|---|---|
| Recall | 96.4% | 96.0% | **100%** (24/24) |
| False positive rate | 3.6% | 0.0% | **0.0%** (0/24) |
| Clean-case FP rate | 0% | 0% | **0%** (0/10) |
| Severity accuracy | 100% (post-fix) | 100% | **100%** (24/24) |

## Aggregate metrics — cumulative (cases 1–60, 57 valid cases)

| Metric | Result |
|---|---|
| Recall | 97.4% (75/77) |
| False positive rate | 1.3% (1/76) |
| Clean-case false-positive rate | 0% (0/29) |
| Severity accuracy | 100% (75/75) |

The two remaining cumulative false negatives are case-09's P1 miss (Batch
1, still open, subtle "battery buffer" reassurance language) and case-23's
P5 miss (Batch 2, still open, isolated subsumption-logic slip). The one
cumulative false positive is case-06's extra C1 finding (Batch 1, still
open). None of these three recurred in Batch 3 in any form, including in
cases with structurally similar wording — some limited evidence they're
genuinely isolated rather than systemic, though the sample is still small
enough that this isn't conclusive.

## Methodology notes (carried forward)

- Not blinded — same caveat as v1/v2.
- Compound findings excluded from scoring, as before.
- Sample size: 57 valid cases, 77 expected findings cumulative. Still small
  enough that a single batch's numbers (like Batch 3's clean 100/0/100) can
  legitimately be a good batch rather than a stable rate — the cumulative
  numbers are the more meaningful trend line at this point, and even those
  will keep moving as the corpus grows toward 100.

## Status

Batch 3 (60/100 cases cumulative) complete and scored. `v1-results.md` and
`v2-results.md` are unchanged. Two batches remain to reach the full
100-scenario target (Section 9).
