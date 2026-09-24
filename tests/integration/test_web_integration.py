"""Integration tests: drive the Flask GUI and JSON API with Flask's test client."""

import pytest

from src.web_app import create_app


@pytest.fixture(name="client")
def fixture_client():
    """A Flask test client that sends requests without starting a real server."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_shows_the_form(client):
    """GET / shows the calculator with every operation in the dropdown."""
    response = client.get("/")
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "<h1>Calculator</h1>" in page
    for operation in ["add", "divide", "power", "sqrt", "factorial"]:
        assert f'value="{operation}"' in page
    assert 'id="result"' not in page


@pytest.mark.parametrize(
    ("form", "expected"),
    [
        ({"operation": "add", "first": "2", "second": "3"}, "5"),
        ({"operation": "subtract", "first": "-3", "second": "5"}, "-8"),
        ({"operation": "multiply", "first": "2.5", "second": "4"}, "10"),
        ({"operation": "divide", "first": "7", "second": "2"}, "3.5"),
        ({"operation": "power", "first": "2", "second": "10"}, "1024"),
        ({"operation": "mod", "first": "10", "second": "3"}, "1"),
        ({"operation": "percent", "first": "200", "second": "15"}, "30"),
        ({"operation": "sqrt", "first": "16", "second": ""}, "4"),
        ({"operation": "factorial", "first": "5"}, "120"),
    ],
)
def test_form_submission_shows_result(client, form, expected):
    """Submitting the form shows the right answer for every operation."""
    response = client.post("/", data=form)
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert f'<output id="result">{expected}</output>' in page


def test_form_keeps_entered_values(client):
    """After submitting, the user's numbers and operation stay filled in."""
    form = {"operation": "multiply", "first": "6", "second": "7"}
    page = client.post("/", data=form).get_data(as_text=True)
    assert 'value="6"' in page
    assert 'value="7"' in page
    assert 'value="multiply" selected' in page


def test_divide_by_zero_shows_error(client):
    """Maths errors are shown on the page instead of crashing."""
    form = {"operation": "divide", "first": "5", "second": "0"}
    page = client.post("/", data=form).get_data(as_text=True)
    assert 'id="error"' in page
    assert "Cannot divide by zero" in page
    assert 'id="result"' not in page


def test_invalid_number_shows_error(client):
    """Non-numeric input is reported to the user."""
    form = {"operation": "add", "first": "abc", "second": "1"}
    page = client.post("/", data=form).get_data(as_text=True)
    assert "First number must be a number" in page


def test_user_input_is_html_escaped(client):
    """Input echoed back on the page is escaped, so scripts cannot be injected."""
    form = {"operation": "<script>alert(1)</script>", "first": "1", "second": "1"}
    page = client.post("/", data=form).get_data(as_text=True)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


def test_api_returns_result(client):
    """The JSON API returns the formatted result."""
    response = client.post(
        "/api/calculate", json={"operation": "power", "first": 2, "second": 8}
    )
    assert response.status_code == 200
    assert response.get_json() == {"result": "256"}


def test_api_returns_error_with_400(client):
    """The JSON API reports errors with HTTP 400."""
    response = client.post("/api/calculate", json={"operation": "sqrt", "first": -4})
    assert response.status_code == 400
    assert "negative" in response.get_json()["error"]


def test_api_without_json_body_returns_400(client):
    """A request with no JSON body is rejected cleanly."""
    response = client.post("/api/calculate", data="not json")
    assert response.status_code == 400
    assert "Unknown operation" in response.get_json()["error"]
