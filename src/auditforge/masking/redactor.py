from __future__ import annotations

import re


_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)\d{3,4}[-.\s]?\d{4}(?!\w)")
_KOREAN_RRN_RE = re.compile(r"\b\d{6}-[1-4]\d{6}\b")
_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/\-]+=*")
_COOKIE_HEADER_RE = re.compile(r"(?im)^(cookie|set-cookie)\s*:\s*[^\r\n]+")
_COOKIE_VALUE_RE = re.compile(r"(?i)\b(sessionid|sid|jsessionid|phpsessid|connect\.sid|csrftoken|xsrf-token)\s*=\s*[^;\s]+")
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)(?<![\w-])(api[_-]?key|access[_-]?token|secret[_-]?key|client[_-]?secret|token)\s*[:=]\s*[\"']?[^\"'\s,;]+[\"']?"
)
_PASSWORD_ASSIGNMENT_RE = re.compile(r"(?i)(?<![\w-])(password|passwd|pwd)\s*[:=]\s*[\"']?[^\"'\s,;]+[\"']?")


def redact_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = _EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = _KOREAN_RRN_RE.sub("[REDACTED_ID]", text)
    text = _PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = _BEARER_RE.sub("Bearer [REDACTED_TOKEN]", text)
    text = _COOKIE_HEADER_RE.sub(_redact_cookie_header, text)
    text = _COOKIE_VALUE_RE.sub(lambda match: f"{match.group(1)}=[REDACTED_COOKIE]", text)
    text = _SECRET_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}=[REDACTED_SECRET]", text)
    text = _PASSWORD_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}=[REDACTED_PASSWORD]", text)
    return text


def _redact_cookie_header(match: re.Match[str]) -> str:
    return f"{match.group(1)}: [REDACTED_COOKIE]"
