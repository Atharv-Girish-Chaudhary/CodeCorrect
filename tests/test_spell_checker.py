"""
Integration tests for the spell_checker.py CLI.

Run with:  pytest tests/test_spell_checker.py -v
"""

import os
import subprocess
import tempfile
import sys


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
CLI = os.path.join(PROJECT_ROOT, "src", "spell_checker.py")
VOCAB = os.path.join(PROJECT_ROOT, "data", "python_keywords.txt")


def run_cli(*args):
    """Helper to run the CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


def test_basic_invocation():
    rc, out, _ = run_cli("--word", "pritn", "--vocab", VOCAB, "--method", "tabulation", "--top", "3")
    assert rc == 0
    assert "Suggestions for 'pritn':" in out
    assert "print" in out


def test_default_method():
    rc, out, _ = run_cli("--word", "retrun", "--vocab", VOCAB)
    assert rc == 0
    assert "return" in out


def test_all_methods_produce_output():
    for method in ["naive", "memoized", "tabulation"]:
        rc, out, _ = run_cli("--word", "defn", "--vocab", VOCAB, "--method", method, "--top", "3")
        assert rc == 0, f"method {method} failed"
        assert "def" in out, f"method {method} missing 'def' in output"


def test_top_limits_results():
    rc, out, _ = run_cli("--word", "pritn", "--vocab", VOCAB, "--top", "2")
    assert rc == 0
    # Count suggestion lines (lines with "distance:")
    suggestion_lines = [l for l in out.strip().split("\n") if "distance:" in l]
    assert len(suggestion_lines) == 2


def test_missing_word_arg():
    rc, _, err = run_cli("--vocab", VOCAB)
    assert rc != 0
    assert "required" in err.lower() or "word" in err.lower()


def test_invalid_method():
    rc, _, err = run_cli("--word", "pritn", "--vocab", VOCAB, "--method", "invalid")
    assert rc != 0


def test_missing_vocab_file():
    rc, _, err = run_cli("--word", "pritn", "--vocab", "/nonexistent/vocab.txt")
    assert rc != 0


def test_empty_vocab_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("")
        path = f.name
    try:
        rc, out, _ = run_cli("--word", "pritn", "--vocab", path)
        assert rc == 0
        assert "Suggestions for 'pritn':" in out
    finally:
        os.unlink(path)
