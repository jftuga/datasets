"""Distribution samplers and value formatters shared by the dataset generators.
The standard library's random module covers most continuous distributions but has no
Poisson or Student's t sampler, so those are built here from stdlib primitives. The
formatters turn numbers into the text lines that are written to dataset files."""

import math
import random
from collections.abc import Iterable


def poisson(rng: random.Random, lam: float) -> int:
    """Draw a Poisson-distributed count by counting unit-rate arrivals in [0, lam].

    Cost grows linearly with lam, which is fine for the rates used in this project.

    Args:
        rng: Seeded random number generator.
        lam: Expected count (rate); must be non-negative.

    Returns:
        A non-negative integer count.
    """
    count = 0
    elapsed = rng.expovariate(1.0)
    while elapsed <= lam:
        count += 1
        elapsed += rng.expovariate(1.0)
    return count


def student_t(rng: random.Random, df: float) -> float:
    """Draw from Student's t distribution as a normal divided by a scaled chi-square root.

    Args:
        rng: Seeded random number generator.
        df: Degrees of freedom; lower values give heavier tails.

    Returns:
        A t-distributed float centered on zero.
    """
    chi_square = rng.gammavariate(df / 2.0, 2.0)
    return rng.gauss(0.0, 1.0) / math.sqrt(chi_square / df)


def ar1_series(rng: random.Random, n: int, phi: float, sd: float) -> list[float]:
    """Generate a zero-mean stationary AR(1) series, where each value partly remembers the last.

    Each step is ``x[t] = phi * x[t-1] + e[t]``. The innovation variance is chosen so the
    marginal standard deviation equals ``sd`` regardless of ``phi``.

    Args:
        rng: Seeded random number generator.
        n: Number of values.
        phi: Persistence in (-1, 1); values near 1 give slow, smooth wandering.
        sd: Marginal standard deviation of the series.

    Returns:
        A list of n floats.
    """
    innovation_sd = sd * math.sqrt(1.0 - phi * phi)
    value = rng.gauss(0.0, sd)
    series = []
    for _ in range(n):
        series.append(value)
        value = phi * value + rng.gauss(0.0, innovation_sd)
    return series


def clamp(value: float, low: float, high: float) -> float:
    """Limit a value to the closed interval [low, high].

    Args:
        value: The number to limit.
        low: Lower bound.
        high: Upper bound.

    Returns:
        The value, moved onto the nearest bound if it lies outside the interval.
    """
    return max(low, min(high, value))


def format_floats(values: Iterable[float], decimals: int) -> list[str]:
    """Format floats with a fixed number of decimals, normalizing negative zero.

    Without normalization, tiny negative values would print as ``-0.00``, which breaks
    exact mirror pairs in symmetric datasets.

    Args:
        values: Numbers to format.
        decimals: Digits after the decimal point.

    Returns:
        One formatted string per input value.
    """
    lines = []
    for value in values:
        rounded = round(value, decimals)
        if rounded == 0:
            rounded = 0.0
        lines.append(f"{rounded:.{decimals}f}")
    return lines


def format_ints(values: Iterable[float]) -> list[str]:
    """Round numbers to the nearest integer and format them.

    Args:
        values: Numbers to format.

    Returns:
        One integer string per input value.
    """
    return [str(round(value)) for value in values]
