from __future__ import annotations

import json
from pathlib import Path

from auditforge.finding import Finding


def parse_json(path: str | Path) -> list[Finding]:
    input_path = Path(path)
    with input_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict) and "findings" in payload:
        rows = payload["findings"]
    else:
        rows = payload

    if not isinstance(rows, list):
        raise ValueError(f"{input_path}: JSON input must be a list or an object with a findings list")

    findings: list[Finding] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{input_path}: finding #{index} must be an object")
        findings.append(Finding.from_mapping(row, source=f"{input_path}:finding #{index}"))

    return findings
