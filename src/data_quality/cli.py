"""Command-line interface for the data-quality tool."""

import argparse
import logging
import sys
from pathlib import Path

from data_quality.pipeline import run

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Define the command-line interface."""
    parser = argparse.ArgumentParser(
        prog="data-quality",
        description="Validate a CSV against the data contract.",
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Input CSV file to validate",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for clean.csv, rejects.csv, and summary.json",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns an exit code: 0 on success, 1 on failure."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=args.log_level, format="%(levelname)s %(name)s: %(message)s"
    )
    try:
        run(args.input, args.output_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
