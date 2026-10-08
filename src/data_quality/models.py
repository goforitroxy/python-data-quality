"""Shared data structures."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunSummary:
    """Counts and paths describing one profiling run."""
    input_path: Path
    rows: int
    columns: list[str]
    null_counts: dict[str, int]
    duplicate_rows: int
    accepted_rows: int = 0
    rejected_rows: int = 0
    clean_path: Path | None = None
    rejects_path: Path | None = None
