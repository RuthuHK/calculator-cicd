"""Unit tests for the helper functions in src/cli.py."""

import pytest

from src.cli import calculate, format_result, to_number


def test_to_number_converts_whole_floats():
    """5.0 becomes 5, but 2.5 and ints are unchanged."""
    assert to_number(5.0) == 5
    assert isinstance(to_number(5.0), int)
    assert to_number(2.5) == 2.5
    assert to_number(7) == 7


def test_calculate_binary_and_unary():
    """calculate dispatches to the right operation."""
    assert calculate("add", (2.0, 3.0)) == 5
    assert calculate("divide", (7.0, 2.0)) == 3.5
    assert calculate("sqrt", (16.0,)) == 4
    assert calculate("factorial", (5.0,)) == 120


def test_calculate_wrong_number_of_operands():
    """Too many or too few numbers raises ValueError."""
    with pytest.raises(ValueError, match="exactly 2 numbers"):
        calculate("add", (1.0,))
    with pytest.raises(ValueError, match="exactly 1 number"):
        calculate("sqrt", (1.0, 2.0))


def test_calculate_unknown_operation():
    """An unknown operation name raises ValueError."""
    with pytest.raises(ValueError, match="Unknown operation"):
        calculate("cube", (2.0,))


def test_format_result():
    """Whole numbers print without '.0'; long decimals are shortened."""
    assert format_result(5.0) == "5"
    assert format_result(3.5) == "3.5"
    assert format_result(120) == "120"
    assert format_result(2**0.5) == "1.414213562"
