"""
Standalone tests for memoized.py — mirrors test_tabulation.py edge case coverage.

Run with:  pytest tests/test_memoized.py -v
"""

import pytest
from memoized import (
    edit_distance_memoized,
    edit_distance_memoized_with_ops,
    accuracy_on_dataset,
)
from tabulation import edit_distance_tabulation
from naive import edit_distance_naive


# ── Basic Operations ──

def test_simple_replace():
    assert edit_distance_memoized("cat", "car") == 1

def test_simple_insert():
    assert edit_distance_memoized("cat", "cats") == 1

def test_simple_delete():
    assert edit_distance_memoized("cats", "cat") == 1


# ── Edge Cases ──

def test_both_empty():
    assert edit_distance_memoized("", "") == 0

def test_first_empty():
    assert edit_distance_memoized("", "hello") == 5

def test_second_empty():
    assert edit_distance_memoized("hello", "") == 5

def test_identical_strings():
    assert edit_distance_memoized("same", "same") == 0


# ── Known Examples ──

def test_completely_different():
    assert edit_distance_memoized("abc", "xyz") == 3

def test_kitten_sitting():
    assert edit_distance_memoized("kitten", "sitting") == 3

def test_pritn_print():
    assert edit_distance_memoized("pritn", "print") == 2

def test_sunday_saturday():
    assert edit_distance_memoized("sunday", "saturday") == 3

def test_intention_execution():
    assert edit_distance_memoized("intention", "execution") == 5

def test_adjacent_swap():
    assert edit_distance_memoized("ab", "ba") == 2


# ── Code Typos ──

def test_typo_retrun():
    assert edit_distance_memoized("retrun", "return") == 2

def test_typo_lenght():
    assert edit_distance_memoized("lenght", "length") == 2

def test_typo_flase():
    assert edit_distance_memoized("flase", "false") == 2

def test_typo_ture():
    assert edit_distance_memoized("ture", "true") == 2


# ── Properties ──

def test_symmetry():
    assert edit_distance_memoized("cat", "car") == edit_distance_memoized("car", "cat")
    assert edit_distance_memoized("kitten", "sitting") == edit_distance_memoized("sitting", "kitten")

def test_distance_never_negative():
    assert edit_distance_memoized("any", "thing") >= 0

def test_upper_bound():
    s1, s2 = "abc", "xyz"
    assert edit_distance_memoized(s1, s2) <= max(len(s1), len(s2))


# ── Agreement with Tabulation and Naive ──

@pytest.mark.parametrize("s1,s2", [
    ("cat", "car"),
    ("kitten", "sitting"),
    ("pritn", "print"),
    ("", "hello"),
    ("hello", ""),
    ("", ""),
    ("same", "same"),
    ("sunday", "saturday"),
])
def test_memoized_matches_tabulation(s1, s2):
    assert edit_distance_memoized(s1, s2) == edit_distance_tabulation(s1, s2)

@pytest.mark.parametrize("s1,s2", [
    ("cat", "car"),
    ("kitten", "sitting"),
    ("pritn", "print"),
    ("", ""),
    ("abc", "xyz"),
])
def test_memoized_matches_naive(s1, s2):
    assert edit_distance_memoized(s1, s2) == edit_distance_naive(s1, s2)


# ── With-Ops Variant ──

def test_with_ops_distance_matches_plain():
    cases = [("pritn", "print"), ("abc", "axc"), ("ab", "abc"), ("", "abc")]
    for s1, s2 in cases:
        dist_plain = edit_distance_memoized(s1, s2)
        dist_ops, _ = edit_distance_memoized_with_ops(s1, s2)
        assert dist_plain == dist_ops, f"mismatch for ({s1!r}, {s2!r})"

def test_with_ops_count_equals_distance():
    cases = [("pritn", "print"), ("defn", "def"), ("abc", "abc"), ("abc", "xyz")]
    for s1, s2 in cases:
        dist, ops = edit_distance_memoized_with_ops(s1, s2)
        assert len(ops) == dist, f"op count {len(ops)} != distance {dist} for ({s1!r}, {s2!r})"

def test_with_ops_empty_for_identical():
    dist, ops = edit_distance_memoized_with_ops("print", "print")
    assert dist == 0
    assert ops == []


# ── Accuracy Evaluation ──

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

def test_accuracy_partial():
    vocab = ["print", "for", "while"]
    dataset = [("pritn", "print"), ("whiel", "while"), ("xyz", "print")]
    result = accuracy_on_dataset(dataset, vocab)
    assert result["total"] == 3
    assert result["correct"] >= 2  # pritn->print and whiel->while should match
