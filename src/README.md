# data-quality

A command-line tool that validates a CSV against an explicit data contract,
splits clean rows from rejects (each reject tagged with its reason), and writes
`clean.csv`, `rejects.csv`, and `summary.json`.

Typed modules, contract-first validation, and a full quality gate
(pytest, ruff, mypy) running in CI on every push.

## Quickstart

```bash
pip install -e ".[dev]"
data-quality --input patients.csv --output-dir output/
