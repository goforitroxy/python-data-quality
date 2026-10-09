"""End-to-end pipeline tests. tmp_path keeps real files untouched."""
import json
from pathlib import Path

import pandas as pd
import pytest

from data_quality.pipeline import run


@pytest.fixture
def good_csv(tmp_path: Path) -> Path:
    p = tmp_path / "in.csv"
    p.write_text("id,birthdate,gender\np1,2020-01-01,F\np2,2019-05-05,M\n")
    return p


def test_run_writes_clean_rejects_summary(good_csv: Path, tmp_path: Path):
    out = tmp_path / "out"
    summary = run(good_csv, out)
    assert summary.accepted_rows == 2
    assert summary.rejected_rows == 0
    assert (out / "clean.csv").exists()
    assert (out / "rejects.csv").exists()
    payload = json.loads((out / "summary.json").read_text())
    assert payload["accepted_rows"] == 2


def test_run_quarantines_bad_rows(tmp_path: Path):
    src = tmp_path / "bad.csv"
    src.write_text(
        "id,birthdate,gender\np1,2020-01-01,F\np1,2020-01-01,F\np2,not-a-date,M\n"
    )
    summary = run(src, tmp_path / "out")
    assert summary.accepted_rows == 0
    assert summary.rejected_rows == 3
    rejects = pd.read_csv(tmp_path / "out" / "rejects.csv")
    assert set(rejects["rejection_reason"]) == {"duplicate_key", "bad_date:birthdate"}


def test_run_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        run(tmp_path / "nope.csv", tmp_path / "out")


def test_run_missing_columns_raises(tmp_path: Path):
    src = tmp_path / "in.csv"
    src.write_text("id,birthdate\np1,2020-01-01\n")
    with pytest.raises(ValueError, match="missing required columns"):
        run(src, tmp_path / "out")


def test_run_empty_input(tmp_path: Path):
    src = tmp_path / "empty.csv"
    src.write_text("id,birthdate,gender\n")
    summary = run(src, tmp_path / "out")
    assert summary.rows == 0
    assert summary.accepted_rows == 0
