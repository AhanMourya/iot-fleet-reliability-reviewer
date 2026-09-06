# IoT Fleet Deployment Failure-Mode Taxonomy v2

21 checkable sub-patterns across four categories: Connectivity, Power, OTA, Security.
Severity defaults are assigned per the locked `severity-rubric.md` and must not be
altered to fit a taxonomy entry — where a default is genuinely hard to pin down, that
difficulty is documented in the entry's Edge Cases field instead.

Sources are listed by short label; full citations are in `taxonomy-research-notes.md`.

---

## Connectivity

### C1 — No Reconnect/Fallback Logic
**Category:** Connectivity
**Description:** The device has no logic to detect a dropped network connection and
re-establish it; a connection loss is either fatal (device stops functioning until
manually restarted) or silently permanent (device stays "up" but never resumes
communication).
**Why it matters in the field:** Network drops (Wi-Fi AP reboot, cellular handoff,
ISP outage, ISP router of the site itself rebooting) are routine, not exceptional,
in field IoT deployments. A device that can't recover from one is effectively
single-shot reliable.
**Typical failure mechanism:** Client code establishes a connection once at startup
with no supervising loop; on disconnect, the connection object is simply dead and
nothing re-invokes the connect path.
**Field consequence:** A common network blip (which can affect many/all devices on
the same site or carrier simultaneously) leaves the fleet dark until each device is
power-cycled or physically serviced.
**Evidence — handled:** Plan explicitly describes an automatic reconnect loop or
library-level auto-reconnect feature, ideally with a description of how it behaves
across an outage.
**Evidence — missing/inadequate:** No mention of reconnect behavior anywhere in the
plan, or an explicit statement that reconnection is manual/requires a restart.
**Default severity:** **Critical.** A single common-cause event (site network
outage) can affect the fleet simultaneously, and per the decision procedure, if the
only recovery is manual/physical per device at that scale, it's Critical — this is
the canonical example used in the locked rubric itself.
**Edge cases:** If the plan describes a fleet where devices are on independent,
uncorrelated connectivity (e.g., different cellular carriers/sites with no common
failure domain), the "simultaneous fleet-wide" premise weakens — in that case
document the reasoning and consider High instead, since it becomes a device-level
issue with no shared trigger. Do not downgrade by default; require the plan to state
the independence explicitly.
**Sources:** EMQX/HiveMQ reconnect docs; Merobix reconnect-loop troubleshooting
guide (general context on how reconnect gaps manifest in real fleets).
**Derivation:** Published evidence + field experience (prior hands-on Pi/Greengrass
deployments directly motivated prioritizing this pattern).

---

### C2 — No Backoff/Jitter on Reconnect (Reconnect Storm)
**Category:** Connectivity
**Description:** The device retries connecting immediately and repeatedly after a
disconnect, with no increasing delay and no randomization relative to other devices.
**Why it matters in the field:** When an outage affecting many devices resolves,
uncoordinated immediate retries from the whole fleet can overwhelm the
broker/server, prolonging the outage or triggering a secondary one.
**Typical failure mechanism:** Reconnect logic exists (distinguishing this from C1)
but retries on a fixed short interval with no exponential increase and no jitter
across devices.
**Field consequence:** Broker/server overload at the moment of recovery; the fleet
appears to reconnect, then drops again as the server buckles, extending the
effective outage window.
**Evidence — handled:** Plan describes exponential backoff and/or jitter in the
reconnect strategy, or names a client library/platform (e.g., AWS IoT SDK, HiveMQ
client, EMQX client) known to implement this by default.
**Evidence — missing/inadequate:** Plan describes "automatic reconnect" with a fixed
interval, or gives no detail on retry timing at all.
**Default severity:** **High.** Fleet-wide-capable trigger (a shared outage), but a
real recovery path exists — devices do eventually reconnect, even if inefficiently;
this doesn't meet the "no recovery path" bar for Critical.
**Edge cases:** For very small fleets (a handful of devices), reconnect-storm risk
is minimal even without backoff — but taxonomy default severity should not be
adjusted per-deployment-size at the taxonomy-authoring stage; that judgment belongs
to the reviewer applying the taxonomy to a specific plan, with a documented rationale
if downgraded.
**Sources:** EMQX Cloud client-development best practices; HiveMQ reconnect
handling docs; MQTT.js GitHub issue #561 on exponential backoff with jitter;
exponential-backoff-calculator industry reference.
**Derivation:** Published evidence.

---

### C3 — Non-Unique Client/Connection Identifiers
**Category:** Connectivity
**Description:** Devices share or can collide on the same connection/client
identifier (e.g., an MQTT client ID cloned from a template, a test image reused in
production), causing the broker to treat a new connection as a takeover of an
existing one.
**Why it matters in the field:** This causes "flapping" — devices being silently
disconnected by their own sibling devices — which looks like an intermittent
connectivity problem but is actually a fleet provisioning defect.
**Typical failure mechanism:** Client ID is hardcoded in a golden image or derived
from a value that isn't guaranteed unique (e.g., a static config value) rather than
a hardware serial/MAC address.
**Field consequence:** A subset of devices (however many share an ID) continuously
disconnect each other, appearing online/offline unpredictably; data loss and
alerting noise.
**Evidence — handled:** Plan states client/connection IDs are derived from a
guaranteed-unique hardware identifier (serial number, MAC address) at provisioning
time.
**Evidence — missing/inadequate:** Plan doesn't address ID uniqueness, or describes
a provisioning process (e.g., "flash the same image to all units") that plausibly
produces duplicate IDs without an explicit per-device injection step.
**Default severity:** **High.** Device-level (affects only the colliding subset),
recoverable via a remote config/identity fix once diagnosed, not a fleet-wide
unrecoverable event.
**Edge cases:** If the *entire* fleet is provisioned from a single template with no
per-device identity injection described anywhere, this could affect most/all
devices simultaneously — still High under the rubric because a remote fix (push
corrected identities) remains available, distinguishing it from Critical-tier
"no recovery path" cases.
**Sources:** Merobix "How to Fix an MQTT Client Reconnect Loop" (cloned-config/golden-image
root cause of duplicate client IDs in real fleets).
**Derivation:** Published evidence.

---

### C4 — No Bounded Local Buffering for Offline Periods
**Category:** Connectivity
**Description:** The device has no local store-and-forward mechanism for data
generated while disconnected, or has one with an undocumented/unbounded-overflow
behavior (oldest data silently dropped once a buffer fills).
**Why it matters in the field:** Field connectivity is inherently intermittent;
without buffering, every outage is a silent data-loss event, and even with
buffering, outages longer than the buffer's capacity cause loss without any error
surfaced.
**Typical failure mechanism:** Device publishes data live with no local queue, or
has a fixed-size in-memory/on-disk queue that overwrites oldest entries with no
alerting when it wraps.
**Field consequence:** Data gaps corresponding to outage duration; for outages
exceeding buffer capacity, permanent, unrecoverable data loss for that window even
though the device itself resumes normal operation afterward.
**Evidence — handled:** Plan describes a local queue/buffer with a stated capacity
and explicit behavior on overflow (e.g., alert, or an accepted/deliberate policy).
**Evidence — missing/inadequate:** No mention of offline behavior for data
generated during a network outage.
**Default severity:** **High.** A real, evidenced failure condition (buffer
exhaustion, or no buffer at all) causes unrecoverable data loss under plausible
operating conditions, but the device itself remains otherwise functional and
recovers — not fleet-wide-unrecoverable.
**Edge cases:** Severity is contingent on expected outage duration relative to
buffer size/data rate, which the reviewer should note in the finding's `Risk`
field even though it doesn't change the assigned tier by default (per the locked
rubric's cross-cutting rules).
**Sources:** Ellenex MQTT explainer (buffering/keep-alive context); general field
pattern also independently supported by prior hands-on field experience.
**Derivation:** Both.

---

### C5 — No Liveness/Heartbeat Distinguishing "Silently Dead" from "Connected"
**Category:** Connectivity
**Description:** The device/broker relationship has no mechanism (heartbeat,
keep-alive with a Last-Will-and-Testament style status message, or equivalent) to
let the operator distinguish a device that is truly connected and healthy from one
that has gone silent without triggering a formal disconnect.
**Why it matters in the field:** Without this, a hung or wedged device that hasn't
formally disconnected can look "online" indefinitely, delaying detection of a real
failure that a different taxonomy entry (e.g., P3) would otherwise cause to
recover.
**Typical failure mechanism:** No keep-alive interval configured, or no
last-will/status-topic pattern used, so the platform has no signal beyond "the TCP
socket hasn't errored."
**Field consequence:** Delayed detection of device failures generally; this is an
observability gap that compounds the field impact of other failure modes rather
than being a failure trigger itself.
**Evidence — handled:** Plan describes a keep-alive interval and/or an explicit
online/offline status mechanism (e.g., MQTT Last Will and Testament).
**Evidence — missing/inadequate:** No mention of liveness detection or device
health/status reporting.
**Default severity:** **Advisory.** No active, evidenced failure path on its own —
this is a detection/observability gap, not a trigger for downtime, consistent with
the rubric's Advisory criteria.
**Edge cases:** If combined with C1 (no reconnect) or P3 (no watchdog), the
combination meaningfully worsens outcomes (undetected + unrecoverable); consider a
`[COMPOUND]` finding referencing both when a plan's evidence supports the
interaction, per the rubric's compounding rule — don't upgrade C5 itself.
**Sources:** Ellenex MQTT explainer (keep-alive parameter purpose).
**Derivation:** Published evidence.

---

## Power

### P1 — No Power-Loss-Safe Storage / Graceful Shutdown
**Category:** Power
**Description:** The device has no protection against filesystem/data corruption
from an unclean power loss — no read-only or overlay root filesystem, no
journaling configured for data integrity, no UPS/supercap-triggered graceful
shutdown sequence.
**Why it matters in the field:** Unattended field devices (solar, mains without
backup, vehicle power) lose power unpredictably and often; this is not a rare edge
case but a routine operating condition for many deployments.
**Typical failure mechanism:** Power is cut mid-write to the root filesystem (SD
card, eMMC); the filesystem journal or the card's own wear-leveling process is
interrupted, corrupting the filesystem and leaving the device unable to boot.
**Field consequence:** Device becomes unbootable; recovery requires physical
access to reflash or replace storage — a truck roll per affected device.
**Evidence — handled:** Plan describes a read-only or overlay root filesystem, a
UPS/supercap with a clean-shutdown trigger, or an equivalent write-protection
strategy for the boot/root partition.
**Evidence — missing/inadequate:** No mention of filesystem write protection or
graceful shutdown; deployment described as "unattended" or "remote" with standard
mains/solar power and no backup mentioned.
**Default severity:** **High** by default (device-level: an individual device's
storage is corrupted by its own local power event, requiring physical
intervention for that unit). **Escalates toward Critical** if the plan describes
shared power infrastructure across many devices (e.g., a single circuit or site
generator serving the whole local cluster) such that one power event is a
fleet-wide-capable simultaneous trigger with no remote recovery — apply the
uncertain-consequences principle and note this explicitly when the plan doesn't
specify power topology.
**Edge cases:** This is one of the harder entries to score consistently — see
`taxonomy-research-notes.md` for the documented open question on this default.
**Sources:** Raspberry Pi Forums threads (SD card corruption from unclean power
loss; read-only/overlayfs as mitigation); core-electronics.com.au and
science.miketyka.com write-ups on the same root cause.
**Derivation:** Both — this pattern was directly informed by hands-on prior
Raspberry Pi field deployment experience and cross-checked against multiple
independent public sources describing the identical failure mechanism.

---

### P2 — No Brownout/Undervoltage Detection
**Category:** Power
**Description:** The device has no mechanism to detect marginal/sagging supply
voltage (brownout) and take a safe action (halt writes, log the condition, reset
cleanly) before behavior becomes undefined.
**Why it matters in the field:** Marginal power (long cable runs, cheap power
supplies, solar/battery systems under load) causes silent corruption or erratic
behavior that's harder to diagnose than a clean power-off, because the device
doesn't cleanly stop — it degrades.
**Typical failure mechanism:** Voltage droops below the level needed for reliable
operation but above full power-off; writes may partially complete, memory may
corrupt, without the device ever registering a "power loss" event.
**Field consequence:** Intermittent, hard-to-diagnose corruption or resets;
individual device requires manual diagnosis and likely physical intervention
(power supply replacement, reflash).
**Evidence — handled:** Plan mentions brownout/undervoltage detection (hardware
supervisor IC, software voltage monitoring) or explicitly specifies power
delivery margins that make brownout implausible (e.g., regulated supply with
documented headroom).
**Evidence — missing/inadequate:** No mention of voltage monitoring or power
supply margin.
**Default severity:** **High.** Device-level, requires manual/physical diagnosis
and intervention; no evidenced fleet-wide simultaneous trigger by default.
**Edge cases:** Distinguish from P1 — P1 is about safe behavior *given* a full
power loss; P2 is about detecting a *partial* power failure before it causes
undefined behavior. A plan can satisfy one without the other.
**Sources:** In Compliance Magazine watchdog-design article (brownout/voltage
supervision as a distinct concern from watchdog hang-detection).
**Derivation:** Published evidence.

---

### P3 — No Watchdog Timer for Hang Recovery
**Category:** Power
**Description:** The device has no hardware or software watchdog to detect and
recover from a hung/deadlocked application or OS state.
**Why it matters in the field:** Software hangs (deadlocks, infinite loops,
memory corruption) are a normal occurrence in long-running embedded software;
without a watchdog, the only recovery is a manual power cycle.
**Typical failure mechanism:** No watchdog peripheral configured/enabled, or a
software watchdog with no independent hardware backing (so it fails to fire if
the hang itself prevents the software watchdog from running).
**Field consequence:** Device silently stops functioning and stays wedged
indefinitely until a human notices and physically power-cycles it.
**Evidence — handled:** Plan describes a watchdog timer (hardware watchdog
preferred; software watchdog with a stated independent-failure caveat is
acceptable evidence of partial mitigation).
**Evidence — missing/inadequate:** No mention of a watchdog or hang-detection
mechanism.
**Default severity:** **High.** Device-level, truck-roll-class recovery, no
evidenced fleet-wide simultaneous trigger by default (a hang is generally a
per-device software/timing event, not a shared external trigger).
**Edge cases:** If the hang cause is a firmware bug triggered by a common input
(e.g., a specific malformed message broadcast to the whole fleet), the trigger
becomes fleet-wide-capable — this would typically surface as a `[COMPOUND]`
finding alongside O1/O3 rather than changing P3's standalone default.
**Sources:** Interrupt/Memfault watchdog best-practices guide; Hubble Network
field-reliability watchdog-pattern guide; Ganssle "Designing Great Watchdog
Timers"; Beningo "A Watchdog Timer is Needed in Every Embedded Device."
**Derivation:** Published evidence.

---

### P4 — No Remote Power-Cycle Capability
**Category:** Power
**Description:** There is no way to remotely power-cycle a device (smart PDU,
relay, platform-level reboot command reaching hardware power control) — recovery
from any hang or wedged state requires physical presence.
**Why it matters in the field:** This determines whether P3-class failures (or any
other hang) cost a support ticket resolved remotely or a truck roll. It's a
distinct capability from having a watchdog: a watchdog handles automatic recovery,
remote power-cycle handles the cases the watchdog itself doesn't catch (e.g.,
watchdog disabled, hardware-level lockup upstream of the watchdog).
**Typical failure mechanism:** No remote-controllable power relay/PDU in the
architecture; device power is "dumb" (always-on mains/battery with no cutoff
control).
**Field consequence:** Any hang the watchdog doesn't catch requires physical
intervention, with no remote fallback option at all.
**Evidence — handled:** Plan describes a remote-controllable power path (smart
plug/relay, PDU, platform-triggered hard reset) as a fallback recovery mechanism.
**Evidence — missing/inadequate:** No mention of remote power control; power
described as simply "always on."
**Default severity:** **High.** Device-level capability gap; doesn't itself cause
failures but determines whether other failures are truck-roll-class, which is
itself the checkable, consequential gap.
**Edge cases:** If P3 (watchdog) is well-evidenced as present and adequate, the
practical impact of missing P4 is smaller (fewer failure classes actually need
it) — note this interaction in `Risk` rather than downgrading severity, since the
rubric scores each sub-pattern independently.
**Sources:** General embedded reliability guidance context (Interrupt/Memfault,
Ganssle) on watchdog limitations motivating a remote-recovery fallback.
**Derivation:** Field experience, cross-checked against published watchdog
literature's discussion of watchdog limitations.

---

### P5 — No Crash-Loop / Repeated-Reset Protection
**Category:** Power
**Description:** When a watchdog (or brownout detector) resets a device
repeatedly in a short window, there's no mechanism to detect the loop, halt
further automatic resets, alert an operator, or fall back to a safe/minimal mode.
**Why it matters in the field:** A watchdog alone can turn a hang into an
infinite reset loop rather than a real recovery, if the underlying cause
(corrupted state, a bad config, a bad OTA payload) persists across reboots. This
is a known secondary failure mode of watchdog-only designs.
**Typical failure mechanism:** Device resets, boots into the same bad state
(corrupted persisted data, a config value that immediately re-triggers the
hang), and resets again, with no escalation logic.
**Field consequence:** Device appears to be resetting/rebooting rather than
cleanly hung, which can go undetected for longer (it "looks alive" on each
brief boot) while never actually recovering; requires manual intervention once
diagnosed.
**Evidence — handled:** Plan describes reset-count tracking with an escalation
path (e.g., fall back to a minimal/safe firmware image or configuration, or
alert after N resets in a window).
**Evidence — missing/inadequate:** Watchdog/reset behavior described with no
mention of loop detection or escalation.
**Default severity:** **High.** Device-level by default; recoverable via manual
intervention once the loop is noticed, not fleet-wide-unrecoverable on its own.
**Edge cases:** Becomes Critical-adjacent when the underlying persistent bad
state was pushed fleet-wide (e.g., via a bad OTA update with no rollback,
O1) — handle via `[COMPOUND]` referencing P5 and O1 rather than raising P5's
standalone default.
**Sources:** In Compliance Magazine (watchdog dependent-failure analysis
concept, adapted); general reset-loop pattern independently corroborated across
multiple watchdog-design sources reviewed for P3.
**Derivation:** Published evidence.

---

## OTA (Over-the-Air Updates)

### O1 — No Rollback / No A/B (Dual-Bank) Update Path
**Category:** OTA
**Description:** Firmware/software updates are written directly over the running
system (single-partition overwrite) with no fallback slot to revert to if the new
image is bad or the write is interrupted.
**Why it matters in the field:** This is the single most consequential OTA
failure mode: it turns "bad update" from a recoverable, remote event into a
fleet-wide bricking event requiring physical reflash.
**Typical failure mechanism:** Update client downloads and writes the new image
directly to the boot/root partition currently in use; a corrupted image, an
interrupted write (power loss, network drop mid-write), or a failed
post-update boot leaves no known-good image to fall back to.
**Field consequence:** Affected devices are unbootable and require physical
reflash — at fleet scale, a single bad push can brick the entire fleet
simultaneously with no remote recovery path.
**Evidence — handled:** Plan explicitly describes A/B (dual-bank) partitioning,
or an equivalent fallback-slot mechanism, for firmware/software updates.
**Evidence — missing/inadequate:** No mention of a fallback partition/rollback
mechanism; update process described only as "push new firmware" or similar.
**Default severity:** **Critical.** Textbook fleet-wide-capable trigger (a bad
push) with no recovery path other than physical reflash per device — this is
the explicit example used in the locked severity rubric.
**Edge cases:** A staged rollout (O3) reduces the *number* of devices exposed to
a single bad push but does not change O1's own severity — a plan can have
excellent staging and still be Critical on O1 if no rollback mechanism exists
at all, since eventually the rollout reaches devices with no recovery path.
**Sources:** Android AOSP A/B system update documentation; Esper FOTA
explainer (non-A/B devices "go fully offline with no automatic rollback path");
Memfault OTA testing guide (missing rollback as a named root cause of bricking).
**Derivation:** Published evidence.

---

### O2 — No Update Image Integrity/Signature Verification
**Category:** OTA
**Description:** The device installs an update image without verifying its
cryptographic signature (and/or hash/size) against an expected, trusted value
before applying it.
**Why it matters in the field:** Without verification, a corrupted download
(network issue) or a maliciously substituted image (if the transport or update
server is compromised) is installed exactly as if it were legitimate.
**Typical failure mechanism:** Update client downloads and applies an image
based on it successfully downloading, with no signature check step in the
pipeline.
**Field consequence:** Corrupted or malicious firmware is installed
fleet-wide as the rollout reaches each device, with consequences ranging from
bricking (if paired with O1) to full compromise.
**Evidence — handled:** Plan describes signed update images with client-side
signature verification before installation.
**Evidence — missing/inadequate:** No mention of image verification; update
process described only in terms of download and install.
**Default severity:** **Critical.** A single compromised or corrupted image
(fleet-wide-capable trigger via the shared update pipeline) installed with no
verification gate has no recovery path other than the recovery properties of
O1 — and if O1 is also missing, there is none.
**Edge cases:** If O1 (rollback) is well-evidenced as present and adequate, the
consequence of a bad O2 install is contained (device rolls back) — but O2's own
severity default should not be downgraded on that basis alone per the rubric's
per-finding scoring rule; note the mitigating interaction in `Risk` and consider
noting the reduced *compounded* risk rather than changing O2's tier.
**Sources:** Memfault OTA testing guide (failed cryptographic verification
named as a root cause category); Mender.io robust-OTA guide (signing as a core
OTA safety component).
**Derivation:** Published evidence.

---

### O3 — No Staged/Phased Rollout
**Category:** OTA
**Description:** Updates are pushed to the entire fleet at once rather than in
increasing waves (e.g., 1% → 10% → 100%) with a pause/abort gate between waves.
**Why it matters in the field:** Staging is the primary control that limits
blast radius when an update turns out to be bad despite passing pre-release
testing — testing environments rarely reproduce the full diversity of field
conditions.
**Typical failure mechanism:** Update orchestration pushes to all
registered/online devices in a single campaign with no percentage-based
gating.
**Field consequence:** A defect that testing missed reaches 100% of the fleet
before anyone can react, rather than being caught and halted after affecting a
small percentage.
**Evidence — handled:** Plan describes a phased/staged rollout strategy with
defined wave sizes and gates between waves.
**Evidence — missing/inadequate:** No mention of rollout staging; update
described as pushed to "the fleet" or "all devices" without phasing.
**Default severity:** **High.** Fleet-wide-capable amplifier, but assuming O1
(rollback) is present, a working recovery path exists even without staging —
staging controls *how many* devices are affected before someone reacts, not
*whether* they can recover. Does not independently meet the Critical "no
recovery path" bar.
**Edge cases:** If O1 is also missing, O3's practical severity is effectively
subsumed by O1's Critical rating (an unstaged push with no rollback is just a
faster, more complete version of the O1 scenario) — score both on their own
merits per the rubric and let the `[COMPOUND]` mechanism carry the combined
risk narrative.
**Sources:** Esper FOTA explainer (staged rollout controls named explicitly);
Memfault OTA testing guide (staged rollouts listed as a core defensive
measure).
**Derivation:** Published evidence.

---

### O4 — No Update Confirmation / Health-Check Gate
**Category:** OTA
**Description:** After installing an update, the device (or the fleet
orchestration layer) has no defined criteria for confirming the update
succeeded (e.g., network connectivity restored, key services running) before
marking it complete — or no timeout on that check if one exists.
**Why it matters in the field:** Without a positive health confirmation, a
device that boots but is subtly broken (e.g., hung, or running but unable to
reach the network) can be recorded as "updated successfully" indefinitely,
masking a real failure and, if paired with automatic rollback-on-failure
(O1's mechanism), preventing that rollback from ever triggering.
**Typical failure mechanism:** Update marks itself successful immediately on
boot completing, with no application-level liveness check, or a health check
exists but has no timeout, so a hung (not crashed) device is never flagged as
failed.
**Field consequence:** Devices left in a degraded state post-update, invisible
to fleet monitoring, with any automatic rollback-on-failure mechanism
neutralized because the failure condition is never detected.
**Evidence — handled:** Plan describes a defined post-update health check (with
a timeout) whose failure triggers rollback or alerting.
**Evidence — missing/inadequate:** No mention of post-update validation, or a
health check described without a timeout/failure-handling path.
**Default severity:** **High.** Fleet-wide-capable (affects every device in a
rollout), but a real recovery mechanism (O1's rollback) is presumed to exist
elsewhere in a well-formed plan — O4's gap is that the mechanism may never
*fire*, which is a serious but not on-its-own unrecoverable gap, since manual
detection and intervention remain possible.
**Edge cases:** This entry's severity assumes O1 exists; if O1 is also absent,
O4 is moot (there's nothing to gate) and the finding should reference O1 as the
primary gap.
**Sources:** Mender.io robust-OTA guide ("defining update confirmation
criteria" named as an essential practice); Esper FOTA explainer's discussion of
Android Verified Boot's first-boot check as the confirmation gate model.
**Derivation:** Published evidence.

---

### O5 — No Bootloader-Level Update/Rollback Support
**Category:** OTA
**Description:** The hardware/bootloader was not designed to support secure,
rollback-capable OTA updates at all (no A/B-capable bootloader, no signature
verification at the bootloader level) — meaning the gap cannot be fixed by a
future software update, only by different hardware or a physical
re-provisioning of every unit.
**Why it matters in the field:** This is a foreclosure risk: if discovered
after fleet deployment, none of O1/O2's software-level fixes can be
retrofitted remotely, because the boot chain itself lacks the capability.
**Typical failure mechanism:** Hardware/bootloader selection was made without
OTA reliability requirements in view (e.g., a minimal bootloader on a
cost-optimized board), and the gap is only discovered once OTA becomes
necessary in the field.
**Field consequence:** Permanent inability to safely update the fleet
remotely; every future firmware fix requires physical access to every device.
**Evidence — handled:** Plan names a bootloader/platform with documented
A/B and signature-verification support (or explicitly states the device
generation supports it).
**Evidence — missing/inadequate:** No mention of bootloader OTA capability;
device platform named without any statement of update-related bootloader
features; or software-level A/B/signing described with no confirmation that
the underlying bootloader actually supports enforcing it.
**Default severity:** **Critical.** Fleet-wide-capable (affects every unit
built on the same hardware/bootloader baseline) with genuinely no recovery
path — not even a future software fix — until physical re-provisioning.
**Edge cases:** This is the hardest OTA entry to detect from free text, since
plans may describe *intended* OTA software design (O1/O2) without stating
whether the underlying bootloader can actually enforce it. Confidence on this
finding should generally be MEDIUM–LOW unless the plan explicitly names
bootloader capabilities, per the rubric's uncertainty-handling rule — treat
silence as absence rather than assuming the bootloader is adequate.
**Sources:** OTA Forge/Medium field guide on OTA design ("the bootloader is the
constraint that bites hardest... you can't add those capabilities remotely");
Android AOSP A/B documentation implicitly confirming the bootloader-level
nature of the mechanism.
**Derivation:** Published evidence.

---

## Security

### S1 — Default or Shared Credentials
**Category:** Security
**Description:** Devices ship with, or are deployed using, a default
username/password (vendor-set or team-set) that is either never required to
change, or is identical across every unit in the fleet.
**Why it matters in the field:** This is the single most exploited real-world
IoT failure mode on record — the Mirai botnet compromised hundreds of
thousands of devices almost entirely through default/hardcoded credential
scanning, at real internet scale.
**Typical failure mechanism:** A management interface (web UI, SSH, Telnet)
accepts a default credential that was never rotated, or a credential that is
hardcoded into firmware and genuinely cannot be changed by the deploying team
at all.
**Field consequence:** A single leaked or guessed credential compromises every
device sharing it simultaneously — remote takeover, inclusion in a botnet, or
data exfiltration across the fleet at once.
**Evidence — handled:** Plan states unique, randomly generated per-device
credentials are provisioned (and, ideally, that default vendor credentials are
disabled or rotated before field deployment).
**Evidence — missing/inadequate:** No mention of credential provisioning; plan
implies a shared image/config is deployed to all units without a per-device
credential-injection step.
**Default severity:** **Critical.** Directly matches the Critical decision
rule's canonical security example: single shared credential, fleet-wide
compromise, no remote recovery of the exposure itself (rotating after the
fact doesn't undo an already-exploited window).
**Edge cases:** If the plan states credentials are hardcoded and
vendor-unchangeable (as documented in real XiongMai-derived Mirai-affected
devices), this is still Critical but the `Recommended mitigation` field should
note that software-level rotation isn't possible and hardware/vendor selection
is the actual fix — a meaningfully different remediation path worth
surfacing distinctly.
**Sources:** West Oahu Mirai forensic summary; Graham Cluley/SecurityWeek and
Cyber Defense Magazine reporting on the XiongMai/Dahua hardcoded-credential
root cause; CSK.gov.in Mirai advisory; IDIoT paper (2010 scan finding ~13% of
responding devices vulnerable to default credentials).
**Derivation:** Published evidence.

---

### S2 — Open/Exposed Debug or Management Interfaces
**Category:** Security
**Description:** A debug, administrative, or diagnostic interface (Telnet,
SSH with default config, an unauthenticated debug HTTP endpoint, a UART
console left enabled) is reachable without being explicitly scoped to a
trusted network or disabled in production.
**Why it matters in the field:** These interfaces are frequently added for
development convenience and never disabled or firewalled off before field
deployment — and they were the specific entry vector Mirai used at scale
(Telnet).
**Typical failure mechanism:** A debug service that was enabled during
development ships unchanged into the production image, with no
network-level restriction applied at deployment.
**Field consequence:** Depends heavily on network exposure — ranges from
localized risk (LAN-only) to full remote compromise of any reachable device
(internet-facing).
**Evidence — handled:** Plan explicitly states the interface is
disabled in production builds, or is restricted to a specific
trusted/management network with no path from the public internet, or requires
authentication that meets the bar described for S1.
**Evidence — missing/inadequate:** No mention of debug interface handling in
production, or a description that leaves network exposure unstated.
**Default severity:** **High**, escalating to **Critical** when the plan
explicitly confirms internet-facing exposure with no authentication. Per the
locked rubric's own worked example: undetermined exposure on a security
finding defaults to High with Confidence: LOW rather than being resolved
toward Advisory by silence, and explicit confirmation of open internet
exposure moves it to Critical (matching the Mirai/XiongMai pattern directly).
**Edge cases:** This is a genuinely difficult entry to score consistently
because most deployment plans won't state network topology in enough detail
to resolve the ambiguity either way — flagged in `taxonomy-research-notes.md`
as a priority case to test heavily in the eval corpus.
**Sources:** Mirai sources (S1 above) — Telnet-port scanning was the specific
mechanism; Graham Cluley/SecurityWeek reporting on Telnet as
hardcoded-on-by-default in the affected devices.
**Derivation:** Published evidence.

---

### S3 — No Unique Per-Device Identity / Shared Authentication Material
**Category:** Security
**Description:** Devices authenticate to backend services using a shared
secret, API key, or certificate/private key common to the whole fleet (or a
large subset), rather than a unique credential per device.
**Why it matters in the field:** This is the device-to-cloud analogue of S1:
one extracted key compromises every device that shares it, and — unlike a
web password — device-embedded keys are often extractable via physical
access to a single unit, then reusable against the entire fleet remotely.
**Typical failure mechanism:** A single API key or certificate/private key is
baked into a shared firmware image rather than being provisioned uniquely
per device at manufacturing/deployment time.
**Field consequence:** Physical or software compromise of one device yields
credentials valid for impersonating any device in the fleet to backend
services — data injection, fleet-wide data exfiltration, or command
injection depending on what the credential authorizes.
**Evidence — handled:** Plan describes per-device unique credentials/certificates
issued through an enrollment or provisioning process (e.g., a device-identity
service, per-device X.509 certs).
**Evidence — missing/inadequate:** No mention of per-device credential
provisioning; a single API key or certificate is referenced as used across
the deployment.
**Default severity:** **Critical.** Same structure as S1 — single shared
secret, fleet-wide simultaneous compromise potential, no remote undo of an
already-extracted secret.
**Edge cases:** Distinguish from S1 — S1 is about human-facing
administrative credentials (device management UI/SSH); S3 is about
machine-to-machine device identity used for normal operational
communication. A plan can score well on one and poorly on the other.
**Sources:** alldaystech.com IoT security guide (per-device identity via
unique certificates as the standard mitigation; explicit framing of "no
fleet-wide shared password" as the goal).
**Derivation:** Published evidence.

---

### S4 — No Certificate/Credential Expiry Monitoring or Rotation
**Category:** Security
**Description:** Device certificates or long-lived credentials used for
backend authentication have no tracked expiry date and no automated renewal
or rotation process before expiry.
**Why it matters in the field:** Certificate expiry is a well-documented,
recurring cause of fleet-wide simultaneous outages in both IoT and
non-IoT systems — and for IoT specifically, an expired device certificate can
mean the device loses its only channel for receiving a fix, since the fix
itself would need to travel over the now-broken authenticated channel.
**Typical failure mechanism:** A certificate is provisioned once (often with
a long validity period to minimize operational overhead) with no monitoring
of approaching expiry and no automated renewal (e.g., via EST or a similar
protocol) before the expiry date arrives.
**Field consequence:** On expiry, every device using that certificate
(or certificates from the same batch/campaign) simultaneously loses the
ability to authenticate to backend services — and if the update channel
itself depends on that authentication, there is no remote recovery path.
**Evidence — handled:** Plan describes certificate expiry monitoring/alerting
and an automated renewal process that completes before expiry.
**Evidence — missing/inadequate:** No mention of certificate lifecycle
management; certificates mentioned only in the context of initial
provisioning.
**Default severity:** **Critical.** Textbook fleet-wide simultaneous trigger
(a shared expiry date, or many devices provisioned in the same batch expiring
close together) with a real chance of no remote recovery path if the expired
credential is also what would authenticate an OTA fix — directly grounded in
documented certificate-outage incident patterns.
**Edge cases:** If the plan describes short-lived, frequently auto-rotated
certificates (reducing blast radius of any single expiry) but doesn't
describe monitoring for rotation *failures*, the finding still applies —
automation without failure monitoring just changes the trigger from "long-lived
cert expires" to "rotation silently stops working," not the underlying risk.
**Sources:** AppViewX and Encryption Consulting certificate-outage analyses;
CertPulse TLS-expiry guide (industry incident pattern, embedded-device
hardcoded-CA framing); AWS IoT Device Defender certificate-expiry-check
documentation; alldaystech.com IoT TLS guide.
**Derivation:** Published evidence.

---

### S5 — Unencrypted Data-in-Transit
**Category:** Security
**Description:** Device-to-backend (or device-to-device) communication is
sent without transport encryption (plain HTTP, unencrypted MQTT, unencrypted
UDP telemetry) rather than TLS/DTLS or an equivalent.
**Why it matters in the field:** Any network position between the device and
its destination (a compromised local network, a malicious access point, an
ISP-level observer) can read or, worse, inject data and commands.
**Typical failure mechanism:** Transport layer is configured without
TLS/DTLS, often to reduce compute overhead on constrained hardware or to
simplify early development, and the choice isn't revisited before field
deployment.
**Field consequence:** Interception of telemetry data, and — if
authentication credentials are transmitted the same way — potential
credential capture enabling the S1/S3 failure modes even if those
credentials were otherwise well-designed.
**Evidence — handled:** Plan states TLS/DTLS (or an equivalent
transport-layer encryption) is used for device communication.
**Evidence — missing/inadequate:** No mention of transport security; protocol
named without an encryption layer (e.g., "devices publish over MQTT" with no
mention of MQTTS/TLS).
**Default severity:** **High.** A real, evidenced exposure (any
network-adjacent party can intercept) with concrete consequence, but not
itself a fleet-wide simultaneous unrecoverable event the way a shared-secret
compromise (S1/S3) is — remediation is a straightforward remote
configuration change once identified, and exploitation requires an attacker
in a specific network position rather than being exploitable from anywhere on
the internet by default.
**Edge cases:** If S1 or S3 findings are also present, the compounded risk
(credentials transiting in the clear, then reused fleet-wide) is meaningfully
worse than either alone — candidate for a `[COMPOUND]` finding when the plan's
evidence supports both simultaneously.
**Sources:** alldaystech.com IoT security guide (TLS basics framing);
general context from certificate-focused sources on TLS's role in IoT
device communication.
**Derivation:** Published evidence.

---

### S6 — No Reliable Time Source for Certificate Validation
**Category:** Security
**Description:** The device has no battery-backed real-time clock (RTC) or
reliable time-sync mechanism (NTP or equivalent) that completes *before*
certificate validation is required — so after a power loss, the device may
boot believing the date is far in the past (or otherwise wrong).
**Why it matters in the field:** TLS/certificate validation is time-dependent
(certificates have validity windows); a device with no reliable clock can
fail to establish any authenticated connection after every power cycle,
specifically because it can't tell that a valid certificate is, in fact,
currently valid.
**Typical failure mechanism:** Device has no battery-backed RTC (common on
cost-optimized boards) and relies on NTP sync after boot — but the update or
telemetry channel that would need to work first is itself gated by
certificate validation that fails until time sync completes, or worse, is
never triggered if NTP itself depends on the same broken channel.
**Field consequence:** After any power loss (see P1/P2), every affected
device simultaneously fails to establish trusted connections until its clock
is corrected — a direct amplifier of the power-related categories'
consequences into the security/connectivity domain.
**Evidence — handled:** Plan describes a battery-backed RTC, or an explicit,
early-boot time-sync step that doesn't itself depend on the certificate
validation it's meant to enable (e.g., an unauthenticated or
separately-trusted time source).
**Evidence — missing/inadequate:** No mention of time source/RTC; device
platform named without confirming RTC presence.
**Default severity:** **High.** Fleet-wide-capable (any shared power event
affecting multiple RTC-less devices triggers this simultaneously), but a
recovery path generally exists (device eventually syncs time via an
unauthenticated NTP request, if the architecture allows one) — doesn't meet
the Critical "no recovery path" bar unless paired with S4 in a plan that
gates *all* connectivity behind certificate validation with no
time-sync exception.
**Edge cases:** Placement under Security rather than Connectivity is a
documented, revisitable taxonomy decision — see
`taxonomy-research-notes.md`. Strong candidate for a `[COMPOUND]` finding with
S4 (expiry) and P1/P2 (the power events that trigger it).
**Sources:** alldaystech.com IoT security guide (explicit description of the
RTC-less/wrong-clock-breaks-cert-validation failure mode).
**Derivation:** Published evidence.

---

## Severity distribution summary

| Category | Critical | High | Advisory | Total |
|---|---|---|---|---|
| Connectivity | 1 (C1) | 3 (C2, C3, C4) | 1 (C5) | 5 |
| Power | 0 | 5 (P1–P5) | 0 | 5 |
| OTA | 3 (O1, O2, O5) | 2 (O3, O4) | 0 | 5 |
| Security | 3 (S1, S3, S4) | 3 (S2, S5, S6) | 0 | 6 |
| **Total** | **7** | **13** | **1** | **21** |

Note: S2's default is dual-valued (High default, Critical on confirmed
internet-facing exposure) and is counted as High above since that's its
default absent confirming evidence, per the rubric's uncertainty rule.
