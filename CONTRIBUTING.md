# Contributing

Thank you for considering a contribution to AuditForge.

## Development Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m compileall src tests
```

## Guidelines

- Keep changes small and focused.
- Use fake sample data only.
- Do not commit secrets, customer data, private URLs, or sensitive logs.
- Add or update tests for behavior changes.
- Keep user-facing errors understandable without exposing internals or sensitive values.

## Pull Requests

Pull requests should describe:

- The problem being solved
- The main changes
- Test results
- Any security or compatibility risks

Keep pull requests focused on one behavior change when practical. Avoid broad formatting-only changes mixed with feature work.

## Good First Issues

Good first contributions usually improve documentation, add tests for existing behavior, or add small report template refinements.

Good first issues should:

- Use fake data only
- Avoid new dependencies unless clearly justified
- Avoid network scanning, exploitation, or live target interaction
- Include a simple expected behavior description

## Issue Triage

When filing an issue, choose the closest template and include a minimal example using fake input. If the issue involves redaction, include only synthetic values that match the pattern being discussed.
