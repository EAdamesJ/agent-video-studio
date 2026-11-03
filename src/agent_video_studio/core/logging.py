from __future__ import annotations

import logging
import re

_SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|authorization)"
    r"(\s*[:=]\s*|\s+)([^\s,;]+)"
)


class SecretRedactionFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            rendered = record.getMessage()
            record.msg = _SECRET_PATTERN.sub(r"\1\2[REDACTED]", rendered)
            record.args = ()
        except Exception:
            record.msg = "[log message redacted after formatting error]"
            record.args = ()
        return True


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    for handler in logging.getLogger().handlers:
        handler.addFilter(SecretRedactionFilter())
