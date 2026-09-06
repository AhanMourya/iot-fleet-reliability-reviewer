#!/usr/bin/env python3
"""
Eval harness for the IoT Fleet Deployment Reliability Reviewer.

Reads paired files:
  evals/corpus/case-NN-slug.md          -- deployment plan + ground truth table
  evals/results/raw-runs/case-NN-run.md -- reviewer's actual output for that case

For each case:
  1. Reconciliation gate (MANDATORY): count [CRITICAL]/[HIGH]/[ADVISORY] tags
     directly in the run file and compare to that file's own "Findings: ..."
     summary line. If they don't match, the case's run is INVALID and is
     excluded from scoring entirely -- never silently scored anyway.
  2. For valid cases: compare the set of taxonomy PatternIDs found (excluding
     COMPOUND entries, which aren't part of the 21-pattern base) against the
     case's ground truth to compute true positives, false negatives, false
     positives, and severity-match accuracy on true positives.

Outputs aggregate recall, false-positive rate, and severity accuracy, plus
a per-case table, to stdout. v1-results.md is written by hand from this
output (not auto-generated) so methodology notes and caveats can be added
alongside the numbers.

Note on PatternID tags: the `PatternID:` line in each run file is an
eval-harness-only annotation, appended after `Confidence:` in each finding
block. It is NOT part of the locked, user-facing SKILL.md output format from
Project Plan V2 Section 6 -- it exists solely so this harness can match
findings to taxonomy IDs programmatically. Production reviewer output shown
to end users omits it.
"""

import re
import glob
import os
from collections import defaultdict

CORPUS_DIR = "evals/corpus"
RUNS_DIR = "evals/results/raw-runs"

SEVERITIES = ("CRITICAL", "HIGH", "ADVISORY")


def case_id_from_path(path):
    base = os.path.basename(path)
    m = re.match(r"(case-\d+)", base)
    return m.group(1)


def parse_ground_truth(path):
    """Returns dict: pattern_id -> severity, for base (non-COMPOUND) patterns."""
    text = open(path, encoding="utf-8").read()
    if "## Ground Truth" not in text:
        raise ValueError(f"No Ground Truth section in {path}")
    gt_section = text.split("## Ground Truth", 1)[1]
    rows = re.findall(
        r"\|\s*([A-Za-z0-9]+(?:\([^)]*\))?)\s*\|\s*(CRITICAL|HIGH|ADVISORY)\s*\|",
        gt_section,
    )
    expected = {}
    for pid, sev in rows:
        if pid.upper().startswith("COMPOUND"):
            continue
        if pid.upper() == "PATTERN ID":  # header row artifact
            continue
        expected[pid] = sev
    return expected


def parse_run(path):
    """
    Returns (findings, tag_counts, summary_counts, reconciled, summary_line)
    findings: list of (pattern_id, severity) for non-COMPOUND findings.
    """
    text = open(path, encoding="utf-8").read()

    # All [SEVERITY] tag occurrences, in order they appear as finding headers.
    tag_lines = re.findall(r"^\[(CRITICAL|HIGH|ADVISORY)\]\s+\S+", text, re.M)
    tag_counts = {s: tag_lines.count(s) for s in SEVERITIES}

    # Each finding block: from a [SEVERITY] header to the next blank-line
    # boundary, capturing severity + PatternID within that block.
    blocks = re.split(r"\n(?=\[(?:CRITICAL|HIGH|ADVISORY)\])", text)
    findings = []
    for block in blocks:
        m_sev = re.match(r"\[(CRITICAL|HIGH|ADVISORY)\]", block)
        if not m_sev:
            continue
        sev = m_sev.group(1)
        m_pid = re.search(r"PatternID:\s*([A-Za-z0-9]+(?:\([^)]*\))?)", block)
        if not m_pid:
            continue
        pid = m_pid.group(1)
        if pid.upper().startswith("COMPOUND"):
            continue
        findings.append((pid, sev))

    m_summary = re.search(
        r"Findings:\s*(\d+)\s*Critical,\s*(\d+)\s*High,\s*(\d+)\s*Advisory",
        text,
    )
    if not m_summary:
        raise ValueError(f"No summary line found in {path}")
    summary_counts = {
        "CRITICAL": int(m_summary.group(1)),
        "HIGH": int(m_summary.group(2)),
        "ADVISORY": int(m_summary.group(3)),
    }
    summary_line = m_summary.group(0)

    reconciled = tag_counts == summary_counts
    return findings, tag_counts, summary_counts, reconciled, summary_line


def score(case_range=None):
    """case_range: optional (min, max) inclusive tuple of case numbers to include."""
    corpus_paths = sorted(glob.glob(f"{CORPUS_DIR}/case-*.md"))
    if case_range:
        lo, hi = case_range
        corpus_paths = [
            p for p in corpus_paths
            if lo <= int(case_id_from_path(p).split("-")[1]) <= hi
        ]
    per_case = []

    total_tp = total_fn = total_fp = 0
    total_sev_correct = total_sev_checked = 0
    clean_cases_total = 0
    clean_cases_with_fp = 0
    invalid_cases = []

    for corpus_path in corpus_paths:
        case_id = case_id_from_path(corpus_path)
        run_path = os.path.join(RUNS_DIR, f"{case_id}-run.md")
        if not os.path.exists(run_path):
            per_case.append({"case_id": case_id, "status": "MISSING_RUN"})
            continue

        corpus_text = open(corpus_path, encoding="utf-8").read()
        case_type = "clean" if "**Type:** clean" in corpus_text else "seeded"

        expected = parse_ground_truth(corpus_path)
        findings, tag_counts, summary_counts, reconciled, summary_line = parse_run(run_path)

        if not reconciled:
            invalid_cases.append(case_id)
            per_case.append({
                "case_id": case_id,
                "status": "INVALID (reconciliation gate failed)",
                "tag_counts": tag_counts,
                "summary_counts": summary_counts,
                "summary_line": summary_line,
            })
            continue

        found = {pid: sev for pid, sev in findings}
        expected_ids = set(expected.keys())
        found_ids = set(found.keys())

        tp_ids = expected_ids & found_ids
        fn_ids = expected_ids - found_ids
        fp_ids = found_ids - expected_ids

        sev_correct = sum(1 for pid in tp_ids if found[pid] == expected[pid])

        total_tp += len(tp_ids)
        total_fn += len(fn_ids)
        total_fp += len(fp_ids)
        total_sev_correct += sev_correct
        total_sev_checked += len(tp_ids)

        if case_type == "clean":
            clean_cases_total += 1
            if len(fp_ids) > 0:
                clean_cases_with_fp += 1

        per_case.append({
            "case_id": case_id,
            "status": "VALID",
            "type": case_type,
            "expected": expected_ids,
            "found": found_ids,
            "tp": tp_ids,
            "fn": fn_ids,
            "fp": fp_ids,
            "sev_correct": sev_correct,
            "sev_checked": len(tp_ids),
        })

    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else float("nan")
    fp_rate_patterns = total_fp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    clean_fp_rate = clean_cases_with_fp / clean_cases_total if clean_cases_total else float("nan")
    severity_accuracy = total_sev_correct / total_sev_checked if total_sev_checked else float("nan")

    print("=" * 70)
    print("PER-CASE RECONCILIATION GATE STATUS")
    print("=" * 70)
    for c in per_case:
        if c["status"] != "VALID":
            print(f"{c['case_id']}: {c['status']}")
            if "tag_counts" in c:
                print(f"    tag counts (actual):  {c['tag_counts']}")
                print(f"    summary line (claimed): {c['summary_counts']}  <- {c['summary_line']!r}")
    print()

    print("=" * 70)
    print("PER-CASE SCORING (valid cases only)")
    print("=" * 70)
    for c in per_case:
        if c["status"] != "VALID":
            continue
        print(f"{c['case_id']} [{c['type']}] "
              f"expected={sorted(c['expected']) or '-'} "
              f"tp={sorted(c['tp']) or '-'} "
              f"fn={sorted(c['fn']) or '-'} "
              f"fp={sorted(c['fp']) or '-'} "
              f"sev_correct={c['sev_correct']}/{c['sev_checked']}")
    print()

    print("=" * 70)
    print("AGGREGATE METRICS (excludes INVALID cases)")
    print("=" * 70)
    n_valid = sum(1 for c in per_case if c["status"] == "VALID")
    n_invalid = len(invalid_cases)
    print(f"Cases scored: {n_valid} valid, {n_invalid} invalid (excluded): {invalid_cases}")
    print(f"True positives:  {total_tp}")
    print(f"False negatives: {total_fn}")
    print(f"False positives: {total_fp}")
    print(f"Recall (pattern-level, seeded+clean combined): {recall:.1%}" if recall == recall else "Recall: n/a")
    print(f"False positive rate (pattern-level, of all findings raised): {fp_rate_patterns:.1%}")
    print(f"Clean-case false-positive rate ({clean_cases_with_fp}/{clean_cases_total} clean cases had >=1 unexpected finding): {clean_fp_rate:.1%}" if clean_fp_rate == clean_fp_rate else "Clean-case FP rate: n/a")
    print(f"Severity accuracy on true positives: {total_sev_correct}/{total_sev_checked} = {severity_accuracy:.1%}" if severity_accuracy == severity_accuracy else "Severity accuracy: n/a")


if __name__ == "__main__":
    import sys
    rng = None
    if len(sys.argv) == 3:
        rng = (int(sys.argv[1]), int(sys.argv[2]))
        print(f"Scoring cases {rng[0]}-{rng[1]} only\n")
    else:
        print("Scoring full corpus (no range given)\n")
    score(case_range=rng)
