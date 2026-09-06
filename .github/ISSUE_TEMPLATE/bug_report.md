---
name: Reviewer bug report
about: Report a case where the reviewer missed a real gap, flagged something incorrectly, got a severity wrong, or produced a reconciliation mismatch.
title: "[BUG] "
labels: bug
assignees: ''
---

<!--
Thanks for reporting this. The more concrete this is, the easier it is to
turn into a new eval corpus case (see evals/corpus/ and
evals/results/v5-results.md for how this project tracks known issues) —
please try to fill in every section rather than leaving it to prose in the
description.
-->

## Deployment plan text used

<!--
Paste the exact free-text deployment plan you gave the reviewer, in full.
If it's long, that's fine — the full text matters more than brevity, since
findings are traced to specific evidence in the plan.
-->

```
(paste plan text here)
```

## Expected finding

<!--
What should the reviewer have said? Be specific: which gap (or absence of
a gap) should have been reported, and at what severity if applicable.
If you expected NO finding here and the reviewer raised one incorrectly,
say that explicitly (e.g., "expected: no finding — the plan already
describes staged rollout and signature verification").
-->

## Actual finding

<!--
What did the reviewer actually output? Paste the specific finding block(s)
verbatim if possible (severity, category, finding text, evidence,
confidence) rather than paraphrasing.
-->

```
(paste actual reviewer output here)
```

## Taxonomy ID (if known)

<!--
Which of the 21 patterns in references/taxonomy-v2.md does this relate to
(e.g., C1, P3, O2, S4)? Leave blank if you're not sure — that's fine, but
filling it in helps route the issue faster.
-->

## Type of mismatch

<!-- Check one -->

- [ ] False negative — a real gap was missed entirely
- [ ] False positive — a finding was raised that shouldn't have been
- [ ] Severity mismatch — the right gap was found, but at the wrong tier
- [ ] Confidence mismatch — severity and evidence were right, but confidence looked wrong
- [ ] Reconciliation mismatch — the summary line's counts didn't match the findings actually listed
- [ ] Other (describe below)

## Anything else worth knowing

<!--
Optional: why you think this happened (e.g., "the plan gave a rationale for
the gap and the reviewer seemed to accept it instead of flagging it" — see
KNOWN_LIMITATIONS.md for prior instances of this shape), or whether this
looks similar to an existing known limitation.
-->
