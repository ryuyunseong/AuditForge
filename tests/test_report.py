import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.finding import Finding
from auditforge.report import generate_markdown


class MarkdownReportTests(unittest.TestCase):
    def test_generates_grouped_markdown_with_redaction(self):
        findings = [
            Finding(
                title="Weak TLS",
                severity="Medium",
                affected_asset="api.example.test",
                evidence="TLS 1.0 accepted by qa@example.com",
                impact="Downgrade risk",
                recommendation="Disable TLS 1.0",
            ),
            Finding(
                title="SQL Injection",
                severity="Critical",
                affected_asset="https://app.example.test/login",
                evidence="Authorization: Bearer fake.token",
                impact="Authentication bypass",
                recommendation="Use parameterized queries",
            ),
        ]

        report = generate_markdown(findings)

        self.assertIn("| Critical | 1 |", report)
        self.assertIn("| Medium | 1 |", report)
        self.assertLess(report.index("## Critical"), report.index("## Medium"))
        self.assertIn("Bearer [REDACTED_TOKEN]", report)
        self.assertIn("[REDACTED_EMAIL]", report)
        self.assertNotIn("qa@example.com", report)


if __name__ == "__main__":
    unittest.main()
