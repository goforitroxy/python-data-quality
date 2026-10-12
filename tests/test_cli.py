"""Tests for the command-line interface."""

from data_quality.cli import build_parser, main


def test_parser_requires_input_and_output_dir():
    parser = build_parser()
    args = parser.parse_args(["--input", "a.csv", "--output-dir", "out"])
    assert str(args.input) == "a.csv"
    assert args.log_level == "INFO"


def test_main_missing_file_returns_1(tmp_path, capsys):
    code = main(
        ["--input", str(tmp_path / "nope.csv"), "--output-dir", str(tmp_path / "out")]
    )
    assert code == 1
    assert "error" in capsys.readouterr().err


def test_main_success_returns_0(tmp_path):
    src = tmp_path / "in.csv"
    src.write_text("id,birthdate,gender\np1,2020-01-01,F\n")
    code = main(["--input", str(src), "--output-dir", str(tmp_path / "out")])
    assert code == 0
    assert (tmp_path / "out" / "clean.csv").exists()
