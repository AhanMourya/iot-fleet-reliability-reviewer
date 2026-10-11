"""
Deterministic reconciliation engine.

Replaces the informal "reconciliation gate" instruction in SKILL.md, and
the count-comparison gate in the old evals/harness.py, with real code that
validates structured LLM output before it's allowed to count toward any
eval metric or be shown as a final report.

This module does NOT judge whether a finding is correct. It only checks
that the *structure* of the LLM's output is internally consistent and
complete. See ARCHITECTURE.md for the full schema contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field

BASE_PATTERN_IDS = (
    "C1", "C2", "C3", "C4", "C5",
    "P1", "P2", "P3", "P4", "P5",
    "O1", "O2", "O3", "O4", "O5",
    "S1", "S2", "S3", "S4", "S5", "S6",
)

VALID_SEVERITIES = ("CRITICAL", "HIGH", "ADVISORY")
VALID_CONFIDENCES = ("HIGH", "MEDIUM", "LOW")

REQUIRED_FINDING_FIELDS = (
    "pattern", "severity", "finding", "evidence", "risk", "mitigation", "confidence",
)


class ReconciliationError(Exception):
    """A structural problem in the LLM's JSON output. Not a review judgment."""


@dataclass
class ReconciliationResult:
    case_id: str
    valid: bool
    errors: list[str] = field(default_factory=list)
    summary_counts: dict[str, int] = field(default_factory=dict)
    summary_line: str = ""
    base_findings: dict[str, str] = field(default_factory=dict)  # pattern -> severity
    all_findings: list[dict] = field(default_factory=list)
    no_gap_patterns: list[str] = field(default_factory=list)


def _is_compound(pattern: str) -> bool:
    return pattern.upper().startswith("COMPOUND")


def reconcile(payload: dict) -> ReconciliationResult:
    """
    Validate one case's structured review output.

    payload: dict matching the schema in ARCHITECTURE.md, i.e.
        {"case_id": str, "findings": [ {...} ], "no_gap_patterns": [str]}

    Returns a ReconciliationResult. Never raises for malformed *content*
    (missing patterns, bad enum values, duplicates) -- those are collected
    as errors and the result is marked invalid. Raises ReconciliationError
    only for a payload so malformed it can't be checked at all (e.g. not a
    dict, or missing the top-level keys).
    """
    if not isinstance(payload, dict):
        raise ReconciliationError("payload must be a JSON object")

    case_id = payload.get("case_id")
    if not case_id:
        raise ReconciliationError("payload missing required 'case_id'")

    findings = payload.get("findings")
    no_gap = payload.get("no_gap_patterns")
    if findings is None or no_gap is None:
        raise ReconciliationError(
            f"{case_id}: payload missing 'findings' or 'no_gap_patterns'"
        )

    errors: list[str] = []

    # --- Rule 2: enum validity + required fields, checked per finding ---
    for i, f in enumerate(findings):
        missing = [k for k in REQUIRED_FINDING_FIELDS if k not in f or not f[k]]
        if missing:
            errors.append(f"finding[{i}] missing fields: {missing}")
            continue
        if f["severity"] not in VALID_SEVERITIES:
            errors.append(
                f"finding[{i}] (pattern {f['pattern']}) has invalid severity "
                f"'{f['severity']}', expected one of {VALID_SEVERITIES}"
            )
        if f["confidence"] not in VALID_CONFIDENCES:
            errors.append(
                f"finding[{i}] (pattern {f['pattern']}) has invalid confidence "
                f"'{f['confidence']}', expected one of {VALID_CONFIDENCES}"
            )

    # --- Rule 1: full coverage of the 21 base patterns, no dup/omission ---
    base_findings: dict[str, str] = {}
    seen_base_patterns: list[str] = []
    for f in findings:
        pattern = f.get("pattern", "")
        if _is_compound(pattern):
            continue
        if pattern not in BASE_PATTERN_IDS:
            errors.append(f"finding references unknown pattern id '{pattern}'")
            continue
        seen_base_patterns.append(pattern)
        base_findings[pattern] = f.get("severity", "")

    no_gap_clean = []
    for pid in no_gap:
        if pid not in BASE_PATTERN_IDS:
            errors.append(f"no_gap_patterns references unknown pattern id '{pid}'")
            continue
        no_gap_clean.append(pid)

    # duplicates within findings themselves
    dup_findings = {p for p in seen_base_patterns if seen_base_patterns.count(p) > 1}
    if dup_findings:
        errors.append(f"pattern(s) appear more than once in findings: {sorted(dup_findings)}")

    # duplicates within no_gap_patterns itself
    dup_no_gap = {p for p in no_gap_clean if no_gap_clean.count(p) > 1}
    if dup_no_gap:
        errors.append(f"pattern(s) appear more than once in no_gap_patterns: {sorted(dup_no_gap)}")

    findings_set = set(seen_base_patterns)
    no_gap_set = set(no_gap_clean)

    overlap = findings_set & no_gap_set
    if overlap:
        errors.append(
            f"pattern(s) claimed as BOTH a finding and a no-gap: {sorted(overlap)}"
        )

    covered = findings_set | no_gap_set
    missing_ids = set(BASE_PATTERN_IDS) - covered
    if missing_ids:
        errors.append(
            f"pattern(s) never accounted for (no finding, no no-gap entry): {sorted(missing_ids)}"
        )

    # --- Summary is COMPUTED, never trusted from a separate field ---
    summary_counts = {"CRITICAL": 0, "HIGH": 0, "ADVISORY": 0}
    for f in findings:
        sev = f.get("severity")
        if sev in summary_counts:
            summary_counts[sev] += 1

    n_checked = len(BASE_PATTERN_IDS)
    n_no_gap = len(no_gap_set)
    summary_line = (
        f"Findings: {summary_counts['CRITICAL']} Critical, "
        f"{summary_counts['HIGH']} High, {summary_counts['ADVISORY']} Advisory "
        f"({n_checked} of {n_checked} patterns checked; {n_no_gap} showed no gap)."
    )

    return ReconciliationResult(
        case_id=case_id,
        valid=(len(errors) == 0),
        errors=errors,
        summary_counts=summary_counts,
        summary_line=summary_line,
        base_findings=base_findings,
        all_findings=list(findings),
        no_gap_patterns=sorted(no_gap_set),
    )
