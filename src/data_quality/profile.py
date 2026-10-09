"""Profile a CSV and print a summary."""

import logging
import sys
from pathlib import Path

from data_quality.io import read_csv
from data_quality.models import RunSummary
from data_quality.pipeline import run
from data_quality.transform import normalize_column_names
from data_quality.validation import count_duplicates, count_nulls, find_missing_columns

REQUIRED_COLUMNS = ["id", "birthdate", "gender"]


def profile(input_path: Path) -> RunSummary:
    """Read, normalize, validate, and summarize one CSV file."""
    df = read_csv(input_path)
    df = normalize_column_names(df)
    missing = find_missing_columns(df, REQUIRED_COLUMNS)
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    return RunSummary(
        input_path=input_path,
        rows=len(df),
        columns=list(df.columns),
        null_counts=count_nulls(df),
        duplicate_rows=count_duplicates(df),
    )


def main() -> None:
    """Configure logging, run the pipeline, exit non-zero on failure."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    try:
        run(Path("data/patients.csv"), Path("output"))
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
