"""Generators for real-world datasets built to hit specific stats-tool edge cases.
Each dataset still follows a plausible real-world story, but is shaped to trigger
zero variance, z-score masking, sorted-input warnings, exact symmetry, or skipped
malformed lines. Each generator takes a seeded RNG and a count and returns output lines."""

import math
import random

from sampling import ar1_series, format_floats, format_ints, poisson

AC_SAMPLE_RATE_HZ = 4000
AC_LINE_HZ = 60
AC_PEAK_VOLTS = 169.71
AC_SAMPLES_PER_PHASE_CYCLE = 200


def flat_rate_shipping_usd(rng: random.Random, n: int) -> list[str]:
    """Shipping charges on orders under a flat-rate policy, so every value is identical.

    Args:
        rng: Unused; accepted to match the generator signature.
        n: Number of orders.

    Returns:
        The same dollar amount on every line.
    """
    return ["4.99"] * n


def pressure_gauge_masking_psi(rng: random.Random, n: int) -> list[str]:
    """Tire pressure readings that cluster tightly, plus two readings from a faulty gauge.

    The two high readings inflate the mean and standard deviation enough that neither
    exceeds a classic z-score of 2.5. Modified z-scores and the IQR method still flag them.

    Args:
        rng: Seeded random number generator.
        n: Total number of readings, including the two faulty ones.

    Returns:
        Pressures in psi with one decimal, one per line, in shuffled order.
    """
    values = [rng.gauss(32.0, 0.4) for _ in range(n - 2)] + [58.0, 59.5]
    rng.shuffle(values)
    return format_floats(values, 1)


def leaderboard_scores_sorted(rng: random.Random, n: int) -> list[str]:
    """Game leaderboard scores following a power-law decay by rank, exported best-first.

    Args:
        rng: Seeded random number generator.
        n: Number of players.

    Returns:
        Integer scores in descending order, one per line.
    """
    scores = [100000.0 * rank**-0.8 * rng.lognormvariate(0.0, 0.05) for rank in range(1, n + 1)]
    return format_ints(sorted(scores, reverse=True))


def cumulative_downloads(rng: random.Random, n: int) -> list[str]:
    """Running total of app downloads, where daily downloads grow exponentially.

    Args:
        rng: Seeded random number generator.
        n: Number of days.

    Returns:
        Integer cumulative totals in ascending order, one per line.
    """
    total = 0
    values = []
    for day in range(n):
        total += poisson(rng, 40.0 * math.exp(0.008 * day))
        values.append(total)
    return format_ints(values)


def ac_mains_voltage(rng: random.Random, n: int) -> list[str]:
    """Samples of an ideal 120 V RMS, 60 Hz mains waveform taken at 4 kHz.

    Every sample has an exact mirror partner across 0 V, so the dataset is perfectly
    symmetric. The sine shape gives a U-shaped histogram with an arcsine distribution.
    Negative half-cycle samples are computed by negating their positive partner, so the
    mirror pairs match exactly once rounded.

    Args:
        rng: Unused; accepted to match the generator signature.
        n: Number of samples; must be a multiple of 200 for exact symmetry.

    Returns:
        Voltages with two decimals, one per line.

    Raises:
        ValueError: If n is not a multiple of 200.
    """
    if n % AC_SAMPLES_PER_PHASE_CYCLE != 0:
        raise ValueError(f"ac_mains_voltage count must be a multiple of {AC_SAMPLES_PER_PHASE_CYCLE}, got {n}")
    half = AC_SAMPLE_RATE_HZ // 2
    values = []
    for k in range(n):
        phase = (k * AC_LINE_HZ) % AC_SAMPLE_RATE_HZ
        mirrored = phase > half
        base = AC_SAMPLE_RATE_HZ - phase if mirrored else phase
        volts = AC_PEAK_VOLTS * math.sin(2.0 * math.pi * base / AC_SAMPLE_RATE_HZ)
        values.append(-volts if mirrored else volts)
    return format_floats(values, 2)


def sensor_temp_log_c(rng: random.Random, n: int) -> list[str]:
    """One day of 1 Hz room-temperature readings from a flaky sensor logger.

    The log starts with a header line, contains scattered ``ERR`` lines, a two-minute
    ``NaN`` dropout, and a few blank lines. Readings combine a daily HVAC cycle, slow
    drift, and quantization noise.

    Args:
        rng: Seeded random number generator.
        n: Number of reading lines, malformed ones included; header and blanks are extra.

    Returns:
        Log lines: a header, readings with three decimals, malformed entries, and blanks.
    """
    drift = ar1_series(rng, n, 0.9995, 0.6)
    readings = []
    for second in range(n):
        cycle = 1.5 * math.sin(2.0 * math.pi * second / 86400.0 - math.pi / 2.0)
        readings.append(21.0 + cycle + drift[second] + rng.gauss(0.0, 0.02))
    lines = format_floats(readings, 3)
    for i in range(n):
        if rng.random() < 0.001:
            lines[i] = "ERR"
    dropout_start = rng.randrange(n - 120)
    lines[dropout_start : dropout_start + 120] = ["NaN"] * 120
    for _ in range(3):
        lines.insert(rng.randrange(len(lines)), "")
    return ["temp_c", *lines]
