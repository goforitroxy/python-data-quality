"""Orchestrate a full run: read -> normalize -> validate -> split -> write."""

import json
import logging
from dataclasses import asdict
from pathlib import Path

from data_quality.contract import DEFAULT_CONTRACT, Contract
from data_quality.io import read_csv, write_csv
from data_quality.models import RunSummary
from data_quality.transform import normalize_column_names, strip_whitespace
from data_quality.validation import (
    count_duplicates,
    count_nulls,
    find_missing_columns,
    reject_reasons,
)

log = logging.getLogger(__name__)


def run(
    input_path: Path, output_dir: Path, contract: Contract = DEFAULT_CONTRACT
) -> RunSummary:
    """Run the full pipeline and return a summary. Raises on bad input."""
    log.info("reading %s", input_path)
    try:
        df = read_csv(input_path)
    except FileNotFoundError:
        log.error("input file not found: %s", input_path)
        raise

    df = normalize_column_names(df)
    df = strip_whitespace(df)

    missing = find_missing_columns(df, list(contract.required_columns))
    if missing:
        log.error("missing required columns: %s", missing)
        raise ValueError(f"missing required columns: {missing}")

    reasons = reject_reasons(df, contract)
    clean = df.loc[reasons == ""].copy()
    rejected = df.loc[reasons != ""].copy()
    rejected["rejection_reason"] = reasons[reasons != ""]

    output_dir.mkdir(parents=True, exist_ok=True)
    clean_path = output_dir / "clean.csv"
    rejects_path = output_dir / "rejects.csv"
    write_csv(clean, clean_path)
    write_csv(rejected, rejects_path)

    summary = RunSummary(
        input_path=input_path,
        rows=len(df),
        columns=list(df.columns),
        null_counts=count_nulls(df),
        duplicate_rows=count_duplicates(df),
        accepted_rows=len(clean),
        rejected_rows=len(rejected),
        clean_path=clean_path,
        rejects_path=rejects_path,
    )
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(asdict(summary), indent=2, default=str))
    log.info(
        "input=%d accepted=%d rejected=%d",
        summary.rows,
        summary.accepted_rows,
        summary.rejected_rows,
    )
    log.info("wrote %s %s %s", clean_path, rejects_path, summary_path)
    return summary
