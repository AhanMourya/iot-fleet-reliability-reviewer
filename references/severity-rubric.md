# Severity Rubric v1 (Locked)

Defines the three severity tiers used by all findings in the IoT Fleet Deployment
Reliability Reviewer. This rubric is authored and locked **before** the failure-mode
taxonomy, per Project Plan V2 Section 8. All taxonomy sub-patterns must map their
default severity to this document, not the reverse.

## How to use this rubric

Severity is a function of two independent axes, evaluated in this order:

1. **Scope** — does the failure affect a single device, or can it affect the fleet
   as a whole (simultaneously, or via unbounded spread from one compromised/failed
   unit)?
2. **Recovery path** — once triggered, can the failure be resolved *remotely and
   automatically*, does it require *manual/remote intervention* (e.g., a support
   ticket, a config push, a manual approval), or does it require *physical
   intervention* (truck roll, device replacement), or is there *no recovery path
   at all*?

Severity is **not** a function of how likely the triggering event is considered to
be. A rare trigger with catastrophic, unrecoverable, fleet-wide consequences is
still Critical. Likelihood is a separate concern the reviewer may note in `Risk`,
but it does not lower severity.

### Decision procedure (apply in order, stop at first match)

1. Does the failure mode, once triggered, leave affected devices with **no
   recovery path** (not even physical truck roll — e.g., permanently bricked,
   cryptographically locked out, hardware damaged) — **or** can a single event
   (bad OTA push, expired shared cert, leaked shared credential, malformed
   fleet-wide config) trigger the failure **simultaneously across the fleet**
   with only manual-per-device recovery available? → **Critical**
2. Else, does the failure require **manual or physical intervention** to recover
   (truck roll, individual reflash, manual credential reset), OR is it fleet-wide
   but a **working, evidenced, automatic recovery path** exists that meaningfully
   contains it? → **High**
3. Else (no active exploitable/triggerable failure path is evidenced; this is a
   hardening, observability, or best-practice gap) → **Advisory**

## Tier: Critical

**Criteria:** A fleet-wide failure mode with no recovery path. Either (a) the
failure has no recovery path at all for an affected device, and a single trigger
can hit many/all devices at once, or (b) the failure has no recovery path even at
the single-device level once triggered under the conditions the plan describes as
supported/expected.

**Decision rule:** Ask two questions — *"Can one bad event take out more than one
device without a human touching each one?"* and *"If it does, is remote recovery
actually possible, or does every affected device need individual manual/physical
attention?"* If the answer to the second is "no remote recovery, one device at a
time, at fleet scale" — Critical.

**IoT-specific examples:**
- No OTA rollback: a bad firmware push bricks the fleet, and un-bricking requires
  physical reflash of each device.
- A single shared default/hardcoded credential across all devices: one leak
  compromises the entire fleet simultaneously.
- No A/B partitioning and no watchdog-triggered fallback: interrupted OTA writes
  corrupt the boot partition with no automatic recovery.
- Internet-facing open debug port with no auth: any device is remotely
  compromisable, and a compromised device can pivot to others on the same
  network/fleet-management plane.

**Borderline cases:**
- A fleet-wide trigger exists, but recovery is automatic and evidenced (e.g.,
  staged rollout + automatic rollback on health-check failure) → not Critical;
  see High.
- A single-device failure is unrecoverable, but there is no plausible fleet-wide
  trigger for it (e.g., a rare hardware fault) → not Critical; see High
  (device-level, no remote recovery = truck roll).

**Distinguishing from High:** Critical requires the *combination* of
fleet-wide-capable trigger **and** no-better-than-manual-per-device recovery, or
a wholly unrecoverable single-device outcome that is nonetheless the kind of
default-config issue that would hit the whole fleet under normal operating
conditions (e.g., a default credential every unit ships with). High is either
device-level-only failures with a truck-roll recovery, or fleet-wide failures with
a working remote fix.

**Sufficient evidence:** Explicit absence of a stated mitigation for a taxonomy
sub-pattern whose default severity is Critical (e.g., "no mention of rollback
anywhere in the plan"), or an explicit description of a shared/fleet-wide
mechanism (shared credential, shared cert, centrally pushed config) with no
per-device isolation or remote-recovery mechanism described.

**Effect of uncertainty:** If the plan is silent on a mitigation whose taxonomy
default severity is Critical, assign Critical with **Confidence: MEDIUM** (not
LOW) — silence on a Critical-default sub-pattern is treated as absence, consistent
with the Evidence field's requirement to name what evidence was used ("no mention
of X"). Confidence drops to LOW only when the plan's description is too vague to
tell whether the sub-pattern even applies (e.g., unclear whether devices are
network-connected at all).

## Tier: High

**Criteria:** A device-level failure requiring manual intervention (truck roll or
equivalent per-device manual fix) to resolve, OR a fleet-wide-capable failure that
has a working but imperfect/partial/unreliable recovery path.

**Decision rule:** *"Does fixing this cost a truck roll, a manual reset, or a
support ticket per device — but the fleet as a whole isn't taken down by one
event with no way back?"* → High. Also High: *"Is there fleet-wide exposure, but
a real recovery mechanism exists and is evidenced, even if it's not perfect?"*

**IoT-specific examples:**
- No power-loss recovery: a device that loses power mid-write needs a manual
  power cycle or local reset, but only that device is affected and a human
  visit (physical or remote console) fixes it.
- OTA has automatic rollback on health-check failure, but the health check has
  no timeout defined, so a hung (not crashed) device could sit un-rolled-back
  until someone notices — fleet-wide capable trigger, but a real (if imperfect)
  recovery mechanism exists.
- No watchdog timer causes an individual device to hang and require a manual
  power cycle, with no evidence the same code path would be hit by all devices
  simultaneously.
- Reconnect logic exists but has no backoff cap, causing one device to hammer
  the broker after prolonged outages — degrades service but is recoverable via
  remote reconfiguration, not a truck roll, and is isolated per device.

**Borderline cases:**
- A partial/conditional mitigation (e.g., "power-loss recovery works if a UPS is
  installed" but UPS is only "recommended," not guaranteed in the deployment) —
  treat as High for the un-covered condition (see "Partial mitigation rule"
  below), not automatically downgraded to Advisory just because a mitigation
  exists in some configurations.
- A locally-buffered offline queue with a bounded buffer: temporary outages are
  fully recoverable (Advisory-leaning), but outages exceeding the buffer window
  cause silent, unrecoverable data loss for that device (High-leaning). Assign
  High, since the plan as described has a real, evidenced failure condition
  (buffer overflow) with no recovery of the lost data, even though the device
  itself resumes normal operation afterward. Note in `Risk` that severity is
  contingent on outage duration relative to buffer size.

**Distinguishing from Critical:** High never has "no recovery path" at
fleet-wide scale — either it's contained to one device at a time, or a real
remote/automatic recovery mechanism exists. Distinguishing from Advisory: High
describes an evidenced failure condition that *will* require intervention or
*will* cause loss/downtime under plausible operating conditions described in the
plan, not merely a theoretical gap.

**Sufficient evidence:** A described failure path with a described but
incomplete/manual/physical recovery step, or a fleet-wide mechanism with an
evidenced but imperfect automatic recovery.

**Effect of uncertainty:** If the plan is silent on a mitigation whose taxonomy
default severity is High, assign High with Confidence: MEDIUM. If the plan
describes a mitigation vaguely (e.g., "we have some retry logic for network
issues" — no detail on backoff, persistence, or scope), assign the sub-pattern's
default severity with **Confidence: LOW**, and state in `Evidence` exactly what
is missing from the description that prevents verifying the mitigation is
adequate. Do not silently upgrade to Critical or downgrade to Advisory to
compensate for vagueness — vagueness affects Confidence, not Severity.

## Tier: Advisory

**Criteria:** A best-practice gap that, based on the evidence in the plan, is
unlikely to cause a field outage on its own. Hardening, observability, or
defense-in-depth items with no currently-evidenced active failure path.

**Decision rule:** *"If I do nothing about this, does the plan as described still
function without an outage, an intervention, or data loss under normal and
plausible-abnormal operating conditions?"* If yes → Advisory.

**IoT-specific examples:**
- Debug port is open but is bound to a local-only interface / firewalled subnet
  with no described path to internet exposure — a real gap in defense-in-depth,
  but not itself an active exploitable failure path given the evidence provided.
- OTA rollback exists and is described adequately, but update logs are not
  centrally aggregated, making fleet-wide pattern detection slower — an
  observability gap, not a failure mode.
- No documented credential-rotation policy, but credentials are unique
  per-device and not defaulted.

**Borderline cases:**
- "Debug port open, network topology not described" — do not assume
  internet-facing (that would be inventing evidence); do not assume fully
  isolated either. Assign High (not Critical, not Advisory) with **Confidence:
  LOW**, and state explicitly in `Evidence` that network exposure is unstated.
  This is a deliberate default: undetermined exposure for a security-category
  finding is treated as a live but unconfirmed risk (High), not dismissed
  (Advisory) — see "Uncertain operational consequences" principle below.

**Distinguishing from High:** Advisory has no evidenced path from "gap exists" to
"outage or intervention occurs" under the conditions described. The moment a
concrete triggering condition and consequence can be articulated from the plan's
own evidence, it moves to High or Critical.

**Sufficient evidence:** The plan positively describes surrounding conditions
that contain the gap (e.g., stated network isolation, stated per-device unique
credentials), or the sub-pattern's taxonomy default is Advisory and nothing in
the plan suggests a worse-than-default condition.

**Effect of uncertainty:** Advisory is the tier that requires the *most*
evidence, not the least — it is a defensive assignment, never a default for
"we don't know." If uncertainty exists about whether a real failure path is
present, do not resolve it toward Advisory; resolve it toward the sub-pattern's
taxonomy default severity with reduced Confidence (MEDIUM/LOW). Advisory should
only be assigned when the plan's evidence actively supports "this is contained,"
not merely when the plan is silent.

## Cross-cutting rules

**Partial/conditional mitigation rule:** When a mitigation is described as
conditional (works only if X: battery level, UPS installed, manual approval
within a window, etc.), evaluate severity for the **uncovered condition** as if
the mitigation were absent for that condition. Cite the partial mitigation in the
finding's `Recommended mitigation` field (e.g., "extend rollback coverage to the
low-battery case") rather than letting it silently reduce severity. A partial
mitigation may still justify a Confidence downgrade if it's unclear how often
the uncovered condition occurs in practice — but never a Severity downgrade on
its own.

**Multiple interacting failure modes rule:** Score each taxonomy sub-pattern
independently against its own scope/recovery evidence. Do not merge findings
into a single meta-severity. If two or more findings, when combined, produce a
qualitatively worse and independently evidenced compound scenario (e.g., no OTA
rollback + fleet-wide default credential together enable a fleet-wide malicious
"update"), add a distinct finding tagged `[COMPOUND]` in its Finding line,
scored on its own merits by the same decision procedure, and cross-reference the
component finding IDs in `Evidence`. Do not speculatively stack worst-case
readings across unrelated findings that lack a stated or inferable interaction.

**Uncertain operational consequences principle:** When the plan's evidence is
insufficient to determine whether a failure path is contained (Advisory) or live
(High/Critical), default to the sub-pattern's taxonomy default severity and lower
Confidence rather than resolving the ambiguity toward the lower tier. The rubric
treats "we can't tell if this is exploitable" as a finding worth surfacing, not
a reason to suppress it — false negatives from under-scoring are treated as more
costly than false positives from over-scoring, given this tool's audit-only,
human-reviewed purpose.

**Vague deployment description principle:** A vague but present mitigation
description (e.g., "some retry logic," "handled elsewhere," "standard security
practices") is evidence of *awareness*, not evidence of *adequacy*. Treat it the
same as an unstated mitigation for severity purposes (apply the taxonomy default
severity) but note in `Evidence` that a description exists and is insufficient to
verify, and use Confidence: LOW rather than MEDIUM to distinguish this case from
pure silence.
