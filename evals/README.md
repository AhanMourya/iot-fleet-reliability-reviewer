# evals/

Per Project Plan V2 Section 9.

- `corpus/` — deployment-plan scenarios with independently-authored ground
  truth, one file per case. Target: ~100 (50 seeded / 50 clean). **Batch 1
  (cases 01–20) complete** — 10 seeded, 10 clean, spanning 12 industries.
  Ground truth for every case was written before the reviewer was ever run
  against it.
- `results/` — versioned eval runs (`v1-results.md`, `v2-results.md`, ...),
  never overwritten, so detection/false-positive/severity-accuracy trends
  are demonstrable over time. `results/raw-runs/` holds the actual reviewer
  output per case (with an eval-only `PatternID:` annotation the harness
  uses for scoring — see `harness.py`'s docstring; this annotation is not
  part of the production SKILL.md output format).
- `harness.py` — scores reviewer runs against ground truth. Runs a mandatory
  reconciliation gate per case (do the `[SEVERITY]` tags in a run match its
  own summary line?) before scoring; a case that fails the gate is excluded
  from metrics, not silently scored. Run with `python3 evals/harness.py`
  from the repo root.

See `results/v1-results.md` for Batch 1's results, including one
deliberately preserved reconciliation-gate failure (proving the gate is
enforced end-to-end) and an honest accounting of the run's actual recall/FP/
severity misses rather than a cleaned-up pass.

Remaining: batches 2–5 (cases 21–100), then a full corpus-wide `v1-results.md`
supersession once all 100 are in.
