from __future__ import annotations

import csv
from pathlib import Path

from auditforge.finding import Finding, REQUIRED_FIELDS


def parse_csv(path: str | Path) -> list[Finding]:
    input_path = Path(path)
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{input_path}: CSV file is empty")

        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            missing_list = ", ".join(missing)
            raise ValueError(f"{input_path}: missing required columns: {missing_list}")

        findings: list[Finding] = []
        for line_number, row in enumerate(reader, start=2):
            if _is_blank_row(row):
                continue
            findings.append(Finding.from_mapping(row, source=f"{input_path}:{line_number}"))

    return findings


def _is_blank_row(row: dict[str, object]) -> bool:
    return all(str(value or "").strip() == "" for value in row.values())
