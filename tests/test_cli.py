import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.cli import main


class CliTests(unittest.TestCase):
    def test_convert_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "findings.csv"
            output = Path(tmp) / "report.md"
            source.write_text(
                "title,severity,affected_asset,evidence,impact,recommendation\n"
                "XSS,High,https://example.test,qa@example.com,script execution,encode output\n",
                encoding="utf-8",
            )

            exit_code = main(["convert", str(source), "--out", str(output)])

            self.assertEqual(exit_code, 0)
            report = output.read_text(encoding="utf-8")
            self.assertIn("# Security Assessment Report", report)
            self.assertIn("[REDACTED_EMAIL]", report)

    def test_convert_writes_html_report_from_html_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "findings.csv"
            output = Path(tmp) / "report.html"
            source.write_text(
                "title,severity,affected_asset,evidence,impact,recommendation\n"
                "<script>alert(1)</script>,High,https://example.test,<b>proof</b>,impact,recommendation\n",
                encoding="utf-8",
            )

            exit_code = main(["convert", str(source), "--out", str(output)])

            self.assertEqual(exit_code, 0)
            report = output.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", report)
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", report)
            self.assertIn("&lt;b&gt;proof&lt;/b&gt;", report)
            self.assertNotIn("<script>alert(1)</script>", report)

    def test_convert_writes_html_report_with_explicit_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "findings.csv"
            output = Path(tmp) / "report.out"
            source.write_text(
                "title,severity,affected_asset,evidence,impact,recommendation\n"
                "XSS,High,https://example.test,evidence,impact,recommendation\n",
                encoding="utf-8",
            )

            exit_code = main(["convert", str(source), "--out", str(output), "--format", "html"])

            self.assertEqual(exit_code, 0)
            self.assertIn("<!doctype html>", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
