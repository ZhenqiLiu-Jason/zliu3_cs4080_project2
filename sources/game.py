from itertools import combinations
from collections import Counter
from typing import List, Tuple, Any


def score_combination(combo: List[Tuple[int, Any]]) -> int:
    faces = [v for v, _ in combo]
    face_counts = Counter(faces)
    total_score = 0
    contributing_faces = Counter()

    # Full straight
    if sorted(face_counts.keys()) == [1, 2, 3, 4, 5, 6]:
        return 2500

    # Three pairs
    if len(face_counts) == 3 and all(count == 2 for count in face_counts.values()):
        return 1500

    # 3-6 of a kind
    for face, count in face_counts.items():
        if count >= 3:
            if count == 3:
                score = 1000 if face == 1 else face * 100
            elif count == 4:
                score = 1000
            elif count == 5:
                score = 2000
            elif count == 6:
                score = 3000
            else:
                continue
            total_score += score
            contributing_faces[face] += count  # all of them contributed

    # Add individual 1s and 5s not used in melds
    if face_counts[1] < 3:
        total_score += 100 * face_counts[1]
        contributing_faces[1] += face_counts[1]
    if face_counts[5] < 3:
        total_score += 50 * face_counts[5]
        contributing_faces[5] += face_counts[5]

    # Reject subset if any die did not contribute
    for face, count in face_counts.items():
        if contributing_faces[face] < count:
            return 0

    return total_score


def get_scoring_combinations(roll: List[Tuple[int, Any]]) -> List[Tuple[List[Tuple[int, Any]], int]]:
    """Generate all subsets of dice, score them, and return the valid ones sorted by score descending."""
    results = []
    for r in range(1, len(roll) + 1):
        for subset in combinations(roll, r):
            score = score_combination(list(subset))
            if score > 0:
                results.append((list(subset), score))
    # sort by score descending, then by subset size descending
    results.sort(key=lambda x: (-x[1], -len(x[0])))
    return results
