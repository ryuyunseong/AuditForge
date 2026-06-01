import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.parser import load_findings


class ParserTests(unittest.TestCase):
    def test_loads_csv_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.csv"
            path.write_text(
                "title,severity,affected_asset,evidence,impact,recommendation\n"
                "XSS,high,https://example.test,alert,script execution,encode output\n",
                encoding="utf-8",
            )

            findings = load_findings(path)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "High")
        self.assertEqual(findings[0].title, "XSS")

    def test_rejects_csv_missing_required_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.csv"
            path.write_text("title,severity\nXSS,High\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "missing required columns"):
                load_findings(path)

    def test_loads_json_findings_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.json"
            path.write_text(
                json.dumps(
                    {
                        "findings": [
                            {
                                "title": "Weak TLS",
                                "severity": "Medium",
                                "affected_asset": "api.example.test",
                                "evidence": "TLS 1.0 accepted",
                                "impact": "Downgrade risk",
                                "recommendation": "Disable TLS 1.0",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            findings = load_findings(path)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].affected_asset, "api.example.test")

    def test_rejects_unknown_severity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "title": "Unknown",
                            "severity": "urgent",
                            "affected_asset": "example.test",
                            "evidence": "n/a",
                            "impact": "n/a",
                            "recommendation": "n/a",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "unsupported severity"):
                load_findings(path)


if __name__ == "__main__":
    unittest.main()
