"""
memoized.py — Top-down memoized edit distance.

Operations: insert, delete, replace (each cost 1).
Time:  O(m * n)  — each (i, j) subproblem solved exactly once
Space: O(m * n)  — memo table + O(m+n) recursion stack

This is the 'top-down DP' counterpart to naive.py (same recurrence,
adds a memo dict) and tabulation.py (same complexity, different traversal).

Per CLRS Ch. 15 / Problem 15-5 connection:
  The three operations map to: copy (cost 0), replace (cost 1),
  insert (cost 1), delete (cost 1).  The twiddle operation for
  transpositions (pritn -> print) is discussed in the project report.
"""

from functools import lru_cache


def edit_distance_memoized(s1: str, s2: str) -> int:
    """Return the minimum edit distance between s1 and s2 (memoized)."""
    memo: dict[tuple[int, int], int] = {}

    def dp(i: int, j: int) -> int:
        if (i, j) in memo:
            return memo[(i, j)]
        if i == 0:
            return j
        if j == 0:
            return i

        if s1[i - 1] == s2[j - 1]:
            memo[(i, j)] = dp(i - 1, j - 1)
        else:
            memo[(i, j)] = 1 + min(
                dp(i - 1, j),      # delete
                dp(i, j - 1),      # insert
                dp(i - 1, j - 1),  # replace
            )
        return memo[(i, j)]

    return dp(len(s1), len(s2))


def edit_distance_memoized_with_ops(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Return (min_edit_distance, operations) using top-down memoization.

    operations is a list of human-readable edit steps, e.g.:
        ["replace 'r' with 'p' at position 2", "insert 't' at position 4"]

    Reconstructs the operation sequence by backtracking through the memo
    table after the distance is computed.
    """
    m, n = len(s1), len(s2)
    memo: dict[tuple[int, int], int] = {}

    def dp(i: int, j: int) -> int:
        if (i, j) in memo:
            return memo[(i, j)]
        if i == 0:
            return j
        if j == 0:
            return i
        if s1[i - 1] == s2[j - 1]:
            memo[(i, j)] = dp(i - 1, j - 1)
        else:
            memo[(i, j)] = 1 + min(
                dp(i - 1, j),
                dp(i, j - 1),
                dp(i - 1, j - 1),
            )
        return memo[(i, j)]

    dist = dp(m, n)

    # Backtrack to reconstruct the sequence of operations
    ops: list[str] = []
    i, j = m, n
    while i > 0 or j > 0:
        if i == 0:
            ops.append(f"insert '{s2[j-1]}' at position {j-1}")
            j -= 1
        elif j == 0:
            ops.append(f"delete '{s1[i-1]}' at position {i-1}")
            i -= 1
        elif s1[i - 1] == s2[j - 1]:
            i -= 1
            j -= 1  # copy — no operation recorded
        else:
            current = memo.get((i, j), float("inf"))
            del_val = memo.get((i - 1, j), i - 1) if i > 0 else float("inf")
            ins_val = memo.get((i, j - 1), j - 1) if j > 0 else float("inf")
            rep_val = memo.get((i - 1, j - 1), abs(i - j)) if i > 0 and j > 0 else float("inf")

            if current == 1 + rep_val and rep_val <= del_val and rep_val <= ins_val:
                ops.append(f"replace '{s1[i-1]}' with '{s2[j-1]}' at position {i-1}")
                i -= 1
                j -= 1
            elif current == 1 + del_val and del_val <= ins_val:
                ops.append(f"delete '{s1[i-1]}' at position {i-1}")
                i -= 1
            else:
                ops.append(f"insert '{s2[j-1]}' at position {j-1}")
                j -= 1

    ops.reverse()
    return dist, ops


def accuracy_on_dataset(dataset: list[tuple[str, str]], vocabulary: list[str]) -> dict:
    """
    Evaluate memoized edit distance as a spell-checker on a typo dataset.

    Args:
        dataset:    list of (typo, correct_word) pairs
        vocabulary: list of valid tokens to search

    Returns:
        dict with keys: total, correct, top1_accuracy, avg_distance
    """
    correct_count = 0
    distances = []

    for typo, expected in dataset:
        # Rank all vocabulary entries by edit distance to the typo
        ranked = sorted(
            vocabulary,
            key=lambda word: edit_distance_memoized(typo, word)
        )
        best = ranked[0]
        dist = edit_distance_memoized(typo, best)
        distances.append(dist)
        if best == expected:
            correct_count += 1

    total = len(dataset)
    return {
        "total": total,
        "correct": correct_count,
        "top1_accuracy": correct_count / total if total else 0.0,
        "avg_distance": sum(distances) / total if total else 0.0,
    }


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
        ("flase", "False"),
        ("ture", "True"),
        ("whiel", "while"),
    ]
    print(f"{'Typo':<12} {'Correct':<12} {'Distance':>8}  Operations")
    print("-" * 80)
    for typo, correct in examples:
        dist, ops = edit_distance_memoized_with_ops(typo, correct)
        print(f"{typo:<12} {correct:<12} {dist:>8}  {'; '.join(ops)}")

    # Accuracy demo against a small vocabulary
    print("\n--- Accuracy Evaluation ---")
    vocab = ["print", "length", "return", "import", "def", "False", "True",
             "while", "for", "else", "class", "if", "with", "yield", "pass"]
    test_data = [(t, c) for t, c in examples]
    results = accuracy_on_dataset(test_data, vocab)
    print(f"Top-1 accuracy: {results['top1_accuracy']:.0%} "
          f"({results['correct']}/{results['total']})")
    print(f"Avg edit distance to best match: {results['avg_distance']:.2f}")
