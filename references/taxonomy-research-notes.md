# Taxonomy v2 Research Notes

Companion document to `taxonomy-v2.md`. Records the research pass, what was rejected
and why, and open questions for future revisions. This is the first fully authored
version of the taxonomy (produced in this Stage 1 pass); it is named v2 to align
with the repo layout in Project Plan V2 Section 11.

## Sources consulted

**Security / credentials:**
- Multiple independent analyses of the Mirai botnet (west Oahu forensic summary,
  Graham Cluley/Security Week reporting on the XiongMai default-credential root
  cause, Cyber Defense Magazine on the Flashpoint/Dahua findings, CSK.gov.in
  advisory, arXiv papers on Mirai's DoS mechanics and IoT threat landscape,
  IDIoT paper citing a 2010 IPv4 scan finding ~13% of responding devices
  vulnerable to default credentials) — used to ground S1 and S2.

**OTA update reliability:**
- Android AOSP documentation on A/B (seamless) system updates
- Esper (fleet device management vendor) explainer on A/B rollback mechanics and
  the observability gap at fleet scale
- Memfault OTA testing guide (causes of bricking: power interruption mid-write,
  corrupted downloads, failed signature verification, missing rollback)
- Mender.io and Redstone OTA vendor documentation on A/B partitioning, staged
  rollout, and anti-bricking design patterns
- Used to ground O1, O2, O3, O5, O6

**Connectivity:**
- EMQX, HiveMQ, and general MQTT-client reconnect documentation on exponential
  backoff and jitter as the standard mitigation for reconnect storms
- A Medium engineering write-up citing a "50,000 devices reconnect
  simultaneously" thundering-herd scenario (illustrative industry description,
  not a specific verifiable incident — treated as illustrative, not cited as a
  documented case)
- Merobix MQTT troubleshooting guide on duplicate/non-unique client IDs causing
  connection takeover ("flapping") in real fleets
- AWS re:Post and GitHub (mqtt.js) threads on reconnect behavior
- Used to ground C1, C2, C3, C4

**Power:**
- Multiple Raspberry Pi Forums threads and independent blog write-ups
  (core-electronics.com.au, science.miketyka.com, pswiki) on SD card/filesystem
  corruption from unclean power loss, and read-only/overlayfs as the standard
  mitigation
- Interrupt (Memfault), Hubble Network, Ganssle, and In Compliance Magazine
  guides on watchdog timer design and hung-device recovery
- Used to ground P1, P2, P3, P5

**Certificate/trust-anchor lifecycle (cross-cutting Security/OTA relevance):**
- AppViewX, Encryption Consulting, and CertPulse analyses of certificate-expiry
  outages (citing publicly reported incidents at Microsoft Teams, LinkedIn, and
  Starlink, and a UK banking RTGS outage — cited by these secondary sources, not
  independently verified by me; treated as evidence that certificate-expiry
  outages are a recognized incident class, not as verified incident detail)
- AWS IoT Device Defender documentation on certificate-expiry auditing
- A vendor explainer (alldaystech.com) on IoT TLS validation depending on
  accurate device time, including the specific failure mode of a device without
  a battery-backed RTC booting with a clock in the past and rejecting valid
  certificates
- Used to ground S3, S4, S6

**Domain/field experience (prior fleet-engineering work):**
- Raspberry Pi / Greengrass sensor fleet deployment experience, as previously
  described to Claude, informed prioritization of P1 (SD card corruption from
  unclean shutdown) and C1/C4 (reconnect and offline-buffering behavior) as
  high-value, concrete checks — genericized per your instruction; no specific
  incident details from that work are asserted here beyond what you have
  actually described in this project.

## Major candidate patterns rejected and why

| Candidate | Why rejected |
|---|---|
| "No centralized logging/telemetry aggregation" | Too generic — an observability best practice, not a specific checkable field failure mode. Where it matters concretely (e.g., undetected update failures), it's captured inside O5 instead of standing alone. |
| "No documented incident response plan" | Organizational/process artifact, not a technical deployment characteristic. Not reliably detectable or falsifiable from a free-text deployment plan, and arguably out of scope for a *reliability* reviewer vs. an operations-maturity audit. |
| "Single cloud region / no multi-region redundancy" | Real risk, but it's backend/cloud infrastructure architecture, not device-fleet deployment reliability — outside this taxonomy's scope as defined in Project Plan V2 (fleet deployment reliability, not cloud SRE). |
| "No environmental/thermal enclosure design" | Real field failure cause (heat, moisture, vibration) but physical/mechanical, essentially undetectable from a text deployment plan describing software/ops posture, and not "checkable" in the sense the spec requires. |
| "No load/capacity testing before launch" | Process step, not a deployment characteristic; also overlaps heavily with O3 (staged rollout) as the actual mitigating control that *is* checkable. |
| "No certificate pinning" | Contested as a best practice (pinning has known operational downsides — it can itself cause outages during legitimate rotation) rather than a clear failure mode; folded conceptually into S3/S4 (identity uniqueness and rotation) rather than treated as its own checkable pattern. |
| "No API rate limiting on device-to-cloud traffic" | Backend-side control, not a property of the device fleet's deployment plan; also a much weaker fit to the four locked categories. |
| "No secure boot" | Considered for Security, but overlaps substantially with O6 (bootloader-level rollback/verification capability) once framed around what's detectable from a deployment plan; kept as an edge case under O6 rather than a separate entry to avoid redundancy. |
| "No NTP/time sync" as a standalone Connectivity pattern | Time sync is a connectivity-adjacent capability, but its concrete, checkable field consequence in this research pass was specifically TLS/certificate validation failure — so it's placed under Security (S6) rather than duplicated as a generic connectivity check. Flagged below as a boundary call worth revisiting. |
| "No power-on self-test (POST)" | Real embedded practice, but the failure it catches (bad hardware at boot) is largely orthogonal to the four categories' field-failure framing and not clearly checkable from a deployment-plan description. |

## Final pattern count per category

- Connectivity: 5
- Power: 5
- OTA: 5
- Security: 6
- **Total: 21** (within the 15–25 target range)

## Important research gaps

- No access to a proprietary or peer-reviewed *structured incident corpus*
  (e.g., a formal IoT postmortem database) — sourcing relied on public
  vendor/engineering blog posts, forum threads, security-research summaries,
  and arXiv papers rather than primary incident reports in most cases. Several
  secondary sources (e.g., the CertPulse piece) themselves cite public
  incidents (Microsoft Teams, LinkedIn, Starlink) that I have not independently
  verified against primary sources — treated as "recognized incident class"
  evidence, not as verified specifics, and no specific incident is asserted in
  the taxonomy itself.
- No direct research pass against formal standards text (ETSI EN 303 645, NIST
  IR 8259, IEC 62443) — these were referenced in passing by secondary sources
  but not read and cited directly. If the project wants explicit standards
  traceability, that's a follow-up research pass, not assumed here.
- The "50,000 devices reconnect simultaneously" thundering-herd figure and
  similar illustrative numbers found during research are **not** used as cited
  facts anywhere in the taxonomy — they informed prioritization only.

## Assumptions made

- A "deployment plan" is assumed to be a free-text description written by
  someone with real architectural knowledge of the fleet (per the locked v1
  spec) — patterns assume evidence *could* exist in principle in such a
  document, even if often absent.
- Where a pattern's fleet-wide-vs-device-level blast radius genuinely depends
  on deployment specifics not knowable in the abstract (e.g., whether power
  infrastructure is shared across many devices), I assigned the severity that
  applies under the *most common* real-world deployment assumption (distributed
  power, not shared circuits) and documented the escalation condition as an
  edge case rather than picking a severity that covers the worst case by
  default. This is consistent with the rubric's instruction not to score based
  on worst-case stacking without evidence.

## Taxonomy decisions that may need revisiting later

1. **S6 (time source / RTC) placement under Security rather than Connectivity**
   — defensible either way; revisit if eval corpus scenarios show reviewers
   expect it under Connectivity.
2. **P1 severity default (High, not Critical)** — assumes distributed power per
   device rather than shared site power. If prior-experience-style deployments (or the
   eval corpus) commonly describe shared power infrastructure across many
   units, this default may need to shift toward Critical with an explicit
   scope-escalation note, rather than being a documented edge case.
3. **S2 (open debug interfaces) dual default** — High by default, escalating to
   Critical only on confirmed internet-facing exposure. This directly mirrors
   the rubric's own worked example, but it is one of the harder entries to
   apply consistently and is worth extra attention during eval-corpus scenario
   design (deliberately write some scenarios that state network topology
   explicitly and some that don't, to test this default).
4. **O3 (no staged rollout) and P5 (no crash-loop protection) as High rather
   than Critical** — both become Critical-adjacent when combined with O1 or O2
   (a bad fleet-wide push with no rollback). This is handled via the rubric's
   `[COMPOUND]` mechanism rather than by raising their standalone default
   severity — flagged here in case that produces under-scoring in practice.

## Why each category is sufficiently distinct

- **Connectivity** is about the device's ability to *maintain or recover a
  network session* and behave sanely while disconnected — a runtime,
  session-level concern.
- **Power** is about the device's ability to *survive an unclean loss of
  power* and detect/recover from a hung or under-voltage state — a hardware/OS
  boot-and-runtime-integrity concern, largely orthogonal to whether the network
  is up.
- **OTA** is about the *update delivery and installation pipeline itself* —
  a distinct lifecycle event (not steady-state operation) with its own failure
  surface (verification, staging, rollback) that can occur even on a device
  with perfect connectivity and power handling.
- **Security** is about *unauthorized access and trust/identity integrity* —
  failures here are adversarial or credential/identity-lifecycle failures,
  not reliability failures in the availability sense, even though some
  (S4, S6) manifest as outages.

Overlap exists at the edges by nature of the domain (e.g., a bad OTA push
interacts with power-loss-during-write, and certificate expiry is both a
Security and an availability/Connectivity concern) — these are handled via the
rubric's compound-finding mechanism rather than by blurring category
boundaries in the taxonomy itself.
