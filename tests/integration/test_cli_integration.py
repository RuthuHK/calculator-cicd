"""Integration tests: run the real CLI in-process with Click's CliRunner.

These check that the CLI, the basic operations and the advanced operations
all work together end to end.
"""

import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture(name="runner")
def fixture_runner():
    """A Click test runner that invokes the CLI in the same process."""
    return CliRunner()


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["add", "2", "3"], "5"),
        (["subtract", "10", "4"], "6"),
        (["multiply", "3", "4"], "12"),
        (["divide", "7", "2"], "3.5"),
        (["power", "2", "10"], "1024"),
        (["mod", "10", "3"], "1"),
        (["percent", "200", "15"], "30"),
        (["sqrt", "16"], "4"),
        (["factorial", "5"], "120"),
    ],
)
def test_every_operation_end_to_end(runner, arguments, expected):
    """Each operation prints the right answer and exits with code 0."""
    result = runner.invoke(cli, arguments)
    assert result.exit_code == 0
    assert result.output.strip() == expected


def test_negative_numbers_with_separator(runner):
    """Negative numbers work when placed after --."""
    result = runner.invoke(cli, ["add", "--", "-3", "5"])
    assert result.exit_code == 0
    assert result.output.strip() == "2"


def test_divide_by_zero_shows_error(runner):
    """Errors from the operations are shown cleanly with exit code 1."""
    result = runner.invoke(cli, ["divide", "5", "0"])
    assert result.exit_code == 1
    assert "Cannot divide by zero" in result.output


def test_wrong_number_of_arguments_shows_error(runner):
    """Passing the wrong count of numbers is reported to the user."""
    result = runner.invoke(cli, ["sqrt", "4", "9"])
    assert result.exit_code == 1
    assert "exactly 1 number" in result.output


def test_unknown_operation_is_rejected(runner):
    """Click rejects operations that are not in the list (exit code 2)."""
    result = runner.invoke(cli, ["cube", "3"])
    assert result.exit_code == 2


def test_non_numeric_input_is_rejected(runner):
    """Click rejects text where a number is expected (exit code 2)."""
    result = runner.invoke(cli, ["add", "two", "3"])
    assert result.exit_code == 2


def test_help_lists_usage(runner):
    """--help prints usage information."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "OPERATION" in result.output
