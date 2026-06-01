from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


REQUIRED_FIELDS = (
    "title",
    "severity",
    "affected_asset",
    "evidence",
    "impact",
    "recommendation",
)

SEVERITY_ORDER = ("Critical", "High", "Medium", "Low", "Info")

_SEVERITY_ALIASES = {
    "critical": "Critical",
    "crit": "Critical",
    "high": "High",
    "medium": "Medium",
    "med": "Medium",
    "low": "Low",
    "info": "Info",
    "informational": "Info",
}


@dataclass(frozen=True)
class Finding:
    title: str
    severity: str
    affected_asset: str
    evidence: str
    impact: str
    recommendation: str

    @classmethod
    def from_mapping(cls, row: Mapping[str, object], *, source: str = "finding") -> "Finding":
        values = {
            field: _clean_value(row.get(field))
            for field in REQUIRED_FIELDS
        }
        if not values["title"]:
            raise ValueError(f"{source}: title is required")
        if not values["severity"]:
            raise ValueError(f"{source}: severity is required")

        values["severity"] = normalize_severity(values["severity"], source=source)
        return cls(**values)


def normalize_severity(value: str, *, source: str = "finding") -> str:
    normalized = _SEVERITY_ALIASES.get(value.strip().lower())
    if normalized is None:
        allowed = ", ".join(SEVERITY_ORDER)
        raise ValueError(f"{source}: unsupported severity {value!r}; expected one of {allowed}")
    return normalized


def _clean_value(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()
