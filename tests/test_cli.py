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


if __name__ == "__main__":
    unittest.main()
