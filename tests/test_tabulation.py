import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tabulation import edit_distance_tabulation, edit_distance_optimized


# ── Basic Operations ──

def test_simple_replace():
    assert edit_distance_tabulation("cat", "car") == 1

def test_simple_insert():
    assert edit_distance_tabulation("cat", "cats") == 1

def test_simple_delete():
    assert edit_distance_tabulation("cats", "cat") == 1


# ── Edge Cases ──

def test_both_empty():
    assert edit_distance_tabulation("", "") == 0

def test_first_empty():
    assert edit_distance_tabulation("", "hello") == 5

def test_second_empty():
    assert edit_distance_tabulation("hello", "") == 5

def test_identical_strings():
    assert edit_distance_tabulation("same", "same") == 0


# ── Known Examples ──

def test_completely_different():
    assert edit_distance_tabulation("abc", "xyz") == 3

def test_kitten_sitting():
    assert edit_distance_tabulation("kitten", "sitting") == 3

def test_pritn_print():
    assert edit_distance_tabulation("pritn", "print") == 2

def test_sunday_saturday():
    assert edit_distance_tabulation("sunday", "saturday") == 3

def test_intention_execution():
    assert edit_distance_tabulation("intention", "execution") == 5

def test_adjacent_swap():
    assert edit_distance_tabulation("ab", "ba") == 2


# ── Code Typos ──

def test_typo_retrun():
    assert edit_distance_tabulation("retrun", "return") == 2

def test_typo_lenght():
    assert edit_distance_tabulation("lenght", "length") == 2

def test_typo_flase():
    assert edit_distance_tabulation("flase", "false") == 2

def test_typo_ture():
    assert edit_distance_tabulation("ture", "true") == 2


# ── Properties ──

def test_symmetry():
    assert edit_distance_tabulation("cat", "car") == edit_distance_tabulation("car", "cat")
    assert edit_distance_tabulation("kitten", "sitting") == edit_distance_tabulation("sitting", "kitten")

def test_distance_never_negative():
    assert edit_distance_tabulation("any", "thing") >= 0

def test_upper_bound():
    s1, s2 = "abc", "xyz"
    assert edit_distance_tabulation(s1, s2) <= max(len(s1), len(s2))


# ── Optimized Matches Tabulation ──

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
def test_optimized_matches_tabulation(s1, s2):
    assert edit_distance_tabulation(s1, s2) == edit_distance_optimized(s1, s2)