"""Utilities for formatting timestamps into human-readable relative strings."""
from datetime import datetime
from typing import Optional


def format_relative_time(iso_timestamp: str, now: Optional[datetime] = None) -> str:
    """
    Convert an ISO timestamp into a short relative string like "2 days ago".
    Returns "unknown" if the timestamp is missing or unparseable.
    """
    if not iso_timestamp:
        return "unknown"
    try:
        then = datetime.fromisoformat(iso_timestamp)
    except ValueError:
        return "unknown"

    current = now or datetime.now()
    seconds = (current - then).total_seconds()

    if seconds < 60:
        return "just now"

    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    hours = int(minutes // 60)
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = int(hours // 24)
    return f"{days} day{'s' if days != 1 else ''} ago"
