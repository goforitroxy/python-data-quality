"""Checks that answer: is this data fit to use? No file I/O here."""

import pandas as pd

from data_quality.contract import Contract


def find_missing_columns(df: pd.DataFrame, required: list[str]) -> list[str]:
    """Return required column names not present in df."""
    return [c for c in required if c not in df.columns]


def count_nulls(df: pd.DataFrame) -> dict[str, int]:
    """Map each column to its number of null values."""
    return {str(c): int(n) for c, n in df.isna().sum().items()}


def count_duplicates(df: pd.DataFrame) -> int:
    """Number of duplicated rows (beyond the first occurrence)."""
    return int(df.duplicated().sum())


def reject_reasons(df: pd.DataFrame, contract: Contract) -> pd.Series:
    """One rejection reason per row; empty string means the row is clean.

    Only the first failing check is recorded, so reasons stay readable.
    """
    reasons = pd.Series("", index=df.index)
    key = contract.unique_key
    checks: list[tuple[pd.Series, str]] = [
        (df[key].isna(), "null_key"),
        (df[key].duplicated(keep=False), "duplicate_key"),
    ]
    for col in contract.date_columns:
        if col in df.columns:
            parsed = pd.to_datetime(
                df[col], format=contract.date_format, errors="coerce"
            )
            checks.append((df[col].notna() & parsed.isna(), f"bad_date:{col}"))
    for mask, reason in checks:
        reasons = reasons.mask(mask & (reasons == ""), reason)
    return reasons
