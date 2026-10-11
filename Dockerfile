FROM python:3.12-slim

# Links this container package to the repo on github.com (shows up under the repo's "Packages")
LABEL org.opencontainers.image.source="https://github.com/AhanMourya/iot-fleet-reliability-reviewer"
LABEL org.opencontainers.image.description="IoT Fleet Deployment Reliability Reviewer: deterministic reconciliation + evaluation CLI (iot-review)"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY pyproject.toml README.md ./
COPY iot_reliability_reviewer ./iot_reliability_reviewer
RUN pip install --no-cache-dir .

# Research artifacts the CLI's default paths expect (SKILL.md, corpus, existing runs)
COPY SKILL.md ./
COPY references ./references
COPY evals ./evals

# Usage: docker run --rm ghcr.io/ahanmourya/iot-fleet-reliability-reviewer evaluate
ENTRYPOINT ["iot-review"]
CMD ["--help"]
