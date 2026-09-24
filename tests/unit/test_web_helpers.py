"""Unit tests for the helper functions in src/web_app.py."""

import pytest

from src.cli import ALL_OPERATIONS
from src.web_app import OPERATION_LABELS, compute, parse_number


def test_every_operation_has_a_gui_label():
    """The dropdown must offer exactly the operations the calculator supports."""
    assert sorted(OPERATION_LABELS) == ALL_OPERATIONS


def test_parse_number_accepts_numbers_and_numeric_text():
    """Numbers and numeric strings are converted to floats."""
    assert parse_number("2", "x") == 2.0
    assert parse_number("-3.5", "x") == -3.5
    assert parse_number(7, "x") == 7.0


@pytest.mark.parametrize("bad_value", ["", "abc", None, "1,5"])
def test_parse_number_rejects_non_numbers(bad_value):
    """Empty, text and missing values raise a friendly ValueError."""
    with pytest.raises(ValueError, match="First number must be a number"):
        parse_number(bad_value, "First number")


@pytest.mark.parametrize("bad_value", ["inf", "-inf", "nan"])
def test_parse_number_rejects_infinity_and_nan(bad_value):
    """Infinity and NaN are not accepted."""
    with pytest.raises(ValueError, match="finite number"):
        parse_number(bad_value, "x")


def test_compute_two_number_operations():
    """Two-number operations use both values and return formatted text."""
    assert compute("add", "2", "3") == "5"
    assert compute("divide", "7", "2") == "3.5"
    assert compute("percent", "200", "15") == "30"


def test_compute_one_number_operations_ignore_second_value():
    """sqrt and factorial ignore the second (possibly empty) value."""
    assert compute("sqrt", "16", "") == "4"
    assert compute("factorial", "5") == "120"


def test_compute_errors():
    """Unknown operations and maths errors raise ValueError."""
    with pytest.raises(ValueError, match="Unknown operation"):
        compute("cube", "2", "3")
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        compute("divide", "5", "0")
    with pytest.raises(ValueError, match="Second number must be a number"):
        compute("add", "5", "")
