"""Unit tests for src/validators.py."""

import pytest

from src.validators import validate_numbers


def test_accepts_integers_and_floats():
    """Valid numbers do not raise."""
    validate_numbers(1, 2.5, -3, 0, -0.75)


def test_accepts_no_arguments():
    """Calling with nothing to check is allowed."""
    validate_numbers()


def test_rejects_string():
    """Strings are not numbers."""
    with pytest.raises(TypeError, match="Expected a number, got str"):
        validate_numbers(1, "2")


def test_rejects_none():
    """None is not a number."""
    with pytest.raises(TypeError, match="got NoneType"):
        validate_numbers(None)


def test_rejects_boolean():
    """Booleans are rejected even though bool is a subclass of int."""
    with pytest.raises(TypeError, match="got bool"):
        validate_numbers(True)
