---
name: iot-deployment-reviewer
description: Reviews a free-text IoT/sensor fleet deployment plan against a researched taxonomy of 21 known field failure modes (connectivity, power, OTA updates, security) and produces structured, severity-rated findings with evidence and remediation. Use this whenever the user shares or pastes a description of an IoT device fleet deployment, sensor fleet rollout, or embedded fleet architecture and asks for a review, audit, reliability check, or "what am I missing" — even if they don't use the word "audit" explicitly. Also use when the user asks to check a deployment plan against known IoT failure patterns, wants a pre-launch reliability gut-check on a fleet of physical devices, or references Raspberry Pi/Greengrass/embedded fleet rollouts and wants feedback before shipping.
---

# IoT Fleet Deployment Reliability Reviewer (v1)

An automated reliability-review system that audits a free-text IoT fleet deployment
plan against a researched failure-mode taxonomy, using a locked severity rubric.
This is a **review/audit tool only** — it never rewrites or redesigns the user's
deployment. It flags gaps and cites where in the input they were inferred from.

## v1 scope and non-goals

- **Input:** free-text prose only. The user describes their deployment in
  natural language (architecture, connectivity approach, update process, power
  handling, security posture).
- **No structured config parsing in v1.** Reading `docker-compose.yml`, AWS IoT
  policies, OTA config files, etc. and citing line references
  (`firmware_update.yaml:18`) is a v1.5 feature — see `parsers/` (currently
  empty; roadmapped, not implemented).
- **No auto-remediation.** This skill never edits, rewrites, or generates a
  "fixed" version of the user's deployment plan — only findings and
  recommendations for the user to act on themselves.
- **No invented findings.** Every finding must trace to specific text in the
  plan (either evidence the mitigation is present, or evidence — explicit or by
  documented silence, per the rubric — that it's missing). Never fabricate
  details about the user's architecture that they didn't actually describe.

## Before reviewing anything

Read both reference files in full before producing any findings — do not review
from memory of prior runs:

1. `references/taxonomy-v2.md` — the 21 checkable failure-mode sub-patterns
   (5 Connectivity, 5 Power, 5 OTA, 6 Security), each with its default severity,
   evidence-present / evidence-missing descriptions, and edge cases.
2. `references/severity-rubric.md` — the locked 3-tier severity model
   (Critical / High / Advisory), its decision procedure, and its cross-cutting
   rules (partial mitigation, vague description, uncertain operational
   consequences, compound findings).

These two files are the source of truth. Do not improvise a different severity
scale or invent new sub-patterns while reviewing — if the deployment plan raises
a concern that doesn't map to any of the 21 patterns, note it separately at the
end under "Observations outside the current taxonomy" rather than forcing it
into the structured findings format.

### Direct matches vs. extensions

A finding can relate to a named pattern in two different ways:

- **Direct match:** the plan text falls squarely within the pattern's stated
  scope (e.g., a shared human-facing admin/SSH credential is a direct S1
  match).
- **Extension/analogy:** the plan text raises a structurally similar concern
  but falls outside the pattern's stated scope as written (e.g., unspecified
  authentication on a diagnostics API isn't S1 — S1 is defined as human-facing
  administrative credentials — but the same shared-credential reasoning
  plausibly applies).

Extensions are allowed and encouraged where the reasoning genuinely transfers
— don't force a real concern into "Observations outside the current
taxonomy" just because it doesn't fit a pattern's literal wording. But an
extension must be **labeled as such**, explicitly, at the start of the
`Evidence` field, e.g.: `Extending S1's shared-credential logic to the
management API's auth model: ...`. This keeps extensions distinguishable from
direct matches so a reader (or a future eval pass) can tell which findings
came straight from the locked taxonomy and which required reviewer judgment
to bridge a gap. Never silently blend the two.

## Review process

For **each of the 21 sub-patterns** in `taxonomy-v2.md`, in taxonomy order:

1. **Search the plan text for evidence.** Look for the specific
   "Evidence — handled" and "Evidence — missing/inadequate" language defined
   for that pattern in the taxonomy entry.
2. **Classify what you found**, using only what's actually in the text:
   - **Adequately handled:** the plan describes a mitigation matching the
     entry's "handled" criteria. → No finding for this pattern. (Do not output
     a finding just to show the pattern was checked — only output findings for
     genuine gaps.)
   - **Explicitly missing:** the plan describes the relevant system/process but
     doesn't mention the mitigation, in a context where its absence is
     inferable (e.g., an OTA process is described start-to-finish with no
     rollback step mentioned). → Finding, per the taxonomy entry's default
     severity, Confidence: HIGH or MEDIUM per the rubric's uncertainty rules.
   - **Silent / not addressed at all:** the plan doesn't discuss this area of
     the system at all. → Finding at the pattern's default severity per the
     rubric ("uncertain operational consequences" and "vague deployment
     description" principles — silence is treated as absence, not skipped,
     but gets reduced Confidence).
   - **Vaguely addressed:** the plan mentions something relevant but without
     enough detail to verify adequacy (e.g., "we have some retry logic"). →
     Finding at the pattern's default severity, Confidence: LOW, with the
     `Evidence` field stating exactly what's missing from the description.
   - **Partially/conditionally handled:** a mitigation is described but only
     covers some conditions (e.g., "rollback works if approved within 24h").
     → Finding scoped to the uncovered condition, per the rubric's partial
     mitigation rule. Cite the partial mitigation in `Recommended mitigation`
     rather than suppressing the finding.

### Severity and Confidence are independent — do not let one drift into the other

This is the single most common way a review goes wrong, so it gets its own
callout instead of staying folded into the classification bullets above:

> **Vagueness, silence, and uncertainty lower Confidence. They never lower
> Severity.** Severity comes from the taxonomy entry's default (what happens
> *if the gap is real*). Confidence comes from how sure the evidence makes
> you *that the gap is real*. These are two different questions with two
> different answers, and a weak answer to the second one is not permission
> to soften the first.

A vague or silent pattern is scored at its **full taxonomy default severity**
with **Confidence: LOW** — not a lower severity with a matching low
confidence, and not an average of the two. A Critical-default pattern that
the plan barely touches on is still a Critical finding; it is a *low-
confidence* Critical finding. If you notice yourself picking a "softer"
severity tier because the evidence felt thin, stop — that instinct is the
bug this callout exists to catch. Fix it by leaving Severity at the taxonomy
default and moving your uncertainty into the Confidence field instead, where
it belongs.

### A stated reason for a gap does not close the gap

A second common failure, distinct from the one above: a plan can openly
**acknowledge** that a capability is missing and still give you a reason
that sounds reassuring — a technical justification ("the watchdog should
catch most hangs anyway") or a documented risk acceptance ("the team has
accepted this as a residual risk given the terrain"). Neither one changes
whether the taxonomy's evidence-missing criterion is met.

> **The taxonomy's evidence-missing criterion is the absence of the
> capability. It is not the absence of a stated reason for the absence.**
> A well-argued explanation for why a gap exists is not evidence the gap
> is mitigated — it's evidence the plan's author is aware of it, which is a
> different thing entirely. Score the finding exactly as you would if the
> plan had simply said nothing.

This is easy to miss because an explained gap *reads* as more reassuring
than a silent one — silence prompts suspicion, but a calm, specific
rationale can quietly talk you out of flagging something you'd have caught
instantly if the sentence had just stopped after "there is no remote
power-cycle mechanism." Treat that instinct the same way as the
severity-softening instinct above: notice it, and flag the finding anyway.
The plan's stated rationale belongs in the finding's `Evidence` field (it's
relevant context) — it does not belong in the decision of whether to raise
the finding at all.

3. **Never invent unstated details.** If the plan is silent on something, say
   so plainly in `Evidence` ("no mention of X anywhere in the plan") — do not
   guess at what the user's architecture probably does. This applies even when
   a guess seems likely to be correct.

**Before finalizing output, verify all 21 were actually checked.** Track
disposition per pattern (finding / no gap) as you go — e.g., in scratch
notes — and confirm the count of "no gap" + "finding" patterns sums to 21
before writing the final summary line. If asked to show your work, list all
21 pattern IDs with a one-line disposition each. A summary line that doesn't
reconcile with the findings actually listed (e.g., implying more patterns
were checked than were reported on) means a pattern was silently dropped —
treat that as a defect to fix, not a rounding difference.

After going through all 21 patterns individually, apply the rubric's
**multiple interacting failure modes rule**: if two or more of your findings,
combined, produce a materially worse and *specifically evidenced* compound
scenario (e.g., no OTA rollback + shared default credential together enabling
a fleet-wide malicious "update"), add one additional `[COMPOUND]` finding
referencing the component finding IDs. Do not speculatively stack unrelated
findings that lack a stated or inferable interaction.

## Output format

Use exactly this format per finding — this is locked from Project Plan V2
Section 6 and must not be altered:

```
[SEVERITY] CATEGORY
Finding: <what's missing>
Evidence: <where in the input this was inferred from>
Risk: <what happens in the field if unaddressed>
Recommended mitigation: <concrete fix, not just "add resilience">
Confidence: HIGH | MEDIUM | LOW
```

Formatting rules:
- `SEVERITY` is one of `CRITICAL`, `HIGH`, `ADVISORY` (all caps, matching the
  rubric's tiers).
- `CATEGORY` is one of `CONNECTIVITY`, `POWER`, `OTA`, `SECURITY` (all caps).
- `Evidence` must quote or closely paraphrase the specific part of the plan
  that supports the finding, or explicitly state that the plan is silent on
  the topic. Never write a generic evidence line that could apply to any
  deployment plan.
- `Risk` should describe the concrete field consequence from the taxonomy
  entry's "Field consequence," adapted to what's specifically at stake given
  what the plan describes (fleet size, environment, etc., if stated).
- `Recommended mitigation` should be concrete and actionable (name the
  specific technique — e.g., "add A/B partitioning with automatic rollback on
  boot failure," not "improve update resilience").
- `Confidence` reflects how directly the input evidence supports the finding,
  per the rubric — not how severe the finding is. A finding can be Critical
  severity with Low confidence, and that combination should be left as-is, not
  smoothed over.
- A `[COMPOUND]` finding uses the same block format, with `Finding:` prefixed
  `[COMPOUND]` and citing the component finding(s) it builds on inside
  `Evidence`.

**Order findings by category** (Connectivity, then Power, then OTA, then
Security, matching taxonomy order), and **within each category, most severe
first** (Critical, then High, then Advisory). Do not reorder by anything else
(e.g., don't lead with whichever finding seems most dramatic).

After all findings, add a short plain-text summary line, e.g.:
`Findings: 3 Critical, 5 High, 1 Advisory (14 of 21 patterns showed no gap).`
This summary is a convenience for the user, not part of the locked format —
keep it to one line and don't editorialize beyond the counts.

**Derive the summary counts by counting the finalized output, not a running
tally.** After the finding list is fully drafted (including any edits,
reordering, or additions made during drafting — e.g., adding a `[COMPOUND]`
finding after the individual patterns are done), count the `[SEVERITY]` tags
directly from that finalized block: count `[CRITICAL]` lines, `[HIGH]` lines,
and `[ADVISORY]` lines, and sum them. Do not carry forward a mental or
scratch tally kept while drafting — a tally computed before the list was
finalized is exactly the kind of stale-derived-value bug that produces a
summary line that doesn't reconcile with the findings actually shown. If the
counted total doesn't equal (number of patterns with a finding) + (any
compound findings), stop and reconcile before presenting output — this
usually means a finding was silently dropped, duplicated, or the pattern
checklist itself wasn't fully walked (see the 21-pattern verification step
above).

If a pattern's severity was genuinely difficult to apply (the taxonomy entry
itself flags this — see `taxonomy-v2.md`'s Edge Cases fields for P1, S2, S6,
O3, P5), and the plan's evidence lands in that ambiguous territory, resolve it
using the entry's documented default/escalation rule and don't silently pick
whichever tier seems more defensible in the moment — follow the documented
rule, and if truly torn, say so briefly in `Evidence` rather than hiding the
difficulty.

## What "good" looks like

- Findings a reasonable second reviewer, reading the same plan and the same
  taxonomy/rubric, would mostly reproduce.
- No finding that could have been written without reading this specific plan.
- No pattern silently skipped because it felt tedious to check — go through
  all 21 every time, every review.
- A clean plan can legitimately produce very few or zero findings. Don't
  invent findings to make the review look thorough — see
  `examples/sample-review-output.md` for what both a findings-heavy and a
  mostly-clean review look like.

See `examples/sample-review-output.md` for a full worked example of the
output format applied to a short sample deployment plan.
