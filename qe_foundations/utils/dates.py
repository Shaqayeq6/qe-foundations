"""Helpers for working with dates and timestamps."""

from datetime import datetime, timedelta


def add_days(day, days):
    """Return the date the given number of days after day."""
    return day + timedelta(days=days)


def is_weekend(day):
    """True when the date falls on Saturday or Sunday."""
    return day.weekday() >= 5


def timestamp_for_filename(moment=None):
    """Return a timestamp suitable for file and folder names."""
    moment = moment or datetime.now()
    return moment.strftime("%Y%m%d_%H%M%S")