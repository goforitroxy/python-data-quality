.PHONY: check
check:
	ruff format --check .
	ruff check .
	mypy src
	pytest -q
