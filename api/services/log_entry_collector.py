import re

from services.log_parser import LogParser

CONTINUATION_RE = re.compile(
    r"^(\s+"                                      # indentação
    r"|Traceback \(most recent call last\):"      # início de traceback
    r"|File \""                                   # linha de frame
    r"|Caused by:"                                # traceback encadeado (Java)
    # linha final: NomeException: msg
    r"|\w+(Error|Exception):)"
)


class LogEntryCollector:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def is_continuation(self, line: str) -> bool:
        return bool(CONTINUATION_RE.match(line))

    def parse_lines(self) -> list[dict]:
        entries = []
        current_entry = None

        for line in self._lines:
            if current_entry is not None and self.is_continuation(line):
                current_entry["log_line"] += "\n" + line
                continue

            parser = LogParser(line)
            entry = {
                "message": line,
                "log_line": line,
                "severity": parser.severity(),
                "is_error": parser.is_error(),
                "timestamp": parser.timestamp,
                "format": parser.format
            }

            if current_entry is not None:
                entries.append(current_entry)

            current_entry = entry

        if current_entry is not None:
            entries.append(current_entry)

        return entries
