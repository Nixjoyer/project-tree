"""CLI test coverage for argument parsing and orchestration."""

from pathlib import Path
from unittest.mock import patch

import pytest

from projtree import __version__
from projtree.cli import argparse_main


class TestOutputIgnoreBehavior:
    """Tests for output file ignore behavior."""

    def test_output_name_ignored_when_output_is_under_root(self, tmp_path: Path):
        """Add output name to ignores when output stays under root."""
        output = tmp_path / "structure.md"
        captured_ignore = None

        def fake_generate_markdown_tree(_root, ignore):
            nonlocal captured_ignore
            captured_ignore = ignore
            return "# Project Structure\n"

        with patch("projtree.cli.generate_markdown_tree", side_effect=fake_generate_markdown_tree):
            result = argparse_main([str(tmp_path), "-o", str(output)])

        assert result == 0
        assert captured_ignore is not None
        assert output.name in captured_ignore

    def test_output_name_not_ignored_when_output_is_outside_root(self, tmp_path: Path):
        """Avoid ignoring output name when output is outside root."""
        output = tmp_path.parent / "outside.md"
        captured_ignore = None

        def fake_generate_markdown_tree(_root, ignore):
            nonlocal captured_ignore
            captured_ignore = ignore
            return "# Project Structure\n"

        with patch("projtree.cli.generate_markdown_tree", side_effect=fake_generate_markdown_tree):
            result = argparse_main([str(tmp_path), "-o", str(output)])

        assert result == 0
        assert captured_ignore is not None
        assert output.name not in captured_ignore


class TestVersionFlag:
    """Tests for the --version flag."""

    def test_version_flag_short_form(self, capsys):
        """Test that -v flag shows version and exits."""
        with pytest.raises(SystemExit) as exc_info:
            argparse_main(["-v"])
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out
        assert "projtree" in captured.out

    def test_version_flag_long_form(self, capsys):
        """Test that --version flag shows version and exits."""
        with pytest.raises(SystemExit) as exc_info:
            argparse_main(["--version"])
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out
        assert "projtree" in captured.out

    def test_version_flag_exits_before_argument_processing(self, capsys):
        """Test that --version exits before processing other arguments."""
        # Even if we provide an invalid path, --version should exit cleanly
        with pytest.raises(SystemExit) as exc_info:
            argparse_main(["-v", "/nonexistent/path"])
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_version_output_format(self, capsys):
        """Test that version output has expected format."""
        with pytest.raises(SystemExit):
            argparse_main(["--version"])
        
        captured = capsys.readouterr()
        # Output should contain "projtree:" and the version
        assert "projtree:" in captured.out
        assert __version__ in captured.out


class TestWatchOnlyFlag:
    """Tests for the --watch-only flag."""

    def test_watch_only_requires_watch_flag(self, capsys):
        """Test that --watch-only without --watch causes an error."""
        with pytest.raises(SystemExit) as exc_info:
            argparse_main(["--watch-only"])
        
        # argparse.error() calls sys.exit(2) by default
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "--watch-only requires --watch" in captured.err

    def test_watch_only_with_watch_flag(self, tmp_path: Path):
        """Test that --watch-only works when --watch is also provided."""
        output = tmp_path / "structure.md"
        
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "-o", str(output),
                "--watch",
                "--watch-only"
            ])
            
            # verify watch_and_generate was called
            mock_watch.assert_called_once()
            
            # Verify initial_generate is False
            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["initial_generate"] is False

    def test_watch_only_with_watch_passes_correct_args(self, tmp_path: Path):
        """Test that --watch-only with --watch passes all correct arguments."""
        output = tmp_path / "custom_output.md"
        
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "-o", str(output),
                "--watch",
                "--watch-only",
                "--ignore", "node_modules,.git"
            ])
            
            mock_watch.assert_called_once()
            call_kwargs = mock_watch.call_args[1]
            
            # Verify all parameters
            assert call_kwargs["root_path"] == tmp_path
            assert call_kwargs["output_path"] == output
            assert call_kwargs["initial_generate"] is False
            assert call_kwargs["debounce_seconds"] == 0.4
            assert call_kwargs["extra_ignores"] == {"node_modules", ".git"}

    def test_watch_only_with_watch_accepts_ignore_patterns(self, tmp_path: Path):
        """Test that --ignore is forwarded in watch-only mode."""
        output = tmp_path / "structure.md"
        
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "-o", str(output),
                "--watch",
                "--watch-only",
                "--ignore", ".git,node_modules,build"
            ])
            
            mock_watch.assert_called_once()
            # Verify watch-only behavior is still correct
            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["initial_generate"] is False
            assert call_kwargs["extra_ignores"] == {".git", "node_modules", "build"}

    def test_watch_only_flag_position_independent(self, tmp_path: Path):
        """Test that --watch-only works regardless of position relative to --watch."""
        output = tmp_path / "structure.md"
        
        # Test with --watch-only before --watch
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "--watch-only",
                "--watch",
                "-o", str(output),
            ])
            
            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["initial_generate"] is False

    def test_watch_only_without_watch_error_message(self, capsys):
        """Test the specific error message for --watch-only without --watch."""
        with pytest.raises(SystemExit):
            argparse_main([
                ".",
                "--watch-only"
            ])
        
        captured = capsys.readouterr()
        # The error message should be from parser.error()
        assert "error:" in captured.err.lower()
        assert "--watch-only requires --watch" in captured.err

    def test_watch_only_with_output_flag(self, tmp_path: Path):
        """Test --watch-only combined with custom output flag."""
        output = tmp_path / "my_structure.md"
        
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "--watch",
                "--watch-only",
                "--output", str(output)
            ])
            
            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["output_path"] == output
            assert call_kwargs["initial_generate"] is False

    def test_watch_only_default_path(self, tmp_path: Path, monkeypatch):
        """Test that --watch-only uses default path when none is provided."""
        output = tmp_path / "structure.md"
        
        # Change to the tmp_path directory for this test
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            monkeypatch.chdir(tmp_path)

            argparse_main([
                "--watch",
                "--watch-only",
                "-o", str(output)
            ])

            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["initial_generate"] is False
            assert call_kwargs["root_path"] == tmp_path


class TestWatchAndWatchOnlyInteraction:
    """Tests for interaction between --watch and --watch-only flags."""

    def test_watch_without_watch_only_generates_initially(self, tmp_path: Path):
        """Test that --watch alone sets initial_generate to True."""
        output = tmp_path / "structure.md"
        
        with patch("projtree.cli.watch_and_generate") as mock_watch:
            argparse_main([
                str(tmp_path),
                "-o", str(output),
                "--watch"
            ])
            
            call_kwargs = mock_watch.call_args[1]
            assert call_kwargs["initial_generate"] is True

    def test_both_flags_together_return_zero(self, tmp_path: Path):
        """Test that using both flags returns exit code 0."""
        output = tmp_path / "structure.md"
        
        with patch("projtree.cli.watch_and_generate"):
            result = argparse_main([
                str(tmp_path),
                "-o", str(output),
                "--watch",
                "--watch-only"
            ])
            
            assert result == 0


class TestIgnorePathLikeEntries:
    """Tests documenting exact-name ignore semantics."""

    def test_ignore_option_path_like_value_does_not_ignore_nested_entry(self, tmp_path: Path):
        """Keep nested entries when ignore argument is path-like."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "target").write_text("", encoding="utf-8")

        output = tmp_path / "structure.md"
        result = argparse_main([str(tmp_path), "-o", str(output), "--ignore", "src/target"])

        assert result == 0
        contents = output.read_text(encoding="utf-8")
        assert "target" in contents

    def test_projtreeignore_path_like_value_does_not_ignore_nested_entry(self, tmp_path: Path):
        """Keep nested entries when .projtreeignore entry is path-like."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "target").write_text("", encoding="utf-8")
        (tmp_path / ".projtreeignore").write_text("src/target\n", encoding="utf-8")

        output = tmp_path / "structure.md"
        result = argparse_main([str(tmp_path), "-o", str(output)])

        assert result == 0
        contents = output.read_text(encoding="utf-8")
        assert "target" in contents
