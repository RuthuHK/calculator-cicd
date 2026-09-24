"""Command-line interface for the calculator, built with Click.

Usage examples (run from the project root):
    python -m src.cli add 2 3
    python -m src.cli sqrt 16
    python -m src.cli subtract -- -3 5     (use -- before negative numbers)
"""

import click

from src.advanced_operations import (
    factorial,
    modulus,
    percentage,
    power,
    square_root,
)
from src.basic_operations import add, divide, multiply, subtract

BINARY_OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "mod": modulus,
    "percent": percentage,
}

UNARY_OPERATIONS = {
    "sqrt": square_root,
    "factorial": factorial,
}

ALL_OPERATIONS = sorted([*BINARY_OPERATIONS, *UNARY_OPERATIONS])


def to_number(value):
    """Turn whole-number floats such as 5.0 into ints so results print cleanly."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def calculate(operation, operands):
    """Run the named operation on a sequence of numbers and return the result."""
    numbers = [to_number(value) for value in operands]
    if operation in BINARY_OPERATIONS:
        if len(numbers) != 2:
            raise ValueError(f"'{operation}' needs exactly 2 numbers")
        return BINARY_OPERATIONS[operation](*numbers)
    if operation in UNARY_OPERATIONS:
        if len(numbers) != 1:
            raise ValueError(f"'{operation}' needs exactly 1 number")
        return UNARY_OPERATIONS[operation](numbers[0])
    raise ValueError(f"Unknown operation '{operation}'")


def format_result(value):
    """Format a result for display, dropping a trailing '.0' on whole numbers."""
    value = to_number(value)
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


@click.command()
@click.argument("operation", type=click.Choice(ALL_OPERATIONS))
@click.argument("numbers", nargs=-1, type=float, required=True)
def cli(operation, numbers):
    """Apply OPERATION to NUMBERS and print the result.

    Put -- before the numbers if any of them are negative.
    """
    try:
        result = calculate(operation, numbers)
    except (ValueError, TypeError) as error:
        raise click.ClickException(str(error)) from error
    click.echo(format_result(result))


if __name__ == "__main__":  # pragma: no cover
    cli()  # pylint: disable=no-value-for-parameter
