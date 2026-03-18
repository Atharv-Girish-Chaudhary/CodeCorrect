def print_dp_table(s1, s2, dp):
    """Print the DP table with string characters as row/column headers."""

    m, n = len(s1), len(s2)

    # Column headers
    print("     ", end="")
    print(f"{'ε':>4}", end="")
    for ch in s2:
        print(f"{ch:>4}", end="")
    print()

    # Separator
    print("    " + "----" * (n + 1))

    # Rows
    for i in range(m + 1):
        label = "ε" if i == 0 else s1[i - 1]
        print(f"  {label} |", end="")
        for j in range(n + 1):
            print(f"{dp[i][j]:>4}", end="")
        print()

def edit_distance_tabulation(s1: str, s2: str) -> int:
    """
    Compute edit distance using bottom-up tabulation.

    Fills an (m+1) x (n+1) table iteratively, row by row.
    Operations: insert, delete, replace (each costs 1).
    """
    m = len(s1)
    n = len(s2)

    # Create (m+1) x (n+1) matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # delete all characters from s1[0..i-1]
    for j in range(n + 1):
        dp[0][j] = j  # insert all characters of s2[0..j-1]

    # Fill the table using bottom-up approach
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # characters match, no edit needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete from s1
                    dp[i][j - 1],      # insert into s1
                    dp[i - 1][j - 1],  # replace in s1
                )

    return dp[m][n]


def edit_distance_optimized(s1: str, s2: str) -> int:
    """
    Space-optimized bottom-up tabulation.

    Since each row only depends on the previous row, we only
    keep two rows in memory at a time.
    """
    # Ensure s2 is the shorter string for space optimization
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    m, n = len(s1), len(s2)

    prev = list(range(n + 1))  # base case: dp[0][j] = j
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i  # base case: dp[i][0] = i
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    prev[j],        # delete
                    curr[j - 1],    # insert
                    prev[j - 1],    # replace
                )
        prev, curr = curr, prev  # swap rows

    return prev[n]


if __name__ == "__main__":
    # Sample Test Case
    s1, s2 = "pritn", "print"
    expected = 2
    
    print(f"Edit Distance Testing: '{s1}' -> '{s2}'")
    
    # 1. Standard Tabulation
    result = edit_distance_tabulation(s1, s2)
    print(f"  Tabulation Result: {result} (Expected: {expected})")
    
    # 2. Space-Optimized Tabulation
    result_opt = edit_distance_optimized(s1, s2)
    print(f"  Optimized Result:  {result_opt} (Expected: {expected})")
    
    # 3. DP Table Visualization
    print("\nDP Table Visualization:")
    # Re-calculate table for visualization
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    print_dp_table(s1, s2, dp)

