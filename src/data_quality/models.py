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

