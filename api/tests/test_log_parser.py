from datetime import datetime

import pytest

from services.log_parser import LogParser
from models.severity import Severity


@pytest.fixture
def fake_logs():
    return [
        ("This is an info message", Severity.INFO),
        ("This is a warning message", Severity.WARNING),
        ("This is a warn message", Severity.WARNING),
        ("This is an error message", Severity.ERROR),
        ("This is a critical message", Severity.CRITICAL),
        ("This is a fatal error message", Severity.CRITICAL),
        ("This is a panic message", Severity.CRITICAL),
        ("This is an exception message", Severity.ERROR),
        ("This is a traceback message", Severity.ERROR),
        ("This is a random message with no keywords", Severity.INFO)
    ]


def test_severity_parsing(fake_logs):

    for log_line, expected_severity in fake_logs:
        parser = LogParser(log_line)
        assert parser.severity(
        ) == expected_severity, f"Expected {expected_severity} \
            for log line: '{log_line}', but got {parser.severity()}"


def test_is_error(fake_logs):
    for log_line, expected_severity in fake_logs:
        parser = LogParser(log_line)
        is_error = parser.is_error()
        expected_is_error = expected_severity >= Severity.ERROR
        assert is_error == expected_is_error, f"Expected is_error \
              to be {expected_is_error} for log line: '{log_line}', \
                but got {is_error}"


def test_timestamp_extraction():
    cases = [
        ("2026-01-15 10:23:45 ERROR Failed to connect",
         datetime(2026, 1, 15, 10, 23, 45)),
        ("2026-01-15T10:23:45 ERROR Failed to connect",
         datetime(2026, 1, 15, 10, 23, 45)),
        ("ERROR Failed to connect",   # sem timestamp
         None),
    ]

    for line, expected_timestamp in cases:
        parser = LogParser(line)
        assert parser.timestamp == expected_timestamp, f"Expected \
            timestamp {expected_timestamp} for log line: '{line}', \
                but got {parser.timestamp}"


def test_detect_format():
    assert LogParser('{"level":"error","message":"db down"}').format == "json"
    assert LogParser(
        "2026-01-15 10:25:01.512 | ERROR    |\
              app.db:connect:88 - Falha").format == "loguru"
    assert LogParser(
        "2026-01-15T10:23:45.123Z [error]: \
            Falha ao conectar").format == "winston"
    assert LogParser(
        "2026-01-15 10:23:45 ERROR Falha ao conectar").format == "plaintext"
