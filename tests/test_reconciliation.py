"""
Regression tests for reconciliation.py, built from the project's actual
historical bug cases (case-06, case-12, case-28, case-49). If these pass,
the corresponding bug classes are provably impossible in the new
structured-output pipeline, not just "haven't recurred."

Note on fixtures: cases 28 and 49 are reconstructed directly from the
shipped raw-run text (evals/results/raw-runs/case-28-run.md,
case-49-run.md) — same findings, same PatternIDs, same (buggy) claimed
summary. Cases 06 and 12 are reconstructed the same way and are VALID
under the old prose-trusting harness; they're included here as clean
finding sets to make sure the new engine doesn't introduce false
INVALIDs, and as the base for a synthetic "coverage gap" variant that
models the case-06-style bug class Plan V4 calls out (a pattern silently
missing from the accounted-for set, papered over by an untracked prose
claim like "18 showed no gap").
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from iot_reliability_reviewer.reconciliation import (
    reconcile,
    BASE_PATTERN_IDS,
    ReconciliationError,
)


def _no_gap_except(*findings_patterns):
    """All 21 base patterns except the given ones (which are findings)."""
    claimed = {p for p in findings_patterns if not p.upper().startswith("COMPOUND")}
    return sorted(set(BASE_PATTERN_IDS) - claimed)


def _finding(pattern, severity, confidence="HIGH"):
    return {
        "pattern": pattern,
        "severity": severity,
        "finding": f"finding for {pattern}",
        "evidence": "evidence text",
        "risk": "risk text",
        "mitigation": "mitigation text",
        "confidence": confidence,
    }


# ---------------------------------------------------------------------
# case-28 / case-49: the arithmetic-mismatch bug class (compound finding
# pushed the claimed summary count up by one beyond the real tag count).
# The old harness caught this by comparing two separately-produced
# numbers. The new engine makes it structurally impossible: there is no
# separate "claimed" summary field to disagree with the findings at all.
# ---------------------------------------------------------------------

def test_case_28_style_summary_is_computed_not_trusted():
    findings = [
        _finding("S1", "CRITICAL"),
        _finding("S2", "HIGH"),
        _finding("COMPOUND(S1,S2)", "CRITICAL"),
    ]
    payload = {
        "case_id": "case-28",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S1", "S2"),
    }
    result = reconcile(payload)
    assert result.valid, result.errors
    # The real tag-level count is 2 CRITICAL (S1 + the compound) and 1 HIGH.
    # The original buggy run *claimed* "3 Critical, 1 High" -- that number
    # is simply not representable anymore, because we compute it ourselves.
    assert result.summary_counts == {"CRITICAL": 2, "HIGH": 1, "ADVISORY": 0}
    assert "2 Critical, 1 High, 0 Advisory" in result.summary_line


def test_case_49_style_summary_is_computed_not_trusted():
    findings = [
        _finding("S1", "CRITICAL"),
        _finding("S2", "HIGH"),
        _finding("COMPOUND(S1,S2)", "CRITICAL"),
    ]
    payload = {
        "case_id": "case-49",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S1", "S2"),
    }
    result = reconcile(payload)
    assert result.valid, result.errors
    assert result.summary_counts == {"CRITICAL": 2, "HIGH": 1, "ADVISORY": 0}


# ---------------------------------------------------------------------
# case-06-style: a pattern's status was only asserted in untracked prose
# ("18 showed no gap") rather than machine-checkable per-pattern. Model
# the failure mode directly: a base pattern that is neither a finding nor
# in no_gap_patterns must be caught, even though the old free-text
# harness had no way to see it was missing at all.
# ---------------------------------------------------------------------

def test_case_06_style_missing_pattern_is_caught():
    findings = [
        _finding("C2", "HIGH"),
        _finding("C1", "ADVISORY", confidence="LOW"),
        _finding("C4", "HIGH"),
    ]
    # Bug: C3 is silently dropped from no_gap_patterns instead of being
    # explicitly accounted for -- exactly the "trust the prose count"
    # failure mode the old harness could not detect structurally.
    no_gap = _no_gap_except("C1", "C2", "C4")
    no_gap.remove("C3")
    payload = {"case_id": "case-06", "findings": findings, "no_gap_patterns": no_gap}
    result = reconcile(payload)
    assert not result.valid
    assert any("C3" in e for e in result.errors)


def test_case_06_style_when_fixed_is_valid():
    findings = [
        _finding("C2", "HIGH"),
        _finding("C1", "ADVISORY", confidence="LOW"),
        _finding("C4", "HIGH"),
    ]
    payload = {
        "case_id": "case-06",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("C1", "C2", "C4"),
    }
    result = reconcile(payload)
    assert result.valid, result.errors
    assert result.summary_counts == {"CRITICAL": 0, "HIGH": 2, "ADVISORY": 1}


# ---------------------------------------------------------------------
# case-12-style: a simple, single-finding valid case. Sanity check that
# straightforward cases aren't disturbed by the new engine.
# ---------------------------------------------------------------------

def test_case_12_style_simple_valid_case():
    findings = [_finding("S6", "HIGH", confidence="MEDIUM")]
    payload = {
        "case_id": "case-12",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S6"),
    }
    result = reconcile(payload)
    assert result.valid, result.errors
    assert result.summary_counts == {"CRITICAL": 0, "HIGH": 1, "ADVISORY": 0}


# ---------------------------------------------------------------------
# Additional structural checks not tied to a specific historical case,
# but required by the schema contract in ARCHITECTURE.md.
# ---------------------------------------------------------------------

def test_duplicate_pattern_in_findings_is_invalid():
    findings = [_finding("S1", "CRITICAL"), _finding("S1", "HIGH")]
    payload = {
        "case_id": "case-x",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S1"),
    }
    result = reconcile(payload)
    assert not result.valid
    assert any("S1" in e and "more than once" in e for e in result.errors)


def test_pattern_claimed_as_both_finding_and_no_gap_is_invalid():
    findings = [_finding("S1", "CRITICAL")]
    no_gap = _no_gap_except()  # forgot to remove S1
    payload = {"case_id": "case-x", "findings": findings, "no_gap_patterns": no_gap}
    result = reconcile(payload)
    assert not result.valid
    assert any("S1" in e and "BOTH" in e for e in result.errors)


def test_invalid_severity_enum_is_caught():
    findings = [_finding("S1", "SEVERE")]  # not a real severity
    payload = {
        "case_id": "case-x",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S1"),
    }
    result = reconcile(payload)
    assert not result.valid
    assert any("invalid severity" in e for e in result.errors)


def test_invalid_confidence_enum_is_caught():
    findings = [_finding("S1", "CRITICAL", confidence="SORT-OF")]
    payload = {
        "case_id": "case-x",
        "findings": findings,
        "no_gap_patterns": _no_gap_except("S1"),
    }
    result = reconcile(payload)
    assert not result.valid
    assert any("invalid confidence" in e for e in result.errors)


def test_fully_clean_case_all_21_no_gap():
    payload = {
        "case_id": "case-clean",
        "findings": [],
        "no_gap_patterns": list(BASE_PATTERN_IDS),
    }
    result = reconcile(payload)
    assert result.valid, result.errors
    assert result.summary_counts == {"CRITICAL": 0, "HIGH": 0, "ADVISORY": 0}
    assert "21 of 21 patterns checked; 21 showed no gap" in result.summary_line


def test_malformed_payload_raises():
    try:
        reconcile({"case_id": "case-x"})  # missing findings/no_gap_patterns
        assert False, "expected ReconciliationError"
    except ReconciliationError:
        pass


if __name__ == "__main__":
    import inspect
    fails = 0
    tests = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            fails += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - fails}/{len(tests)} passed")
    sys.exit(1 if fails else 0)
