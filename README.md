# Calculator CI/CD

A Python calculator built by a two-person team to practise
feature branches, Pull Requests and a GitHub Actions CI/CD pipeline.
It has two front ends: a web GUI (Flask) and a command-line interface (Click).

## Web GUI

```bash
python -m src.web_app
```

Open http://127.0.0.1:5000 in your browser, pick an operation, enter the
numbers and press **Calculate**. Press `Ctrl+C` in the terminal to stop it.

The same calculator is available as a JSON API:

```bash
curl -X POST http://127.0.0.1:5000/api/calculate -H "Content-Type: application/json" -d '{"operation": "add", "first": 2, "second": 3}'
```

## Command-line interface

| Command     | Example                          | Result |
|-------------|----------------------------------|--------|
| `add`       | `python -m src.cli add 2 3`      | 5      |
| `subtract`  | `python -m src.cli subtract 10 4`| 6      |
| `multiply`  | `python -m src.cli multiply 3 4` | 12     |
| `divide`    | `python -m src.cli divide 7 2`   | 3.5    |
| `power`     | `python -m src.cli power 2 10`   | 1024   |
| `mod`       | `python -m src.cli mod 10 3`     | 1      |
| `percent`   | `python -m src.cli percent 200 15` | 30   |
| `sqrt`      | `python -m src.cli sqrt 16`      | 4      |
| `factorial` | `python -m src.cli factorial 5`  | 120    |

Negative numbers must come after `--`, for example
`python -m src.cli add -- -3 5`.

## Setup

```bash
git clone https://github.com/<owner>/calculator-cicd.git
cd calculator-cicd
python -m pip install -r requirements.txt
```

## Running the quality checks locally

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80
pylint src/ --fail-under=7.0
black src/ tests/ --check
bandit -r src/ -lll
```

## Project structure

```
src/
  validators.py           shared input validation         (main)
  basic_operations.py     add, subtract, multiply, divide (feature/basic-operations)
  advanced_operations.py  power, sqrt, mod, %, factorial  (feature/advanced-operations)
  cli.py                  Click command-line interface    (feature/cli)
  web_app.py              Flask web GUI + JSON API        (feature/web-gui)
  templates/index.html    the GUI page                    (feature/web-gui)
tests/
  unit/                   tests for each function
  integration/            end-to-end CLI and GUI tests
.github/workflows/ci.yml  CI/CD pipeline
```

## CI/CD pipeline

Every push and every Pull Request into `main` runs:
Build → Test → Coverage (≥ 80%) → Lint (pylint ≥ 7.0) → Format (black)
→ Security (bandit). Pushes to `main` also run a Package (CD) stage that
uploads a deployment zip. Reports are downloadable from each run's
Artifacts section on the Actions tab.
