"""Checks that answer: is this data fit to use? No file I/O here."""
import pandas as pd


def find_missing_columns(df: pd.DataFrame, required: list[str]) -> list[str]:
    """Return required column names not present in df."""
    return [c for c in required if c not in df.columns]


def count_nulls(df: pd.DataFrame) -> dict[str, int]:
    """Map each column to its number of null values."""
    return {c: int(n) for c, n in df.isna().sum().items()}


def count_duplicates(df: pd.DataFrame) -> int:
    """Number of duplicated rows (beyond the first occurrence)."""
    return int(df.duplicated().sum())

