# Sample Review Output

This is a worked example showing the exact output format applied to a short,
fictional deployment plan. It's illustrative, not exhaustive — a real review
walks all 21 taxonomy patterns; this example shows a representative subset
across all four categories (including one Advisory-tier and one low-confidence
finding, so the format's full range is visible in one place).

## Sample input (fictional deployment plan)

> We're deploying 200 environmental sensor units (temperature/humidity)
> across several agricultural sites. Each unit runs a Raspberry Pi Zero 2 W
> with a custom Python data logger, connects over WiFi to a local gateway,
> and publishes readings via MQTT to our AWS IoT Core endpoint every 5
> minutes. All units are flashed from the same golden SD card image before
> deployment. Firmware/software updates are pushed by SSHing into each
> device or, for larger batches, using a script that copies files to each
> device and restarts the service — there's no formal OTA pipeline yet.
> Devices use a shared API key baked into the image to authenticate to AWS
> IoT Core. If a unit loses WiFi, the Python script logs an error and keeps
> trying to publish; readings that fail to publish are just dropped. Power
> comes from mains adapters at each site, with no battery backup. The SD
> card uses the standard Raspberry Pi OS Lite image with no modifications to
> the filesystem. We haven't set up a watchdog yet but plan to add one
> before full rollout.

## Output

```
[CRITICAL] CONNECTIVITY
Finding: Reconnect behavior on WiFi loss is not clearly specified
Evidence: Plan states the script "keeps trying to publish" after WiFi loss,
but gives no detail on retry timing, backoff, or whether the underlying
MQTT client reconnects the session or just retries the publish call.
Risk: Without confirmed backoff, a site-wide WiFi outage could cause
uncoordinated retries across units at that site; without confirmed
reconnect logic, the true failure behavior on prolonged disconnection is
unknown.
Recommended mitigation: Document (and if needed, implement) explicit
reconnect logic with exponential backoff and jitter for the MQTT client,
distinct from the application-level publish retry.
Confidence: LOW

[HIGH] CONNECTIVITY
Finding: No local buffering for data generated while disconnected
Evidence: Plan states explicitly that "readings that fail to publish are
just dropped."
Risk: Every WiFi outage at a site is a silent, permanent data-loss window
for the units at that site, with no way to backfill afterward.
Recommended mitigation: Add a bounded local queue (e.g., on-device SQLite
or a flat file buffer) that resyncs once connectivity is restored, with
alerting if the buffer overflows.
Confidence: HIGH

[ADVISORY] CONNECTIVITY
Finding: No liveness/heartbeat mechanism to distinguish a hung device from
a healthy one
Evidence: No mention of a keep-alive interval, status topic, or
last-will-style mechanism anywhere in the plan.
Risk: A wedged device (see the Power findings below) could appear
indistinguishable from a healthy but quiet one until someone notices
missing data.
Recommended mitigation: Add an MQTT Last Will and Testament (or equivalent)
status topic so the platform can distinguish "disconnected" from "silently
hung."
Confidence: MEDIUM

[HIGH] POWER
Finding: No power-loss-safe storage configuration
Evidence: Plan states the SD card uses "the standard Raspberry Pi OS Lite
image with no modifications to the filesystem," and power is from "mains
adapters at each site, with no battery backup."
Risk: An unclean power loss (routine at unattended field sites) can corrupt
the root filesystem, leaving the affected unit unbootable until physically
reflashed.
Recommended mitigation: Convert the root filesystem to read-only with an
overlay for writable paths, or add a small UPS/supercap with a
clean-shutdown trigger.
Confidence: MEDIUM

[HIGH] POWER
Finding: No watchdog timer currently implemented
Evidence: Plan states directly: "We haven't set up a watchdog yet but plan
to add one before full rollout."
Risk: Until added, any software hang requires a physical visit to power-
cycle the affected unit — across 200 units at multiple sites, this is a
meaningful truck-roll cost even for routine software hangs.
Recommended mitigation: Enable the Pi's hardware watchdog (or an
equivalent) before full rollout, as already planned — treat this as a
launch blocker rather than a post-launch improvement.
Confidence: HIGH

[CRITICAL] OTA
Finding: No rollback or A/B update path
Evidence: Plan states updates are "pushed by SSHing into each device" or
via "a script that copies files to each device and restarts the service,"
and explicitly notes "there's no formal OTA pipeline yet."
Risk: A bad update pushed via the batch script has no fallback — affected
units require manual SSH access or physical reflash to recover, and a
mistake in the batch script itself could affect all 200 units
simultaneously.
Recommended mitigation: Before scaling further, move to a proper OTA
pipeline with A/B (dual-bank) partitioning and automatic rollback on
boot/health-check failure.
Confidence: HIGH

[CRITICAL] OTA
Finding: No update image integrity/signature verification
Evidence: No mention of signing or verification anywhere in the described
update process (manual SSH copy / batch file-copy script).
Risk: A corrupted file copy or a compromised update source would be
applied to devices exactly as if it were legitimate, with no gate to catch
it.
Recommended mitigation: Sign update payloads and verify signatures on-
device before applying, even before a full OTA pipeline is built.
Confidence: MEDIUM

[CRITICAL] SECURITY
Finding: Shared authentication credential across the fleet
Evidence: Plan states explicitly: "Devices use a shared API key baked into
the image to authenticate to AWS IoT Core."
Risk: Extraction of the key from a single physically accessible unit
(200 units across multiple field sites) would allow impersonation of any
device in the fleet to AWS IoT Core.
Recommended mitigation: Move to per-device unique credentials (e.g.,
per-device X.509 certificates issued through AWS IoT's device provisioning
flow) rather than a single shared key baked into the golden image.
Confidence: HIGH

[CRITICAL] SECURITY
Finding: [COMPOUND] Shared credential combined with no update verification
or rollback enables a fleet-wide malicious "update" with no recovery path
Evidence: Builds on the OTA no-rollback finding, the no-signature-
verification finding, and the shared-API-key finding above — the plan
describes all three simultaneously, and the shared key is also usable to
push files via the same update path described.
Risk: Anyone who obtains the shared API key could plausibly push
unverified files to the fleet through the same channel, with no rollback
available if the result is malicious or broken — a single compromised
credential could take down or compromise all 200 units with no remote
recovery.
Recommended mitigation: Prioritize per-device credentials and signed,
rollback-capable updates together — fixing only one leaves the other as an
open path to the same outcome.
Confidence: MEDIUM

Findings: 5 Critical, 3 High, 1 Advisory (9 findings shown; this is an
illustrative excerpt, not a full 21-pattern pass).
```

## What this example demonstrates

- **Evidence is always traceable to actual text**, including explicit
  "no mention of X" statements when the plan is silent — never an invented
  architectural detail.
- **Confidence varies independently of severity** — the first finding is
  Critical severity with Low confidence, because the taxonomy's default
  severity for that pattern is Critical but the plan's description is too
  vague to be sure the gap is real.
- **A compound finding** references its component findings by their content
  rather than restating them, and is scored on its own merits per the
  rubric.
- **An Advisory-tier finding** is included so the full severity range is
  visible — not every gap in a real plan will be severe.
- Not every one of the 21 patterns needs to produce a finding — this sample
  plan happens to be gap-heavy across the areas shown; a stronger plan would
  legitimately produce a shorter, quieter report with the same format.
