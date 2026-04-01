"""
Standalone tests for naive.py — mirrors test_tabulation.py edge case coverage.

Run with:  pytest tests/test_naive.py -v
"""

import pytest
from naive import edit_distance_naive, edit_distance_naive_with_ops
from tabulation import edit_distance_tabulation


# ── Basic Operations ──

def test_simple_replace():
    assert edit_distance_naive("cat", "car") == 1

def test_simple_insert():
    assert edit_distance_naive("cat", "cats") == 1

def test_simple_delete():
    assert edit_distance_naive("cats", "cat") == 1


# ── Edge Cases ──

def test_both_empty():
    assert edit_distance_naive("", "") == 0

def test_first_empty():
    assert edit_distance_naive("", "hello") == 5

def test_second_empty():
    assert edit_distance_naive("hello", "") == 5

def test_identical_strings():
    assert edit_distance_naive("same", "same") == 0


# ── Known Examples ──

def test_completely_different():
    assert edit_distance_naive("abc", "xyz") == 3

def test_kitten_sitting():
    assert edit_distance_naive("kitten", "sitting") == 3

def test_pritn_print():
    assert edit_distance_naive("pritn", "print") == 2

def test_sunday_saturday():
    assert edit_distance_naive("sunday", "saturday") == 3

def test_adjacent_swap():
    assert edit_distance_naive("ab", "ba") == 2


# ── Code Typos ──

def test_typo_retrun():
    assert edit_distance_naive("retrun", "return") == 2

def test_typo_lenght():
    assert edit_distance_naive("lenght", "length") == 2

def test_typo_flase():
    assert edit_distance_naive("flase", "false") == 2

def test_typo_ture():
    assert edit_distance_naive("ture", "true") == 2


# ── Properties ──

def test_symmetry():
    assert edit_distance_naive("cat", "car") == edit_distance_naive("car", "cat")
    assert edit_distance_naive("kitten", "sitting") == edit_distance_naive("sitting", "kitten")

def test_distance_never_negative():
    assert edit_distance_naive("any", "thing") >= 0

def test_upper_bound():
    s1, s2 = "abc", "xyz"
    assert edit_distance_naive(s1, s2) <= max(len(s1), len(s2))


# ── Agreement with Tabulation ──

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
def test_naive_matches_tabulation(s1, s2):
    assert edit_distance_naive(s1, s2) == edit_distance_tabulation(s1, s2)


# ── With-Ops Variant ──

def test_with_ops_distance_matches_plain():
    cases = [("pritn", "print"), ("abc", "axc"), ("ab", "abc"), ("", "abc")]
    for s1, s2 in cases:
        dist_plain = edit_distance_naive(s1, s2)
        dist_ops, _ = edit_distance_naive_with_ops(s1, s2)
        assert dist_plain == dist_ops, f"mismatch for ({s1!r}, {s2!r})"

def test_with_ops_count_equals_distance():
    cases = [("pritn", "print"), ("defn", "def"), ("abc", "abc"), ("abc", "xyz")]
    for s1, s2 in cases:
        dist, ops = edit_distance_naive_with_ops(s1, s2)
        assert len(ops) == dist, f"op count {len(ops)} != distance {dist} for ({s1!r}, {s2!r})"

def test_with_ops_empty_for_identical():
    dist, ops = edit_distance_naive_with_ops("print", "print")
    assert dist == 0
    assert ops == []
