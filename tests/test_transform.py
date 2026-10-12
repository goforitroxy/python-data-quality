"""Tests for pure transformations."""

import pandas as pd

from data_quality.transform import normalize_column_names, strip_whitespace


def test_normalize_column_names():
    df = pd.DataFrame({" First Name ": [1], "BIRTHDATE": [2]})
    out = normalize_column_names(df)
    assert list(out.columns) == ["first_name", "birthdate"]


def test_normalize_does_not_mutate_input():
    df = pd.DataFrame({"A B": [1]})
    normalize_column_names(df)
    assert list(df.columns) == ["A B"]


def test_strip_whitespace():
    df = pd.DataFrame({"name": ["  amy ", "bob"], "age": [30, 40]})
    out = strip_whitespace(df)
    assert list(out["name"]) == ["amy", "bob"]
