---
name: Bug report
about: Report a reproducible AuditForge problem using fake or sanitized data.
title: "Bug: "
labels: bug
assignees: ""
---

## Summary

Describe the bug clearly.

## Steps to Reproduce

1. Run:

   ```bash
   auditforge convert examples/sample_findings.csv --out report.md
   ```

2. Observe:

## Expected Behavior

Describe what should happen.

## Actual Behavior

Describe what happened instead.

## Sample Input

Use fake or sanitized data only.

```csv
title,severity,affected_asset,evidence,impact,recommendation
Example,Low,https://example.test,Fake evidence,Fake impact,Fake recommendation
```

## Environment

- AuditForge version or commit:
- Python version:
- Operating system:

## Security and Privacy Check

- [ ] I removed customer data, credentials, cookies, tokens, private URLs, and sensitive logs.
- [ ] This report does not request scanning, exploitation, or testing of a system I do not own or manage.
