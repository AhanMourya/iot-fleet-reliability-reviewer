"""
Evaluation harness, packaged as real code.

This replaces evals/harness.py's role, but scores through
reconciliation.py rather than re-implementing the reconciliation gate
inline. It supports two input modes:

1. Native JSON run files (the Phase 2 pipeline's actual output going
   forward): evals/results/raw-runs-json/case-NN.json
2. Legacy prose run files (evals/results/raw-runs/case-NN-run.md, the v1-v5
   format) via `legacy_run_to_payload`, so the existing 100-case corpus can
   be re-scored through the new engine WITHOUT re-running the LLM, as a
   direct check that the new engine reproduces the old numbers.

Ground-truth parsing is unchanged from harness.py (same corpus files,
same "## Ground Truth" table format).
"""

from __future__ import annotations

import glob
import json
import os
import re

from .reconciliation import reconcile, ReconciliationError, BASE_PATTERN_IDS

CORPUS_DIR = "evals/corpus"


def case_id_from_path(path: str) -> str:
    base = os.path.basename(path)
    m = re.match(r"(case-\d+)", base)
    return m.group(1)


def parse_ground_truth(path: str) -> dict:
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
        if pid.upper() == "PATTERN ID":
            continue
        expected[pid] = sev
    return expected


def legacy_run_to_payload(case_id: str, path: str) -> dict:
    """
    Convert a v1-v5-era prose run file into the Phase 2 JSON schema, so it
    can be scored through reconciliation.py. This does NOT trust the
    file's own "Findings: X Critical..." line -- that field doesn't exist
    in the schema at all; reconciliation.py computes it from the parsed
    findings, same as it would for a real JSON run.
    """
    text = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n(?=\[(?:CRITICAL|HIGH|ADVISORY)\])", text)

    findings = []
    for block in blocks:
        m_sev = re.match(r"\[(CRITICAL|HIGH|ADVISORY)\]", block)
        if not m_sev:
            continue
        sev = m_sev.group(1)
        m_pid = re.search(r"PatternID:\s*([A-Za-z0-9]+(?:\([^)]*\))?)", block)
        m_finding = re.search(r"Finding:\s*(.+)", block)
        m_evidence = re.search(r"Evidence:\s*(.+)", block)
        m_risk = re.search(r"Risk:\s*(.+)", block)
        m_mitigation = re.search(r"Recommended mitigation:\s*(.+)", block)
        m_conf = re.search(r"Confidence:\s*(HIGH|MEDIUM|LOW)", block)
        if not (m_pid and m_finding and m_conf):
            continue
        findings.append({
            "pattern": m_pid.group(1),
            "severity": sev,
            "finding": m_finding.group(1).strip(),
            "evidence": m_evidence.group(1).strip() if m_evidence else "(legacy run: not captured)",
            "risk": m_risk.group(1).strip() if m_risk else "(legacy run: not captured)",
            "mitigation": m_mitigation.group(1).strip() if m_mitigation else "(legacy run: not captured)",
            "confidence": m_conf.group(1),
        })

    base_pattern_ids_used = {f["pattern"] for f in findings if not f["pattern"].upper().startswith("COMPOUND")}
    no_gap_patterns = sorted(set(BASE_PATTERN_IDS) - base_pattern_ids_used)

    return {"case_id": case_id, "findings": findings, "no_gap_patterns": no_gap_patterns}


def score(runs_dir: str, corpus_dir: str = CORPUS_DIR, legacy: bool = False,
          case_range: tuple | None = None) -> dict:
    """
    Score every case in corpus_dir against its run file in runs_dir.

    legacy=True reads `case-NN-run.md` prose files via legacy_run_to_payload.
    legacy=False reads `case-NN.json` native schema files directly.

    Returns a dict of aggregate metrics plus a per-case breakdown, mirroring
    the structure of the original evals/harness.py output.
    """
    corpus_paths = sorted(glob.glob(f"{corpus_dir}/case-*.md"))
    if case_range:
        lo, hi = case_range
        corpus_paths = [
            p for p in corpus_paths
            if lo <= int(case_id_from_path(p).split("-")[1]) <= hi
        ]

    per_case = []
    total_tp = total_fn = total_fp = 0
    total_sev_correct = total_sev_checked = 0
    clean_total = clean_with_fp = 0
    invalid_cases = []

    for corpus_path in corpus_paths:
        case_id = case_id_from_path(corpus_path)

        if legacy:
            run_path = os.path.join(runs_dir, f"{case_id}-run.md")
        else:
            run_path = os.path.join(runs_dir, f"{case_id}.json")

        if not os.path.exists(run_path):
            per_case.append({"case_id": case_id, "status": "MISSING_RUN"})
            continue

        corpus_text = open(corpus_path, encoding="utf-8").read()
        case_type = "clean" if "**Type:** clean" in corpus_text else "seeded"
        expected = parse_ground_truth(corpus_path)

        try:
            if legacy:
                payload = legacy_run_to_payload(case_id, run_path)
            else:
                payload = json.load(open(run_path, encoding="utf-8"))
            result = reconcile(payload)
        except ReconciliationError as e:
            per_case.append({"case_id": case_id, "status": f"MALFORMED: {e}"})
            invalid_cases.append(case_id)
            continue

        if not result.valid:
            invalid_cases.append(case_id)
            per_case.append({
                "case_id": case_id,
                "status": "INVALID (reconciliation failed)",
                "errors": result.errors,
            })
            continue

        found = result.base_findings
        expected_ids, found_ids = set(expected), set(found)
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
            clean_total += 1
            if fp_ids:
                clean_with_fp += 1

        per_case.append({
            "case_id": case_id, "status": "VALID", "type": case_type,
            "tp": sorted(tp_ids), "fn": sorted(fn_ids), "fp": sorted(fp_ids),
            "sev_correct": sev_correct, "sev_checked": len(tp_ids),
        })

    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else float("nan")
    fp_rate = total_fp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    clean_fp_rate = clean_with_fp / clean_total if clean_total else float("nan")
    sev_acc = total_sev_correct / total_sev_checked if total_sev_checked else float("nan")
    n_valid = sum(1 for c in per_case if c["status"] == "VALID")

    return {
        "per_case": per_case,
        "n_valid": n_valid,
        "n_invalid": len(invalid_cases),
        "invalid_cases": invalid_cases,
        "recall": recall,
        "fp_rate": fp_rate,
        "clean_fp_rate": clean_fp_rate,
        "severity_accuracy": sev_acc,
        "total_tp": total_tp,
        "total_fn": total_fn,
        "total_fp": total_fp,
    }


def print_report(results: dict) -> None:
    print("=" * 70)
    print("INVALID / MISSING CASES")
    print("=" * 70)
    for c in results["per_case"]:
        if c["status"] != "VALID":
            print(f"{c['case_id']}: {c['status']}")
            if "errors" in c:
                for e in c["errors"]:
                    print(f"    - {e}")
    print()
    print("=" * 70)
    print("AGGREGATE METRICS")
    print("=" * 70)
    print(f"Cases scored: {results['n_valid']} valid, {results['n_invalid']} invalid: {results['invalid_cases']}")
    print(f"True positives:  {results['total_tp']}")
    print(f"False negatives: {results['total_fn']}")
    print(f"False positives: {results['total_fp']}")
    r = results["recall"]
    print(f"Recall: {r:.1%}" if r == r else "Recall: n/a")
    print(f"False positive rate: {results['fp_rate']:.1%}")
    cfr = results["clean_fp_rate"]
    print(f"Clean-case FP rate: {cfr:.1%}" if cfr == cfr else "Clean-case FP rate: n/a")
    sa = results["severity_accuracy"]
    print(f"Severity accuracy: {sa:.1%}" if sa == sa else "Severity accuracy: n/a")


if __name__ == "__main__":
    import sys
    runs_dir = sys.argv[1] if len(sys.argv) > 1 else "evals/results/raw-runs"
    legacy = "--legacy" in sys.argv or True  # default: legacy mode against existing corpus
    print_report(score(runs_dir, legacy=legacy))
