"""Generators for independent draws from real-world distributions with distinctive shapes.
Each dataset here has no meaningful input order; its interest lies in the histogram,
skewness, kurtosis, and outliers: mixtures, power laws, exponential decay, and heavy
tails. Each generator takes a seeded RNG and a count and returns formatted lines."""

import math
import random

from sampling import clamp, format_floats, format_ints, student_t


def adult_height_cm(rng: random.Random, n: int) -> list[str]:
    """Adult heights as an even mixture of male and female normal distributions.

    Args:
        rng: Seeded random number generator.
        n: Number of people.

    Returns:
        Heights in centimeters with one decimal, one per line.
    """
    values = (rng.gauss(175.4, 7.1) if rng.random() < 0.5 else rng.gauss(161.8, 6.6) for _ in range(n))
    return format_floats(values, 1)


def birth_weight_g(rng: random.Random, n: int) -> list[str]:
    """Birth weights: a term-birth normal plus a smaller, lighter preterm component.

    The preterm component stretches the lower tail, giving a left-skewed distribution.

    Args:
        rng: Seeded random number generator.
        n: Number of births.

    Returns:
        Weights in grams, one integer per line.
    """
    values = []
    for _ in range(n):
        weight = rng.gauss(2400.0, 650.0) if rng.random() < 0.08 else rng.gauss(3450.0, 450.0)
        values.append(max(400.0, weight))
    return format_ints(values)


def age_at_death_years(rng: random.Random, n: int) -> list[str]:
    """Ages at death from a Gompertz mortality law plus a small infant-mortality spike.

    Gompertz ages are drawn by inverting the survival function
    S(t) = exp(-(a/b) * (exp(b*t) - 1)), with a=1e-4 and b=0.085, which puts the mode
    near 79. About 0.6% of deaths occur at age 0.

    Args:
        rng: Seeded random number generator.
        n: Number of deaths.

    Returns:
        Integer ages from 0 to 110, one per line.
    """
    a, b = 1e-4, 0.085
    values = []
    for _ in range(n):
        if rng.random() < 0.006:
            values.append(0.0)
            continue
        survival = 1.0 - rng.random()
        values.append(min(110.0, math.log(1.0 - (b / a) * math.log(survival)) / b))
    return format_ints(values)


def radioactive_decay_intervals_s(rng: random.Random, n: int) -> list[str]:
    """Time between Geiger counter clicks: memoryless exponential waits plus the counter's dead time.

    The 100 microsecond dead time keeps every interval positive after rounding, as on a real
    counter, so the file stays valid for ``stats -l``.

    Args:
        rng: Seeded random number generator.
        n: Number of intervals.

    Returns:
        Intervals in seconds with four decimals, one per line.
    """
    return format_floats((0.0001 + rng.expovariate(1.0 / 2.5) for _ in range(n)), 4)


def earthquake_magnitudes(rng: random.Random, n: int) -> list[str]:
    """Earthquake magnitudes following the Gutenberg-Richter law with b-value 1.0.

    Magnitudes above the completeness threshold of 2.5 are exponential with rate
    b * ln(10). Starting at 2.45 makes every 0.1 reporting bin, including 2.5, full width.

    Args:
        rng: Seeded random number generator.
        n: Number of earthquakes.

    Returns:
        Magnitudes with one decimal, one per line.
    """
    rate = 1.0 * math.log(10.0)
    return format_floats((2.45 + rng.expovariate(rate) for _ in range(n)), 1)


def city_populations(rng: random.Random, n: int) -> list[str]:
    """Settlement populations following a Pareto power law (Zipf-like city sizes).

    Args:
        rng: Seeded random number generator.
        n: Number of settlements.

    Returns:
        Integer populations, one per line.
    """
    return format_ints(2500.0 * rng.paretovariate(1.05) for _ in range(n))


def daily_log_returns(rng: random.Random, n: int) -> list[str]:
    """Daily stock log returns with fat tails, drawn from Student's t with 3 degrees of freedom.

    Args:
        rng: Seeded random number generator.
        n: Number of trading days.

    Returns:
        Fractional returns with six decimals, one per line.
    """
    return format_floats((0.0003 + 0.009 * student_t(rng, 3.0) for _ in range(n)), 6)


def transaction_amounts_usd(rng: random.Random, n: int) -> list[str]:
    """Card transaction amounts: lognormal purchases with charm pricing, plus refunds.

    Most purchases snap to a ``.99`` price point, which creates many exact repeats. About
    3% of transactions are refunds and are recorded as negative amounts.

    Args:
        rng: Seeded random number generator.
        n: Number of transactions.

    Returns:
        Dollar amounts with two decimals, one per line.
    """
    values = []
    for _ in range(n):
        amount = max(0.5, rng.lognormvariate(math.log(35.0), 1.0))
        if rng.random() < 0.6:
            amount = math.ceil(amount) - 0.01
        values.append(-amount if rng.random() < 0.03 else amount)
    return format_floats(values, 2)


def file_sizes_bytes(rng: random.Random, n: int) -> list[str]:
    """File sizes on a disk: a very wide lognormal plus a spike at the 4096-byte block size.

    Args:
        rng: Seeded random number generator.
        n: Number of files.

    Returns:
        Integer sizes in bytes, one per line.
    """
    values = []
    for _ in range(n):
        if rng.random() < 0.10:
            values.append(4096.0)
        else:
            values.append(max(1.0, rng.lognormvariate(math.log(8000.0), 2.2)))
    return format_ints(values)


def http_latency_ms(rng: random.Random, n: int) -> list[str]:
    """HTTP request latencies: a fast path, a slow cache-miss path, and client timeouts.

    Timeouts are recorded as exactly 30000 ms, so that value becomes the mode.

    Args:
        rng: Seeded random number generator.
        n: Number of requests.

    Returns:
        Latencies in milliseconds with two decimals, one per line.
    """
    values = []
    for _ in range(n):
        roll = rng.random()
        if roll < 0.005:
            values.append(30000.0)
        elif roll < 0.035:
            values.append(clamp(rng.lognormvariate(math.log(380.0), 0.5), 0.0, 30000.0))
        else:
            values.append(rng.lognormvariate(math.log(42.0), 0.45))
    return format_floats(values, 2)
