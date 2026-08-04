
from services.log_entry_collector import LogEntryCollector


def test_collect_logs():
    logs = [
        "2026-01-15 10:23:45 ERROR Falha ao conectar",
        "2026-01-15T10:23:45.123Z [error]: Falha ao conectar",
        "2026-01-15 10:25:01.512 | ERROR    | app.db:connect:88 - Falha",
        '{"level":"error","message":"db down"}'
    ]
    collector = LogEntryCollector(logs)
    entries = collector.parse_lines()

    assert len(entries) == 4
    for entry in entries:
        assert "log_line" in entry
        assert "severity" in entry
        assert "is_error" in entry
        assert "timestamp" in entry
        assert "format" in entry


def test_continuation_detection():
    lines = [
        "2026-01-15 10:27:00 ERROR Unhandled exception while processing order",
        "Traceback (most recent call last):",
        '  File "/app/worker.py", line 42, in process',
        "    raise ValueError('invalid order id 998')",
        "ValueError: invalid order id 998",
    ]

    entries = LogEntryCollector(lines).parse_lines()
    assert len(entries) == 1

    assert entries[0]["message"] == (
        "2026-01-15 10:27:00 ERROR Unhandled "
        "exception while processing order")
    assert "Traceback" in entries[0]["log_line"]
    assert "ValueError: invalid order id 998" in entries[0]["log_line"]
