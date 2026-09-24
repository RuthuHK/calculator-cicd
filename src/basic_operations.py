"""Basic arithmetic: addition, subtraction, multiplication and division."""

from src.validators import validate_numbers


def add(first, second):
    """Return first + second."""
    validate_numbers(first, second)
    return first + second


def subtract(first, second):
    """Return first - second."""
    validate_numbers(first, second)
    return first - second


def multiply(first, second):
    """Return first * second."""
    validate_numbers(first, second)
    return first * second


def divide(dividend, divisor):
    """Return dividend / divisor, refusing to divide by zero."""
    validate_numbers(dividend, divisor)
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return dividend / divisor
