"""Unit tests for src/basic_operations.py."""

import pytest

from src.basic_operations import add, divide, multiply, subtract


def test_add_positive_numbers():
    """Adding positive numbers."""
    assert add(2, 3) == 5
    assert add(10, 15) == 25


def test_add_negative_numbers():
    """Adding negative numbers."""
    assert add(-1, -1) == -2
    assert add(-5, 3) == -2


def test_add_zero_and_floats():
    """Adding zero and decimals."""
    assert add(0, 0) == 0
    assert add(7, 0) == 7
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract_numbers():
    """Subtracting positive, negative and zero values."""
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(-5, -3) == -2
    assert subtract(4, 0) == 4


def test_multiply_numbers():
    """Multiplying positive, negative and zero values."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(-4, -5) == 20
    assert multiply(5, 0) == 0
    assert multiply(2.5, 2) == 5.0


def test_divide_numbers():
    """Dividing positive, negative and fractional results."""
    assert divide(10, 2) == 5
    assert divide(-12, -3) == 4
    assert divide(-10, 2) == -5
    assert divide(7, 2) == 3.5


def test_divide_zero_numerator():
    """Zero divided by a number is zero."""
    assert divide(0, 5) == 0


def test_divide_by_zero_raises():
    """Dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


@pytest.mark.parametrize("operation", [add, subtract, multiply, divide])
def test_invalid_input_raises(operation):
    """Every basic operation rejects non-numeric input."""
    with pytest.raises(TypeError):
        operation("5", 3)
    with pytest.raises(TypeError):
        operation(5, None)
