"""Helpers for checking and calculating numbers."""


def is_positive_int(value):
    """True for ints greater than zero; bool is not accepted."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def clamp(value, low, high):
    """Limit value to the range low..high."""
    return max(low, min(value, high))


def percent(part, whole):
    """Return a percentage rounded to one decimal, or 0.0 if whole is zero."""
    if whole == 0:
        return 0.0
    return round(part / whole * 100, 1)