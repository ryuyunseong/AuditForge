import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.finding import Finding
from auditforge.report import generate_html, generate_markdown


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


class HtmlReportTests(unittest.TestCase):
    def test_generates_grouped_html_with_redaction(self):
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

        report = generate_html(findings)

        self.assertIn("<!doctype html>", report)
        self.assertIn("<td>Critical</td><td>1</td>", report)
        self.assertIn("<td>Medium</td><td>1</td>", report)
        self.assertLess(report.index('<section id="critical">'), report.index('<section id="medium">'))
        self.assertIn("Bearer [REDACTED_TOKEN]", report)
        self.assertIn("[REDACTED_EMAIL]", report)
        self.assertNotIn("qa@example.com", report)

    def test_html_escapes_finding_fields(self):
        finding = Finding(
            title="<script>alert('title')</script>",
            severity="High",
            affected_asset='https://example.test/?q=<asset>&mode="test"',
            evidence="<img src=x onerror=alert(1)> api_key=sample-api-key",
            impact="Impact includes <b>markup</b> & details.",
            recommendation='Escape "quotes" and <tags>.',
        )

        report = generate_html([finding])

        self.assertNotIn("<script>alert", report)
        self.assertNotIn("<img src=x", report)
        self.assertNotIn("<b>markup</b>", report)
        self.assertNotIn("sample-api-key", report)
        self.assertIn("&lt;script&gt;alert(&#x27;title&#x27;)&lt;/script&gt;", report)
        self.assertIn("q=&lt;asset&gt;&amp;mode=&quot;test&quot;", report)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt; api_key=[REDACTED_SECRET]", report)
        self.assertIn("Impact includes &lt;b&gt;markup&lt;/b&gt; &amp; details.", report)
        self.assertIn("Escape &quot;quotes&quot; and &lt;tags&gt;.", report)


if __name__ == "__main__":
    unittest.main()
