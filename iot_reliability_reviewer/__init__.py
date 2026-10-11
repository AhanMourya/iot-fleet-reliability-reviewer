"""
iot_reliability_reviewer -- executable reconciliation and evaluation layer
for the IoT Fleet Deployment Reliability Reviewer.

This package does not reimplement the review logic in SKILL.md. It packages
the mechanical, non-judgment parts (structural validation of LLM output,
and eval scoring) as real, deterministic, testable code. See ARCHITECTURE.md
in the repo root for the full deterministic/LLM boundary.
"""

from .reconciliation import reconcile, ReconciliationResult, ReconciliationError, BASE_PATTERN_IDS
from .reviewer import review_case, build_prompt, call_model, parse_model_output
from .evaluation import score, print_report

__version__ = "1.1.0"

__all__ = [
    "reconcile", "ReconciliationResult", "ReconciliationError", "BASE_PATTERN_IDS",
    "review_case", "build_prompt", "call_model", "parse_model_output",
    "score", "print_report",
    "__version__",
]
