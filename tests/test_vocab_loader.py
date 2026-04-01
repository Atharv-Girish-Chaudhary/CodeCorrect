"""
Tests for vocab_loader.py.

Run with:  pytest tests/test_vocab_loader.py -v
"""

import os
import tempfile
import pytest
from vocab_loader import load_vocabulary


def test_load_valid_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("print\ndef\nreturn\n")
        path = f.name
    try:
        vocab = load_vocabulary(path)
        assert vocab == ["print", "def", "return"]
    finally:
        os.unlink(path)


def test_load_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("")
        path = f.name
    try:
        vocab = load_vocabulary(path)
        assert vocab == []
    finally:
        os.unlink(path)


def test_load_file_with_blank_lines():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("print\n\n\ndef\n  \nreturn\n")
        path = f.name
    try:
        vocab = load_vocabulary(path)
        assert vocab == ["print", "def", "return"]
    finally:
        os.unlink(path)


def test_load_file_strips_whitespace():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("  print  \n  def  \n")
        path = f.name
    try:
        vocab = load_vocabulary(path)
        assert vocab == ["print", "def"]
    finally:
        os.unlink(path)


def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_vocabulary("/nonexistent/path/vocab.txt")


def test_load_real_python_keywords():
    """Smoke test against the actual data file."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "python_keywords.txt")
    if os.path.exists(data_path):
        vocab = load_vocabulary(data_path)
        assert len(vocab) > 0
        assert "print" in vocab
