from datetime import datetime

from src.utils.time_format import format_relative_time


def test_missing_timestamp_returns_unknown():
    assert format_relative_time("") == "unknown"


def test_unparseable_returns_unknown():
    assert format_relative_time("not-a-date") == "unknown"


def test_seconds_ago_is_just_now():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T11:59:30", now=now) == "just now"


def test_minutes_ago_plural():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T11:30:00", now=now) == "30 minutes ago"


def test_hours_ago_plural():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-19T09:00:00", now=now) == "3 hours ago"


def test_days_ago_singular():
    now = datetime(2026, 7, 19, 12, 0, 0)
    assert format_relative_time("2026-07-18T12:00:00", now=now) == "1 day ago"
