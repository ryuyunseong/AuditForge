from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

from auditforge.finding import Finding
from auditforge.parser import load_findings
from auditforge.report import generate_html, generate_markdown


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "convert":
        return _convert(args.input, args.out, args.format)

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auditforge",
        description="Convert security assessment findings into standardized reports.",
    )
    subparsers = parser.add_subparsers(dest="command")

    convert = subparsers.add_parser("convert", help="convert findings to a report")
    convert.add_argument("input", help="path to a CSV or JSON findings file")
    convert.add_argument("--out", "-o", required=True, help="path to write the report")
    convert.add_argument(
        "--format",
        choices=("auto", "markdown", "html"),
        default="auto",
        help="report output format; auto uses the --out extension",
    )

    return parser


def _convert(input_path: str, output_path: str, output_format: str) -> int:
    try:
        findings = load_findings(input_path)
        destination = Path(output_path)
        report = _generate_report(findings, destination, output_format)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"auditforge: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {destination}")
    return 0


def _generate_report(findings: Iterable[Finding], destination: Path, output_format: str) -> str:
    resolved_format = _resolve_format(destination, output_format)
    if resolved_format == "html":
        return generate_html(findings)
    return generate_markdown(findings)


def _resolve_format(destination: Path, output_format: str) -> str:
    if output_format != "auto":
        return output_format
    if destination.suffix.lower() in {".html", ".htm"}:
        return "html"
    return "markdown"
