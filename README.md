# AuditForge

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

AuditForge is a small open-source CLI that converts security assessment findings into standardized Markdown and HTML report drafts.

It is designed for user-provided assessment results, not for unauthorized scanning. The tool normalizes finding records, groups findings by severity, redacts common sensitive values, and writes a report that can be reviewed before delivery.

## Who Should Use It

AuditForge is intended for security consultants, internal security teams, and application owners who already have assessment findings and want a repeatable way to turn them into consistent report drafts.

It does not scan targets, discover assets, exploit vulnerabilities, or verify findings against live systems.

## Features

- CSV and JSON findings input
- Severity normalization for Critical, High, Medium, Low, and Info
- Markdown and HTML report generation grouped by severity
- Redaction for emails, phone numbers, Korean resident registration number patterns, bearer tokens, API keys, password-like values, and cookie values
- Fake sample input and output files for quick testing

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
auditforge convert examples/sample_findings.csv --out examples/sample_report.md
```

HTML output is selected automatically when `--out` ends in `.html`:

```bash
auditforge convert examples/sample_web_findings.csv --out examples/sample_web_report.html
```

You can also set the output format explicitly:

```bash
auditforge convert examples/sample_web_findings.csv --out report.out --format html
```

Without installing the console script, run it with `PYTHONPATH`:

```bash
PYTHONPATH=src python -m auditforge convert examples/sample_findings.csv --out examples/sample_report.md
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m auditforge convert examples/sample_findings.csv --out examples/sample_report.md
```

## Input Format

CSV and JSON inputs must provide these fields:

| Field | Description |
| --- | --- |
| `title` | Finding title |
| `severity` | Critical, High, Medium, Low, or Info |
| `affected_asset` | Host, URL, application, or system affected by the finding |
| `evidence` | Assessment evidence to include in the draft report |
| `impact` | Business or technical impact |
| `recommendation` | Remediation guidance |

JSON input can be either a list of finding objects or an object with a `findings` list.

## Output

AuditForge writes Markdown or HTML reports with:

- A severity summary table
- Findings grouped in Critical, High, Medium, Low, and Info order
- Redacted evidence blocks
- Impact and recommendation sections for each finding

HTML output escapes finding content after redaction so generated reports do not render user-provided evidence as active HTML.

## Examples

Sample files are provided in `examples/`:

- `examples/sample_findings.csv`
- `examples/sample_findings.json`
- `examples/sample_report.md`
- `examples/sample_web_findings.csv`
- `examples/sample_web_report.md`
- `examples/sample_web_report.html`
- `docs/report-template-examples.md`

The samples use fake domains and fake data only.

To generate the web assessment sample report:

```bash
auditforge convert examples/sample_web_findings.csv --out examples/sample_web_report.md
auditforge convert examples/sample_web_findings.csv --out examples/sample_web_report.html
```

The web assessment sample includes common finding types such as SQL injection, cross-site scripting, missing security headers, directory listing, and weak TLS configuration.

For wording examples, see `docs/report-template-examples.md`. It includes fake English and Korean examples for finding titles, evidence, impact, and recommendations.

The draft v0.2.0 release notes are available in `docs/release-notes-v0.2.0.md`.

## Security Notes

- Review generated reports before sharing them.
- Do not include real customer data in examples, tests, issues, or pull requests.
- Do not paste private URLs, credentials, cookies, tokens, exploit output, or customer evidence into public GitHub issues.
- Redaction is best-effort and should not replace human review.
- AuditForge processes user-provided assessment results only. It does not perform scanning, exploitation, or target discovery.

## Public Release Checklist

Before publishing a release:

- Run the test suite locally.
- Confirm sample files contain fake data only.
- Review generated reports for accidental sensitive data.
- Update `CHANGELOG.md`.
- Create a signed or annotated Git tag for the release version.

## Development

Run the test suite:

```bash
python -m unittest discover -s tests
```

Run a basic syntax check:

```bash
python -m compileall src tests
```

## Roadmap

- Configurable report templates
- Burp export parsing
- Rule packs for common web and infrastructure findings
- Local web UI
- DOCX output
