"""Generators for independent, discrete-valued datasets: games, ratings, and test scores.
These datasets have few distinct values, so the stats tool reports a true mode and a high
duplicate percentage instead of a modal bin. Each generator takes a seeded RNG and a
count and returns the formatted output lines."""

import random

from sampling import clamp, format_ints, poisson

LIKERT_WEIGHTS: tuple[float, ...] = (0.18, 0.04, 0.06, 0.17, 0.55)


def goals_per_match(rng: random.Random, n: int) -> list[str]:
    """Total goals in soccer matches, modeled as two independent Poisson team scores.

    Args:
        rng: Seeded random number generator.
        n: Number of matches.

    Returns:
        Integer goal totals, one per line.
    """
    return [str(poisson(rng, 1.55) + poisson(rng, 1.20)) for _ in range(n)]


def dice_2d6_sums(rng: random.Random, n: int) -> list[str]:
    """Sums of two six-sided dice, giving a discrete triangular distribution peaking at 7.

    Args:
        rng: Seeded random number generator.
        n: Number of rolls.

    Returns:
        Integer sums from 2 to 12, one per line.
    """
    return [str(rng.randint(1, 6) + rng.randint(1, 6)) for _ in range(n)]


def likert_ratings(rng: random.Random, n: int) -> list[str]:
    """Product review star ratings with the J-shaped profile typical of online reviews.

    Args:
        rng: Seeded random number generator.
        n: Number of reviews.

    Returns:
        Integer ratings from 1 to 5, one per line.
    """
    return [str(r) for r in rng.choices(range(1, 6), weights=LIKERT_WEIGHTS, k=n)]


def exam_scores(rng: random.Random, n: int) -> list[str]:
    """Exam scores from a normal ability distribution, capped at 0 and 100.

    The cap piles excess mass onto 100, creating a ceiling effect and a left skew.

    Args:
        rng: Seeded random number generator.
        n: Number of students.

    Returns:
        Integer scores from 0 to 100, one per line.
    """
    return format_ints(clamp(rng.gauss(82.0, 15.0), 0.0, 100.0) for _ in range(n))
