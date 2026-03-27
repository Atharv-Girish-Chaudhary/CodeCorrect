def edit_distance_memoized(s1: str, s2: str) -> int:
    """
    Compute edit distance using top-down memoization.
    Operations: insert, delete, replace (each costs 1).
    """
    memo = {}
    
    def dp(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        if i == 0:
            return j
        if j == 0:
            return i
        
        if s1[i-1] == s2[j-1]:
            memo[(i, j)] = dp(i-1, j-1)
        else:
            memo[(i, j)] = 1 + min(dp(i-1, j), dp(i, j-1), dp(i-1, j-1))
        return memo[(i, j)]
    
    return dp(len(s1), len(s2))