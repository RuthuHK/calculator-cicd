"""Shared input-validation helpers used by every calculator module."""


def validate_numbers(*values):
    """Raise TypeError unless every value is an int or a float.

    Booleans are rejected even though Python treats them as integers.
    """
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Expected a number, got {type(value).__name__}")
