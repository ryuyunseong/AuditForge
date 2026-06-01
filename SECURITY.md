# Security Policy

## Supported Versions

AuditForge is currently pre-1.0. Security fixes are applied to the latest released version.

## Reporting a Vulnerability

Please report security issues through a private channel when available. Do not open public issues containing secrets, customer data, exploit payloads against real systems, logs with credentials, or private infrastructure details.

When reporting an issue, include:

- A clear description of the risk
- Steps to reproduce with fake or sanitized data
- Affected versions or commits
- Suggested remediation, if known

Use fake or fully sanitized examples. If a report requires sensitive evidence to explain impact, describe the pattern instead of sharing the original value.

## Scope

AuditForge is a report generation and redaction helper for user-provided assessment results. It is not a scanning or exploitation framework.

In scope:

- Redaction bypasses that can expose sensitive values in generated reports
- Parser behavior that mishandles user-provided finding files
- Report generation bugs that can leak unexpected content

Out of scope:

- Requests to scan, test, or exploit third-party systems
- Findings that require real customer data to reproduce publicly
- Vulnerabilities in unrelated tools used to create input files
