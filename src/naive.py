def edit_distance_naive(s1: str, s2: str) -> int:
    """
    Compute edit distance using naive recursion.
    Operations: insert, delete, replace (each costs 1).
    """
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    
    if s1[-1] == s2[-1]:
        return edit_distance_naive(s1[:-1], s2[:-1])
    else:
        return 1 + min(
            edit_distance_naive(s1[:-1], s2),      # delete
            edit_distance_naive(s1, s2[:-1]),      # insert
            edit_distance_naive(s1[:-1], s2[:-1])  # replace
        )