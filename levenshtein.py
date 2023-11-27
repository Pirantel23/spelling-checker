def levenshtein_distance_normalized(s1: str, s2: str, weights=None) -> int:
    s1 = s1.lower()
    s2 = s2.lower()
    if weights is None:
        weights = {'delete': 1, 'insert': 1, 'substitute': 1}
    matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        matrix[i][0] = i * weights['delete']
    for j in range(len(s2) + 1):
        matrix[0][j] = j * weights['insert']

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            substitution_cost = weights['substitute'] if s1[i - 1] != s2[j - 1] else 0
            deletion_cost = weights['delete']
            insertion_cost = weights['insert']

            matrix[i][j] = min(matrix[i - 1][j] + deletion_cost,
                               matrix[i][j - 1] + insertion_cost,
                               matrix[i - 1][j - 1] + substitution_cost)

    normalized = 1 - matrix[-1][-1] / max(len(s1), len(s2))
    return normalized
