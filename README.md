# IoT Fleet Deployment Reliability Reviewer

An automated reliability-review system that audits a free-text IoT fleet
deployment plan against a researched failure-mode taxonomy, using a locked
severity rubric and validated by a 100-case blinded-ground-truth evaluation
corpus.

This is not framed as "an AI skill" or "a Claude Code prompt," because that
undersells what's actually here. The intellectual contribution of this
project is the **taxonomy**, the **severity rubric**, and the **eval
corpus** — three versioned, researched artifacts that would still be
valuable if you swapped out the underlying model entirely. AI is the
execution mechanism that applies them to a specific deployment plan; it is
not the thing being built.

## Origin

This project is grounded in real experience deploying Raspberry Pi sensor
fleets on AWS Greengrass at a company called Glocol. While running physical
devices at scale, a small, recurring set of preventable failure modes kept
showing up — dropped connections with no reconnect path, updates with no
rollback, default credentials left in place, power loss corrupting local
storage. That experience raised an obvious question: could these recurring
failure modes be caught by reviewing a deployment plan *before* a fleet
ships, rather than debugging them in the field afterward? Specific incident
details have been genericized before publication; the failure-mode
categories and the sub-patterns they informed are real.

## What this tool does

Given a free-text description of an IoT/sensor fleet deployment — how
devices connect, how they're powered, how they get updated, how they're
secured — the reviewer checks the plan against 21 researched failure-mode
sub-patterns across four categories and returns structured findings:
severity, evidence, field consequence, and a concrete recommended
mitigation for each real gap it finds.

**It is a review/audit tool, not an auto-fix tool.** It never rewrites,
redesigns, or generates a "corrected" version of your deployment plan. It
tells you what's missing, why it matters in the field, and what a fix would
look like — the decision and the implementation are yours.

Every finding is evidence-based: the reviewer either quotes/paraphrases the
specific part of your plan that indicates a gap, or explicitly says the
plan is silent on that topic. It does not invent details about your
architecture that you didn't describe, and it does not soften a finding
just because your plan gives a reasonable-sounding explanation for a gap —
see [`KNOWN_LIMITATIONS.md`](./KNOWN_LIMITATIONS.md) and
[`SKILL.md`](./SKILL.md) for the specific rules this enforces and why they
exist.

## The taxonomy and rubric, as artifacts in their own right

**`references/taxonomy-v2.md`** — 21 checkable failure-mode sub-patterns
across four categories, each with a plain-language description, why it
matters in the field, a typical failure mechanism, evidence criteria for
"handled" vs. "missing," a default severity, edge cases, and sources.

| Category | Patterns | Critical | High | Advisory |
|---|---|---|---|---|
| Connectivity | 5 | 1 | 3 | 1 |
| Power | 5 | 0 | 5 | 0 |
| OTA (updates) | 5 | 3 | 2 | 0 |
| Security | 6 | 3 | 3 | 0 |
| **Total** | **21** | **7** | **13** | **1** |

The taxonomy is grounded in a real research pass, documented in
[`references/taxonomy-research-notes.md`](./references/taxonomy-research-notes.md):
public postmortems and incident analyses (Mirai and the XiongMai
default-credential root cause, OTA-bricking case studies from Android AOSP
and fleet-management vendors, certificate-expiry outage patterns,
watchdog-timer design literature), cross-checked against the Glocol field
experience that motivated the project, with candidate patterns that turned
out to be too generic, unsupported, or undetectable from free text
explicitly rejected and documented rather than silently dropped.

**`references/severity-rubric.md`** — a three-tier model (Critical / High /
Advisory) built around two axes — blast-radius scope and recovery path —
with an explicit decision procedure and cross-cutting rules for partial
mitigation, vague descriptions, and multiple interacting failure modes. It
was pressure-tested against 11 deliberately ambiguous scenarios before
being locked, and it was never modified afterward to make a taxonomy entry
fit more comfortably — where a severity call was genuinely hard, the
taxonomy entry documents the difficulty instead.

Both were authored and locked **before** the taxonomy's sub-patterns and
the reviewer's instructions were written, specifically so severity wouldn't
get assigned ad hoc per finding.

## Evaluation methodology and results

The reviewer's actual detection performance is measured against a
100-case corpus (`evals/corpus/`), split 50 seeded (deliberately containing
1–3 known failure patterns each, including compound/interacting cases) and
50 clean (mostly gap-free, with the occasional legitimate narrow finding).
Ground truth for every case — which taxonomy IDs should fire, at what
severity, and why — was written into the corpus file **before** the
reviewer was ever run against that case, to avoid ground truth being the
reviewer's own output relabeled.

Every reviewer run is checked by a **mandatory reconciliation gate**
(`evals/harness.py`) before it's allowed to count toward any metric: the
run's own summary line must exactly match the `[SEVERITY]` tags actually
present in its findings. A case that fails this check is excluded from
scoring entirely, not silently counted — this caught real bugs during
development (see the batch trend below) and is part of why these numbers
can be trusted at face value rather than needing a second read.

The corpus was built in five batches of 20, each with its own versioned,
never-overwritten results file, so the tool's improvement over time is
demonstrable rather than asserted:

| Batch | Cases | Recall | FP rate | Severity accuracy | Gate failures | Notable event |
|---|---|---|---|---|---|---|
| [v1](./evals/results/v1-results.md) (1–20) | 20 | 96.4% → 96.4%\* | 3.6% | 96.3% → 100%\* | 1 (deliberate test) | Severity/Confidence conflation found & fixed |
| [v2](./evals/results/v2-results.md) (21–40) | 20 | 88.0% → 96.0%\* | 0.0% | 100% | 1 (genuine) | "Compensating rationale" trap found & fixed |
| [v3](./evals/results/v3-results.md) (41–60) | 20 | 100% | 0.0% | 100% | 1 (genuine, same shape as v2) | Both fixes confirmed to generalize |
| [v4](./evals/results/v4-results.md) (61–80) | 20 | 100% | 0.0% | 100% | 0 | First perfectly clean batch |
| [v5](./evals/results/v5-results.md) (81–100) | 20 | 100% | 0.0% | 100% | 0 | Corpus complete; second clean batch |

\* Before → after an in-batch SKILL.md fix, verified by re-running only the
specific case(s) that exposed the issue in isolation — never a full-batch
re-run — with the fix and its effect documented as an addendum, never as a
silent revision of the original numbers.

**Full cumulative result across all 100 cases:**

| Metric | Result |
|---|---|
| Cases scored | 97 / 100 (3 excluded by the reconciliation gate) |
| Recall | **97.4%** (127 of 130 expected findings detected) |
| False positive rate | **0.8%** (1 of 128 findings raised was unexpected) |
| Clean-case false-positive rate | **0%** (0 of 49 valid clean cases) |
| Severity accuracy | **100%** (127 of 127 correctly severity-matched) |

The story here isn't "it works" — it's that detection issues were found,
diagnosed to a specific root cause, fixed, and verified narrowly before
being trusted, twice, and that the fixes held up under later, deliberate
stress-testing (see v3–v5). The trend across batches is the actual
evidence for that; the final cumulative number alone would hide it.

**→ See [`KNOWN_LIMITATIONS.md`](./KNOWN_LIMITATIONS.md) for what's still
open** — three unresolved detection errors, one suspected-but-unconfirmed
pattern that never recurred a third time, and the structural limitations of
this eval (most importantly: it is not yet a blinded evaluation).

## Repository structure

```
iot-deployment-reviewer/
  SKILL.md                          # the review process (portable; also packaged as a Claude Code skill)
  KNOWN_LIMITATIONS.md              # open issues, honestly documented
  references/
    taxonomy-v2.md                  # 21 failure-mode sub-patterns
    severity-rubric.md              # locked 3-tier severity model
    taxonomy-research-notes.md      # sources, rejected candidates, gaps
  parsers/                          # v1.5 roadmap (structured config input) — not built yet
  evals/
    corpus/                         # 100 deployment-plan scenarios + ground truth
    results/
      v1-results.md … v5-results.md # versioned, never-overwritten eval runs
      raw-runs/                     # per-case reviewer output used for scoring
    harness.py                      # scoring script with the reconciliation gate
  examples/
    sample-review-output.md         # a full worked example of the output format
```

## Using this

The core artifacts here — the taxonomy, the severity rubric, and the review
process SKILL.md describes — are **model- and product-agnostic**. None of
them depend on Claude Code specifically; they're a researched checklist and
a decision procedure that any sufficiently capable LLM (or, in principle, a
careful human reviewer) can apply to a deployment plan. Claude Code's skill
format is one convenient packaging of that process, not the primary way to
think about this project. There's more than one reasonable way to actually
run a review, so pick whichever fits how you work.

### Option A: Using this without Claude Code (zero installation)

This is the simplest path and requires nothing beyond a plain Claude.ai
conversation:

1. Open a new chat with Claude.
2. Paste in the contents of `references/taxonomy-v2.md` and
   `references/severity-rubric.md`.
3. Paste in your deployment plan.
4. Ask Claude to review the plan against the taxonomy, following the same
   process `SKILL.md` describes: check all 21 patterns individually, cite
   evidence (or explicit silence) for each finding, apply the severity
   rubric's decision procedure, and use the locked output format from the
   taxonomy/rubric's own examples.

You can also paste in `SKILL.md` itself alongside the two reference files
if you want Claude to follow its review process and formatting rules
exactly rather than reconstructing them from the taxonomy and rubric alone
— it's a plain-text set of instructions, not something that requires
Claude Code to interpret. This path is a fully supported way to use this
project, not a fallback.

### Option B: Claude Code skill (local install)

If you already use Claude Code and want the review process available
automatically when you mention a deployment plan, without pasting files in
each time:

1. Clone or download this repository.
2. Copy (or symlink) the `iot-deployment-reviewer/` folder into your
   Claude Code skills directory (wherever your Claude Code setup looks for
   custom skills — typically a `skills/` folder in your project or user
   config; check your Claude Code version's docs if you're not sure where
   that is).
3. Restart Claude Code / reload skills if your setup requires it.

Paste or describe your IoT/sensor fleet deployment plan in free text
(architecture, connectivity, power, update process, security posture) and
ask Claude Code to review it — e.g., "review this deployment plan for
reliability issues" or "check this fleet plan against known IoT failure
patterns." The skill's description is written to trigger on this kind of
request; you don't need to invoke it by name.

**A Claude Code plugin marketplace listing is planned but not live yet.**
Until then, the manual copy/symlink step above is the only way to install
the skill locally — there's no one-click install. See
`examples/sample-review-output.md` for exactly what the output looks like
either way.

### What the reviewer needs from your plan (either option)

Free-text prose describing your architecture is sufficient — no config
files required. See the taxonomy's per-pattern "Evidence" fields if you
want to write a plan that the reviewer can evaluate as completely as
possible on a first pass.

**What it won't do:** parse structured config files directly (`parsers/` is
an explicit v1.5 roadmap item, not built), auto-fix your deployment, or
give you a finding without pointing to the specific text — or explicit
silence — that produced it. This is true regardless of which option above
you use.

## Contributing / extending

Found a case where the reviewer got something wrong? Open an issue using
the bug report template — it asks for the exact plan text, expected vs.
actual finding, and the taxonomy ID if you know it, which is the same
structure this project's own eval corpus uses, so a good bug report can
often become a new corpus case directly.

The taxonomy, rubric, and eval corpus are versioned independently by
design (see `taxonomy-research-notes.md`'s "decisions that may need
revisiting" section for known boundary calls worth reconsidering). If you
extend the taxonomy, add a new eval batch, or find a reviewer error the
current eval corpus doesn't catch:

- New taxonomy entries get a new `taxonomy-v3.md`, not an edit to v2.
- New eval cases go in `evals/corpus/` with ground truth authored *before*
  running the reviewer against them.
- A new results file (`v6-results.md`, etc.) — never overwrite an existing
  one.
- If you find and fix a SKILL.md issue, verify it against only the specific
  case(s) that exposed it before trusting a full re-run, and document the
  before/after as an addendum.

## License

MIT — see [`LICENSE`](./LICENSE).
