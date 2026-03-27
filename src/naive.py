"""
naive.py — Naive recursive edit distance (no caching).

Operations: insert, delete, replace (each cost 1).
Time:  O(3^(m+n))  — exponential, recomputes subproblems
Space: O(m+n)      — recursion stack depth

Per CLRS Ch. 15 / Problem 15-5:
  'twiddle' (transposition) is NOT included here; this is the classic
  3-operation Levenshtein model.  See memoized.py for the same model
  with caching, and tabulation.py for the bottom-up version.
"""


def edit_distance_naive(s1: str, s2: str) -> int:
    """Return the minimum edit distance between s1 and s2."""
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    if s1[-1] == s2[-1]:
        return edit_distance_naive(s1[:-1], s2[:-1])

    return 1 + min(
        edit_distance_naive(s1[:-1], s2),       # delete last char of s1
        edit_distance_naive(s1, s2[:-1]),       # insert last char of s2 into s1
        edit_distance_naive(s1[:-1], s2[:-1]),  # replace last char of s1
    )


def edit_distance_naive_with_ops(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Return (min_edit_distance, operations) where operations is a list of
    human-readable strings describing each edit, e.g.:
        ["replace 'r' with 'p' at index 2", "insert 't' at index 4"]

    NOTE: Because this is naive recursion (no memoization), this function
    is only practical for short strings (len <= ~12).  For larger inputs
    use memoized_with_ops from memoized.py.
    """
    def _recurse(i: int, j: int) -> tuple[int, list[str]]:
        # Base cases
        if i == 0:
            ops = [f"insert '{s2[k]}' at position {k}" for k in range(j)]
            return j, ops
        if j == 0:
            ops = [f"delete '{s1[k]}' at position {k}" for k in range(i)]
            return i, ops

        if s1[i - 1] == s2[j - 1]:
            return _recurse(i - 1, j - 1)

        del_cost, del_ops = _recurse(i - 1, j)
        ins_cost, ins_ops = _recurse(i, j - 1)
        rep_cost, rep_ops = _recurse(i - 1, j - 1)

        best_cost = 1 + min(del_cost, ins_cost, rep_cost)

        if rep_cost <= del_cost and rep_cost <= ins_cost:
            return best_cost, rep_ops + [
                f"replace '{s1[i-1]}' with '{s2[j-1]}' at position {i-1}"
            ]
        elif del_cost <= ins_cost:
            return best_cost, del_ops + [
                f"delete '{s1[i-1]}' at position {i-1}"
            ]
        else:
            return best_cost, ins_ops + [
                f"insert '{s2[j-1]}' at position {j-1}"
            ]

    return _recurse(len(s1), len(s2))


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    examples = [
        ("pritn", "print"),
        ("lenght", "length"),
        ("retrun", "return"),
        ("improt", "import"),
        ("defn", "def"),
    ]
    print(f"{'Typo':<12} {'Correct':<12} {'Distance':>8}  Operations")
    print("-" * 70)
    for typo, correct in examples:
        dist, ops = edit_distance_naive_with_ops(typo, correct)
        print(f"{typo:<12} {correct:<12} {dist:>8}  {'; '.join(ops)}")
