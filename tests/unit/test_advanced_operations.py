"""Unit tests for src/advanced_operations.py."""

import pytest

from src.advanced_operations import (
    factorial,
    modulus,
    percentage,
    power,
    square_root,
)


def test_power_positive_numbers():
    """Power with positive numbers."""
    assert power(2, 3) == 8
    assert power(5, 2) == 25


def test_power_zero_and_negative_exponent():
    """Zero exponent gives 1; negative exponent gives a fraction."""
    assert power(5, 0) == 1
    assert power(0, 0) == 1
    assert power(2, -1) == 0.5


def test_power_negative_base():
    """Negative base with a whole-number exponent."""
    assert power(-2, 3) == -8
    assert power(-2, 2) == 4


def test_power_invalid_cases():
    """Zero to a negative power, and negative base with fractional power."""
    with pytest.raises(ValueError, match="zero to a negative power"):
        power(0, -1)
    with pytest.raises(ValueError, match="whole-number exponent"):
        power(-8, 0.5)


def test_square_root_positive_numbers():
    """Square root of perfect squares and non-perfect squares."""
    assert square_root(4) == 2
    assert square_root(9) == 3
    assert square_root(0) == 0
    assert square_root(2) == pytest.approx(1.41421356)


def test_square_root_negative_raises():
    """Square root of a negative number raises ValueError."""
    with pytest.raises(ValueError, match="square root of a negative"):
        square_root(-4)


def test_modulus():
    """Remainder calculations, including Python's sign rules."""
    assert modulus(10, 3) == 1
    assert modulus(9, 3) == 0
    assert modulus(-7, 3) == 2


def test_modulus_by_zero_raises():
    """Modulus by zero raises ValueError."""
    with pytest.raises(ValueError, match="modulus by zero"):
        modulus(10, 0)


def test_percentage():
    """Percentage of a value."""
    assert percentage(200, 15) == 30
    assert percentage(50, 100) == 50
    assert percentage(80, 0) == 0
    assert percentage(-40, 25) == -10


def test_factorial():
    """Factorial of whole numbers, including 0! == 1."""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(5.0) == 120


def test_factorial_invalid_cases():
    """Negative or fractional factorials raise ValueError."""
    with pytest.raises(ValueError, match="negative number"):
        factorial(-3)
    with pytest.raises(ValueError, match="whole number"):
        factorial(2.5)


@pytest.mark.parametrize("operation", [power, modulus, percentage])
def test_two_argument_operations_reject_text(operation):
    """Two-argument operations reject non-numeric input."""
    with pytest.raises(TypeError):
        operation("2", 3)


@pytest.mark.parametrize("operation", [square_root, factorial])
def test_one_argument_operations_reject_text(operation):
    """One-argument operations reject non-numeric input."""
    with pytest.raises(TypeError):
        operation("9")
