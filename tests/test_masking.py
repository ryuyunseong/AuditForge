import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditforge.masking import redact_text


class RedactorTests(unittest.TestCase):
    def test_redacts_email_addresses(self):
        redacted = redact_text("Send report to analyst+audit@example.test and owner@sub.example.test")

        self.assertNotIn("analyst+audit@example.test", redacted)
        self.assertNotIn("owner@sub.example.test", redacted)
        self.assertEqual(redacted.count("[REDACTED_EMAIL]"), 2)

    def test_redacts_phone_numbers(self):
        redacted = redact_text("Contacts: +1-202-555-0198, 010-1234-5678, and (02) 555 0100")

        self.assertNotIn("+1-202-555-0198", redacted)
        self.assertNotIn("010-1234-5678", redacted)
        self.assertNotIn("(02) 555 0100", redacted)
        self.assertEqual(redacted.count("[REDACTED_PHONE]"), 3)

    def test_redacts_korean_resident_registration_number_like_patterns(self):
        redacted = redact_text("Fake identity pattern: 900101-1234567")

        self.assertNotIn("900101-1234567", redacted)
        self.assertIn("[REDACTED_ID]", redacted)

    def test_redacts_bearer_tokens(self):
        redacted = redact_text("Authorization: Bearer fake.header.payload-signature==")

        self.assertNotIn("fake.header.payload-signature", redacted)
        self.assertIn("Bearer [REDACTED_TOKEN]", redacted)

    def test_redacts_api_key_like_values(self):
        cases = {
            "api_key=sample-api-key-123": "api_key=[REDACTED_SECRET]",
            "api-key: sample-api-key-456": "api-key=[REDACTED_SECRET]",
            "access_token='sample-access-token'": "access_token=[REDACTED_SECRET]",
            "client_secret=\"sample-client-secret\"": "client_secret=[REDACTED_SECRET]",
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                redacted = redact_text(text)

                self.assertNotIn("sample-", redacted)
                self.assertIn(expected, redacted)

    def test_redacts_password_like_values(self):
        cases = {
            "password=fake-password": "password=[REDACTED_PASSWORD]",
            "passwd: fake-passphrase": "passwd=[REDACTED_PASSWORD]",
            "pwd='fake-pin'": "pwd=[REDACTED_PASSWORD]",
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                redacted = redact_text(text)

                self.assertNotIn("fake-", redacted)
                self.assertIn(expected, redacted)

    def test_redacts_cookie_values(self):
        redacted = redact_text("Cookie: sessionid=fake-session; csrftoken=fake-csrf; theme=light")

        self.assertNotIn("fake-session", redacted)
        self.assertNotIn("fake-csrf", redacted)
        self.assertIn("Cookie: [REDACTED_COOKIE]", redacted)

    def test_redacts_inline_cookie_values(self):
        redacted = redact_text("Captured headers included sessionid=fake-session and xsrf-token=fake-xsrf.")

        self.assertNotIn("fake-session", redacted)
        self.assertNotIn("fake-xsrf", redacted)
        self.assertIn("sessionid=[REDACTED_COOKIE]", redacted)
        self.assertIn("xsrf-token=[REDACTED_COOKIE]", redacted)

    def test_redacts_mixed_multiline_evidence(self):
        text = "\n".join(
            [
                "Reporter: analyst@example.test",
                "Phone: +1-202-555-0198",
                "ID: 900101-1234567",
                "Authorization: Bearer fake.header.payload",
                "api_key=sample-api-key",
                "password=fake-password",
                "Cookie: sessionid=fake-session; theme=light",
            ]
        )

        redacted = redact_text(text)

        for sensitive_value in (
            "analyst@example.test",
            "+1-202-555-0198",
            "900101-1234567",
            "fake.header.payload",
            "sample-api-key",
            "fake-password",
            "fake-session",
        ):
            with self.subTest(sensitive_value=sensitive_value):
                self.assertNotIn(sensitive_value, redacted)

        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_ID]", redacted)
        self.assertIn("Bearer [REDACTED_TOKEN]", redacted)
        self.assertIn("api_key=[REDACTED_SECRET]", redacted)
        self.assertIn("password=[REDACTED_PASSWORD]", redacted)
        self.assertIn("Cookie: [REDACTED_COOKIE]", redacted)


if __name__ == "__main__":
    unittest.main()
