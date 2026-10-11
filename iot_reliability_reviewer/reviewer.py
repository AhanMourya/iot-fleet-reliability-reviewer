"""
LLM-calling logic for the reviewer.

This is the ONLY module that talks to a model. It is a thin translation
layer: it takes a deployment plan, sends SKILL.md's review instructions
plus a schema instruction to whatever model/API is configured, and returns
the raw structured JSON for reconciliation.py to validate. It does not
itself judge findings, compute summaries, or check coverage -- see
ARCHITECTURE.md for why that split is deliberate.

Model access is intentionally pluggable: swap `call_model` for whatever
API you're using (Anthropic API, a local model, etc.) without touching
reconciliation.py, evaluation.py, or cli.py.
"""

from __future__ import annotations

import json
import os

from .reconciliation import BASE_PATTERN_IDS

SCHEMA_INSTRUCTIONS = f"""
Respond with ONLY a single JSON object (no markdown fences, no preamble),
matching this exact schema:

{{
  "case_id": "<the case identifier you were given>",
  "findings": [
    {{
      "pattern": "<one of {', '.join(BASE_PATTERN_IDS)}, or COMPOUND(id,id,...)>",
      "severity": "CRITICAL | HIGH | ADVISORY",
      "finding": "<what's missing>",
      "evidence": "<where in the input this was inferred from>",
      "risk": "<what happens in the field if unaddressed>",
      "mitigation": "<concrete fix>",
      "confidence": "HIGH | MEDIUM | LOW"
    }}
  ],
  "no_gap_patterns": ["<every base pattern id NOT covered by a finding above>"]
}}

Every one of the 21 base pattern ids ({', '.join(BASE_PATTERN_IDS)}) must
appear exactly once total, either as a finding's "pattern" or in
"no_gap_patterns". Do not include a separate summary/count field -- the
caller computes that itself.
""".strip()


def build_prompt(case_id: str, deployment_plan: str, skill_instructions: str) -> str:
    """Compose the full prompt sent to the model for one case."""
    return (
        f"{skill_instructions}\n\n"
        f"---\n\n"
        f"Case ID: {case_id}\n\n"
        f"Deployment plan to review:\n\n{deployment_plan}\n\n"
        f"---\n\n{SCHEMA_INSTRUCTIONS}"
    )


def call_model(prompt: str, model: str = "claude-sonnet-4-6") -> str:
    """
    Calls the Anthropic API and returns the raw text response.

    Requires ANTHROPIC_API_KEY to be set in the environment. Swap this
    function's body if you want to call a different model/provider --
    nothing else in the package depends on which one you use.
    """
    import urllib.request

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Export it, or replace call_model() "
            "in reviewer.py with your own model-calling logic."
        )

    body = json.dumps({
        "model": model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return "".join(
        block.get("text", "") for block in data.get("content", []) if block.get("type") == "text"
    )


def parse_model_output(raw_text: str) -> dict:
    """
    Parse the model's raw text response into the schema dict. Strips
    markdown code fences defensively, since models sometimes add them
    despite instructions not to.
    """
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    return json.loads(cleaned)


def review_case(case_id: str, deployment_plan: str, skill_instructions: str,
                 model: str = "claude-sonnet-4-6") -> dict:
    """End-to-end: build prompt, call model, parse JSON. Does not reconcile."""
    prompt = build_prompt(case_id, deployment_plan, skill_instructions)
    raw = call_model(prompt, model=model)
    return parse_model_output(raw)
