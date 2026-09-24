"""Browser-based GUI for the calculator, built with Flask.

Start it from the project root with:
    python -m src.web_app
then open http://127.0.0.1:5000 in a web browser.
"""

import math

from flask import Blueprint, Flask, jsonify, render_template, request

from src.cli import ALL_OPERATIONS, UNARY_OPERATIONS, calculate, format_result

OPERATION_LABELS = {
    "add": "Add (x + y)",
    "subtract": "Subtract (x - y)",
    "multiply": "Multiply (x × y)",
    "divide": "Divide (x ÷ y)",
    "power": "Power (x ^ y)",
    "mod": "Modulus (x mod y)",
    "percent": "Percentage (y% of x)",
    "sqrt": "Square root (√x)",
    "factorial": "Factorial (x!)",
}

calculator_blueprint = Blueprint("calculator", __name__)


def parse_number(text, label):
    """Convert user input to a finite float, or raise ValueError with a message."""
    try:
        number = float(text)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a number") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number")
    return number


def compute(operation, first, second=None):
    """Validate raw input values and return the formatted result as a string.

    The second value is ignored for one-number operations (sqrt, factorial).
    """
    if operation not in ALL_OPERATIONS:
        raise ValueError(f"Unknown operation '{operation}'")
    operands = [parse_number(first, "First number")]
    if operation not in UNARY_OPERATIONS:
        operands.append(parse_number(second, "Second number"))
    return format_result(calculate(operation, operands))


@calculator_blueprint.route("/", methods=["GET", "POST"])
def index():
    """Show the calculator form and, after a submit, the result or an error."""
    form = {"operation": "add", "first": "", "second": ""}
    result = None
    error = None
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        try:
            result = compute(form["operation"], form["first"], form["second"])
        except ValueError as exc:
            error = str(exc)
    return render_template(
        "index.html",
        operations=OPERATION_LABELS,
        unary_operations=sorted(UNARY_OPERATIONS),
        form=form,
        result=result,
        error=error,
    )


@calculator_blueprint.route("/api/calculate", methods=["POST"])
def api_calculate():
    """JSON API. Send {"operation": "add", "first": 2, "second": 3}."""
    data = request.get_json(silent=True) or {}
    try:
        result = compute(
            data.get("operation", ""), data.get("first"), data.get("second")
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"result": result})


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(calculator_blueprint)
    return app


if __name__ == "__main__":  # pragma: no cover
    create_app().run()
