"""Profile a CSV and print a summary."""
from pathlib import Path

from data_quality.io import read_csv
from data_quality.models import RunSummary
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
    summary = profile(Path("data/patients.csv"))
    print(f"rows: {summary.rows}")
    print(f"columns: {summary.columns}")
    print(f"nulls: {summary.null_counts}")
    print(f"duplicate rows: {summary.duplicate_rows}")


if __name__ == "__main__":
    main()
