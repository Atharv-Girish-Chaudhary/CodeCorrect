"""
Tests for naive.py and memoized.py (Sandeep's implementations).

Run with:  pytest tests/test_naive_memoized.py -v
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from naive import edit_distance_naive, edit_distance_naive_with_ops
from memoized import edit_distance_memoized, edit_distance_memoized_with_ops, accuracy_on_dataset


# ---------------------------------------------------------------------------
# Shared correctness cases — both implementations must agree
# ---------------------------------------------------------------------------

KNOWN_DISTANCES = [
    # (s1, s2, expected_distance)
    ("", "", 0),
    ("a", "", 1),
    ("", "a", 1),
    ("a", "a", 0),
    ("abc", "abc", 0),
    ("abc", "ab", 1),           # one delete
    ("ab", "abc", 1),           # one insert
    ("abc", "axc", 1),          # one replace
    ("kitten", "sitting", 3),   # classic CLRS example
    ("pritn", "print", 2),      # transposition — twiddle in CLRS 15-5
    ("lenght", "length", 2),
    ("retrun", "return", 2),
    ("improt", "import", 2),
    ("defn", "def", 1),
    ("flase", "False", 3),      # f→F + a/l swap (2 ops in standard Levenshtein, no twiddle)
    ("whiel", "while", 2),
    ("sunday", "saturday", 3),
]


@pytest.mark.parametrize("s1, s2, expected", KNOWN_DISTANCES)
def test_naive_known_distances(s1, s2, expected):
    assert edit_distance_naive(s1, s2) == expected


@pytest.mark.parametrize("s1, s2, expected", KNOWN_DISTANCES)
def test_memoized_known_distances(s1, s2, expected):
    assert edit_distance_memoized(s1, s2) == expected


@pytest.mark.parametrize("s1, s2, _", KNOWN_DISTANCES)
def test_naive_and_memoized_agree(s1, s2, _):
    """The two implementations must always return the same distance."""
    assert edit_distance_naive(s1, s2) == edit_distance_memoized(s1, s2)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_strings():
    assert edit_distance_naive("", "") == 0
    assert edit_distance_memoized("", "") == 0


def test_one_empty():
    assert edit_distance_naive("hello", "") == 5
    assert edit_distance_memoized("", "world") == 5


def test_single_char_replace():
    assert edit_distance_naive("a", "b") == 1
    assert edit_distance_memoized("a", "b") == 1


def test_identical_strings():
    for word in ["print", "return", "lambda", "enumerate"]:
        assert edit_distance_naive(word, word) == 0
        assert edit_distance_memoized(word, word) == 0


def test_symmetry():
    """edit_distance(a, b) == edit_distance(b, a)"""
    pairs = [("abc", "cab"), ("pritn", "print"), ("hello", "world")]
    for a, b in pairs:
        assert edit_distance_naive(a, b) == edit_distance_naive(b, a)
        assert edit_distance_memoized(a, b) == edit_distance_memoized(b, a)


# ---------------------------------------------------------------------------
# Operation sequence sanity checks (memoized_with_ops)
# ---------------------------------------------------------------------------

def test_ops_distance_matches_memoized():
    """Distance returned by with_ops must match the plain memoized distance."""
    cases = [("pritn", "print"), ("kitten", "sitting"), ("abc", "axc"), ("", "abc")]
    for s1, s2 in cases:
        dist_plain = edit_distance_memoized(s1, s2)
        dist_ops, _ = edit_distance_memoized_with_ops(s1, s2)
        assert dist_plain == dist_ops, f"mismatch for ({s1!r}, {s2!r})"


def test_ops_count_matches_distance():
    """Number of operations must equal the edit distance."""
    cases = [("pritn", "print"), ("defn", "def"), ("abc", "abc"), ("abc", "xyz")]
    for s1, s2 in cases:
        dist, ops = edit_distance_memoized_with_ops(s1, s2)
        assert len(ops) == dist, (
            f"op count {len(ops)} != distance {dist} for ({s1!r}, {s2!r})"
        )


def test_no_ops_for_identical():
    dist, ops = edit_distance_memoized_with_ops("print", "print")
    assert dist == 0
    assert ops == []


def test_naive_ops_distance_matches():
    """Same sanity check for naive_with_ops."""
    cases = [("pritn", "print"), ("abc", "axc"), ("ab", "abc")]
    for s1, s2 in cases:
        dist_plain = edit_distance_naive(s1, s2)
        dist_ops, _ = edit_distance_naive_with_ops(s1, s2)
        assert dist_plain == dist_ops


# ---------------------------------------------------------------------------
# Accuracy evaluation
# ---------------------------------------------------------------------------

def test_accuracy_perfect():
    vocab = ["print", "def", "return"]
    dataset = [("pritn", "print"), ("defn", "def"), ("retrun", "return")]
    result = accuracy_on_dataset(dataset, vocab)
    assert result["top1_accuracy"] == 1.0
    assert result["correct"] == 3


def test_accuracy_empty_dataset():
    result = accuracy_on_dataset([], ["print"])
    assert result["total"] == 0
    assert result["top1_accuracy"] == 0.0


def test_accuracy_keys():
    result = accuracy_on_dataset([("pritn", "print")], ["print", "for"])
    assert set(result.keys()) == {"total", "correct", "top1_accuracy", "avg_distance"}
