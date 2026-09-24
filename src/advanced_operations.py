"""Advanced arithmetic: power, square root, modulus, percentage and factorial."""

import math

from src.validators import validate_numbers


def power(base, exponent):
    """Return base raised to exponent."""
    validate_numbers(base, exponent)
    if base == 0 and exponent < 0:
        raise ValueError("Cannot raise zero to a negative power")
    if base < 0 and not float(exponent).is_integer():
        raise ValueError("Negative base needs a whole-number exponent")
    return base**exponent


def square_root(number):
    """Return the square root of a non-negative number."""
    validate_numbers(number)
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(number)


def modulus(dividend, divisor):
    """Return the remainder of dividend / divisor."""
    validate_numbers(dividend, divisor)
    if divisor == 0:
        raise ValueError("Cannot take modulus by zero")
    return dividend % divisor


def percentage(value, percent):
    """Return percent % of value, e.g. percentage(200, 15) == 30."""
    validate_numbers(value, percent)
    return value * percent / 100


def factorial(number):
    """Return number! for a non-negative whole number."""
    validate_numbers(number)
    if not float(number).is_integer():
        raise ValueError("Factorial needs a whole number")
    if number < 0:
        raise ValueError("Cannot calculate factorial of a negative number")
    return math.factorial(int(number))
