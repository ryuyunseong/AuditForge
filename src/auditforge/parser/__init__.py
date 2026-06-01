from __future__ import annotations

from pathlib import Path

from auditforge.finding import Finding
from auditforge.parser.csv_parser import parse_csv
from auditforge.parser.json_parser import parse_json


def load_findings(path: str | Path) -> list[Finding]:
    input_path = Path(path)
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        return parse_csv(input_path)
    if suffix == ".json":
        return parse_json(input_path)

    raise ValueError(f"unsupported input format {suffix!r}; expected .csv or .json")
