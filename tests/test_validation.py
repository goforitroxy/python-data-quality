"""Tests for validation rules: pure functions, no I/O."""
import pandas as pd
import pytest

from data_quality.contract import DEFAULT_CONTRACT
from data_quality.validation import (
    count_duplicates,
    count_nulls,
    find_missing_columns,
    reject_reasons,
)


@pytest.fixture
def patients() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": ["p1", "p2", "p3"],
            "birthdate": ["2020-01-01", "2019-05-05", "2021-12-12"],
            "gender": ["F", "M", "F"],
        }
    )


def test_find_missing_columns_none_missing(patients):
    assert find_missing_columns(patients, ["id", "birthdate"]) == []


def test_find_missing_columns_reports_missing(patients):
    assert find_missing_columns(patients, ["id", "nope"]) == ["nope"]


def test_count_nulls():
    df = pd.DataFrame({"a": [1, None], "b": [None, None]})
    assert count_nulls(df) == {"a": 1, "b": 2}


def test_count_duplicates():
    df = pd.DataFrame({"id": ["p1", "p1", "p2"]})
    assert count_duplicates(df) == 1


def test_reject_reasons_clean_rows(patients):
    reasons = reject_reasons(patients, DEFAULT_CONTRACT)
    assert (reasons == "").all()


def test_reject_reasons_duplicate_key():
    df = pd.DataFrame(
        {
            "id": ["p1", "p1"],
            "birthdate": ["2020-01-01", "2020-01-01"],
            "gender": ["F", "M"],
        }
    )
    reasons = reject_reasons(df, DEFAULT_CONTRACT)
    assert list(reasons) == ["duplicate_key", "duplicate_key"]


def test_reject_reasons_null_key():
    df = pd.DataFrame(
        {
            "id": ["p1", None],
            "birthdate": ["2020-01-01", "2020-01-01"],
            "gender": ["F", "M"],
        }
    )
    reasons = reject_reasons(df, DEFAULT_CONTRACT)
    assert list(reasons) == ["", "null_key"]


def test_reject_reasons_bad_date():
    df = pd.DataFrame({"id": ["p1"], "birthdate": ["not-a-date"], "gender": ["F"]})
    reasons = reject_reasons(df, DEFAULT_CONTRACT)
    assert list(reasons) == ["bad_date:birthdate"]


def test_reject_reasons_first_reason_wins():
    df = pd.DataFrame({"id": [None], "birthdate": ["not-a-date"], "gender": ["F"]})
    reasons = reject_reasons(df, DEFAULT_CONTRACT)
    assert list(reasons) == ["null_key"]
