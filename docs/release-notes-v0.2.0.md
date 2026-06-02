# AuditForge v0.2.0 Release Notes

This release improves AuditForge report output, examples, and documentation while keeping the project focused on user-provided assessment results.

## Highlights

- Improved redaction test coverage for common sensitive value patterns.
- Added a fake sample web assessment input file and generated Markdown report.
- Added HTML report output with escaped finding content.
- Added a generated fake sample HTML report.
- Added Korean and English report wording examples for template planning.

## Changes

### Redaction Coverage

The test suite now covers emails, phone numbers, Korean resident registration number-like patterns, Bearer tokens, API key-like values, password-like values, cookie values, and mixed multiline evidence.

### Web Assessment Sample

The `examples/sample_web_findings.csv` file provides a fake web assessment input with common finding types:

- SQL Injection
- Cross-Site Scripting
- Missing Security Headers
- Directory Listing
- Weak TLS Configuration

Generated sample reports are available as Markdown and HTML:

- `examples/sample_web_report.md`
- `examples/sample_web_report.html`

### HTML Report Output

AuditForge can generate HTML reports when the output path ends in `.html` or `.htm`, or when `--format html` is passed explicitly.

HTML output escapes redacted finding content so generated reports do not render user-provided evidence as active HTML.

### Korean and English Wording Examples

The `docs/report-template-examples.md` file provides fake English and Korean wording examples for:

- Finding titles
- Evidence wording
- Impact statements
- Recommendation text

These examples are documentation only. AuditForge does not include a full template engine in this release.

## Security Notes

AuditForge does not perform scanning, exploitation, probing, or unauthorized testing.

AuditForge only processes user-provided assessment results.

Do not include real customer data, confidential evidence, credentials, tokens, cookies, personal information, real IP addresses, or private URLs in public examples, issues, pull requests, or discussions.

## Validation

Run these commands before publishing the release:

```bash
python -m unittest discover -s tests
python -m compileall src tests
```

On Windows PowerShell, regenerate the sample HTML report with:

```powershell
$env:PYTHONPATH='src'
python -m auditforge convert examples\sample_web_findings.csv --out examples\sample_web_report.html
```

## Follow-Up Work

The following larger work items remain outside this release:

- Burp Suite export import support
- Configurable report templates
- Web and infrastructure rule packs
- DOCX export research
