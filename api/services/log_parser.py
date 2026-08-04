
import datetime
import re

from models.severity import Severity

# severity keywords for log parsing, ordered from highest to lowest severity
SEVERITY_KEYWORDS: list[tuple[Severity, tuple[str, ...]]] = [
    (Severity.CRITICAL, ("critical", "fatal", "panic")),
    (Severity.ERROR, ("error", "exception", "traceback")),
    (Severity.WARNING, ("warning", "warn")),
    (Severity.INFO, ("info",))
]

TIMESTAMP_REGEX = re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})")


class LogParser:
    def __init__(self, log_line: str):
        self.log_line = log_line
        self.format = self._detect_format()

    def severity(self) -> Severity:
        # inference of severity based on keywords in the log line
        # from highest to lowest severity
        # if no keywords are found, default to INFO

        line = self.log_line.lower()
        for severity, keywords in SEVERITY_KEYWORDS:
            if any(keyword in line for keyword in keywords):
                return severity
        return Severity.INFO

    def is_error(self) -> bool:
        return self.severity() >= Severity.ERROR

    @property
    def timestamp(self) -> datetime:
        # extract timestamp from log line if present
        # return None if no timestamp is found

        match = TIMESTAMP_REGEX.search(self.log_line)
        if match:

            raw_timestamp = match.group('ts')

            if "T" in raw_timestamp:
                raw_timestamp = raw_timestamp.replace("T", " ")

            return datetime.datetime.strptime(raw_timestamp,
                                              "%Y-%m-%d %H:%M:%S")
        return None

    def _detect_format(self) -> str:
        # determine the log format based on the log line
        # return 'plaintext' if no known format is detected

        if self.log_line.startswith("{") and self.log_line.endswith("}"):
            return "json"
        if " | " in self.log_line and \
                re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+",
                          self.log_line):
            return "loguru"
        if re.search(r"\[(info|warn|error|debug)\]:", self.log_line,
                     re.IGNORECASE):
            return "winston"
        else:
            return "plaintext"

    def _parse_json(self) -> dict:
        import json
        try:
            data = json.loads(self.log_line)
            level = data.get("level", "").lower(
            ) or data.get("severity", "").lower()
            message = data.get("message", "")
            timestamp = data.get("timestamp", "") or data.get(
                "time", "") or None
            return {
                "level": level,
                "message": message,
                "timestamp": timestamp
            }
        except json.JSONDecodeError as e:

            return {"log": self.log_line,
                    "error": f"Error parsing JSON log line: {e}"}

    def _parse_loguru(self) -> dict:
        # loguru format:
        # "2026-01-15 10:25:01.512 | ERROR
        # | app.db:connect:88 - Falha ao conectar"
        parts = self.log_line.split("|")
        if len(parts) < 3:
            return {"log": self.log_line,
                    "error": "Error parsing loguru log line: not enough parts"}
        timestamp = parts[0].strip()
        level = parts[1].strip().lower()
        message = "|".join(parts[2:]).strip()
        return {
            "level": level,
            "message": message,
            "timestamp": timestamp
        }

    def _parse_winston(self) -> dict:
        # winston format: "2026-01-15T10:23:45.123Z [error]: Falha ao conectar"

        regex_raw = r"(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z) "
        regex_raw += r"\[(?P<level>info|warn|error|debug)\]: (?P<message>.+)"
        regex = re.compile(regex_raw)
        match = re.match(regex,
                         self.log_line, re.IGNORECASE)
        if not match:
            return {"log": self.log_line,
                    "error": "Error parsing winston log line: \
                        regex did not match"}
        return {
            "level": match.group("level").lower(),
            "message": match.group("message"),
            "timestamp": match.group("ts")
        }

    def _parse_plaintext(self) -> dict:
        # plaintext format: "2026-01-15 10:23:45 ERROR Falha ao conectar"
        parts = self.log_line.split(" ", 3)
        if len(parts) < 4:
            return {"log": self.log_line,
                    "error": "Error parsing plaintext log line: \
                        not enough parts"}
        timestamp = f"{parts[0]} {parts[1]}"
        level = parts[2].lower()
        message = parts[3]
        return {
            "level": level,
            "message": message,
            "timestamp": timestamp
        }
