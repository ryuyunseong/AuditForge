import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.masking import redact_text


class RedactorTests(unittest.TestCase):
    def test_redacts_common_sensitive_values(self):
        text = "\n".join(
            [
                "tester@example.com",
                "+1-202-555-0198",
                "900101-1234567",
                "Authorization: Bearer abc.def.ghi",
                "api_key=sk_test_123",
                "password=hunter2",
                "Cookie: sessionid=fake-session; theme=light",
            ]
        )

        redacted = redact_text(text)

        self.assertNotIn("tester@example.com", redacted)
        self.assertNotIn("+1-202-555-0198", redacted)
        self.assertNotIn("900101-1234567", redacted)
        self.assertNotIn("abc.def.ghi", redacted)
        self.assertNotIn("sk_test_123", redacted)
        self.assertNotIn("hunter2", redacted)
        self.assertNotIn("fake-session", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_ID]", redacted)
        self.assertIn("Bearer [REDACTED_TOKEN]", redacted)
        self.assertIn("api_key=[REDACTED_SECRET]", redacted)
        self.assertIn("password=[REDACTED_PASSWORD]", redacted)
        self.assertIn("Cookie: [REDACTED_COOKIE]", redacted)


if __name__ == "__main__":
    unittest.main()
