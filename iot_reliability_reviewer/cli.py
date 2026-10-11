"""
Thin CLI wrapper. No new logic lives here -- it just wires together
reviewer.py, reconciliation.py, and evaluation.py.

Usage:
    iot-review review <plan-file> [--case-id ID] [--human]
    iot-review evaluate [--runs-dir DIR] [--legacy] [--corpus-dir DIR]
"""

from __future__ import annotations

import argparse
import json
import sys

from .reviewer import review_case
from .reconciliation import reconcile, ReconciliationError
from .evaluation import score, print_report, CORPUS_DIR

DEFAULT_SKILL_INSTRUCTIONS_PATH = "SKILL.md"


def _human_readable(result) -> str:
    lines = []
    for f in result.all_findings:
        lines.append(f"[{f['severity']}] {f.get('pattern', '')}")
        lines.append(f"Finding: {f['finding']}")
        lines.append(f"Evidence: {f['evidence']}")
        lines.append(f"Risk: {f['risk']}")
        lines.append(f"Recommended mitigation: {f['mitigation']}")
        lines.append(f"Confidence: {f['confidence']}")
        lines.append("")
    lines.append(result.summary_line)
    return "\n".join(lines)


def cmd_review(args) -> int:
    plan_text = open(args.plan_file, encoding="utf-8").read()
    case_id = args.case_id or "adhoc-case"

    try:
        skill_instructions = open(args.skill, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"warning: {args.skill} not found; sending plan without SKILL.md context", file=sys.stderr)
        skill_instructions = "Review this IoT deployment plan for reliability gaps."

    payload = review_case(case_id, plan_text, skill_instructions, model=args.model)

    try:
        result = reconcile(payload)
    except ReconciliationError as e:
        print(f"error: model output could not be reconciled: {e}", file=sys.stderr)
        return 2

    if not result.valid:
        print("INVALID -- reconciliation failed:", file=sys.stderr)
        for e in result.errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.human:
        print(_human_readable(result))
    else:
        print(json.dumps({
            "case_id": result.case_id,
            "valid": result.valid,
            "summary": result.summary_line,
            "summary_counts": result.summary_counts,
            "findings": result.all_findings,
        }, indent=2))
    return 0


def cmd_evaluate(args) -> int:
    results = score(args.runs_dir, corpus_dir=args.corpus_dir, legacy=args.legacy)
    print_report(results)
    return 0 if results["n_invalid"] == 0 else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="iot-review")
    sub = parser.add_subparsers(dest="command", required=True)

    p_review = sub.add_parser("review", help="Review a single deployment plan file")
    p_review.add_argument("plan_file")
    p_review.add_argument("--case-id", default=None)
    p_review.add_argument("--skill", default=DEFAULT_SKILL_INSTRUCTIONS_PATH)
    p_review.add_argument("--model", default="claude-sonnet-4-6")
    p_review.add_argument("--human", action="store_true", help="Print human-readable output instead of JSON")
    p_review.set_defaults(func=cmd_review)

    p_eval = sub.add_parser("evaluate", help="Score run files against the eval corpus")
    p_eval.add_argument("--runs-dir", default="evals/results/raw-runs")
    p_eval.add_argument("--corpus-dir", default=CORPUS_DIR)
    p_eval.add_argument("--legacy", action="store_true", default=True,
                         help="Parse prose run files (default: on, matches existing corpus format)")
    p_eval.set_defaults(func=cmd_evaluate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
