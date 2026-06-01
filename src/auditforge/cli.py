from __future__ import annotations

import argparse
import sys
from pathlib import Path

from auditforge.parser import load_findings
from auditforge.report import generate_markdown


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "convert":
        return _convert(args.input, args.out)

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auditforge",
        description="Convert security assessment findings into standardized reports.",
    )
    subparsers = parser.add_subparsers(dest="command")

    convert = subparsers.add_parser("convert", help="convert findings to a Markdown report")
    convert.add_argument("input", help="path to a CSV or JSON findings file")
    convert.add_argument("--out", "-o", required=True, help="path to write the Markdown report")

    return parser


def _convert(input_path: str, output_path: str) -> int:
    try:
        findings = load_findings(input_path)
        report = generate_markdown(findings)
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"auditforge: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {destination}")
    return 0
