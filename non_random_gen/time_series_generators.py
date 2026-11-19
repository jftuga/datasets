"""Generators for order-dependent datasets where each value depends on time or on its predecessor.
These exercise the stats tool's sequence features (trendline, lag-1 autocorrelation, EMA,
input order) through seasonality, persistence, trends, and queueing dynamics. Each
generator takes a seeded RNG and a count and returns the formatted output lines."""

import math
import random

from sampling import ar1_series, clamp, format_floats, format_ints, poisson

HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365.25
MINUTES_PER_DAY = 1440


def old_faithful_wait_min(rng: random.Random, n: int) -> list[str]:
    """Geyser waits between eruptions: a two-state Markov chain of short and long waits.

    A short wait is almost always followed by a long one, so the series alternates and
    lag-1 autocorrelation is negative while the histogram is clearly bimodal.

    Args:
        rng: Seeded random number generator.
        n: Number of eruptions.

    Returns:
        Integer waits in minutes, one per line.
    """
    long_wait = rng.random() < 0.68
    values = []
    for _ in range(n):
        values.append(rng.gauss(80.0, 5.9) if long_wait else rng.gauss(54.0, 5.5))
        long_wait = rng.random() < (0.55 if long_wait else 0.95)
    return format_ints(values)


def weekly_flu_cases(rng: random.Random, n: int) -> list[str]:
    """Weekly influenza case counts over several seasons, each with one winter epidemic peak.

    Weeks are counted from July, so each 52-week season peaks around week 30 (late January).
    Peak height and timing vary from season to season.

    Args:
        rng: Seeded random number generator.
        n: Number of weeks.

    Returns:
        Integer case counts, one per line.
    """
    values = []
    peak_height = peak_week = 0.0
    for week in range(n):
        week_of_season = week % 52
        if week_of_season == 0:
            peak_height = rng.lognormvariate(math.log(4000.0), 0.4)
            peak_week = 30.0 + rng.gauss(0.0, 3.0)
        epidemic = peak_height * math.exp(-0.5 * ((week_of_season - peak_week) / 4.5) ** 2)
        values.append(poisson(rng, 150.0 + epidemic))
    return format_ints(values)


def daily_stock_prices(rng: random.Random, n: int) -> list[str]:
    """Daily closing prices following geometric Brownian motion (8% drift, 25% volatility).

    Args:
        rng: Seeded random number generator.
        n: Number of trading days.

    Returns:
        Prices in dollars with two decimals, one per line.
    """
    drift, volatility, dt = 0.08, 0.25, 1.0 / 252.0
    price = 50.0
    values = []
    for _ in range(n):
        values.append(price)
        price *= math.exp((drift - volatility**2 / 2.0) * dt + volatility * math.sqrt(dt) * rng.gauss(0.0, 1.0))
    return format_floats(values, 2)


def fairbanks_daily_temp_f(rng: random.Random, n: int) -> list[str]:
    """Daily mean temperature in a subarctic city: a strong annual cycle plus weather anomalies.

    The seasonal swing is wide (about -8 F in January to 62 F in July), so values spend
    much of their time near the two extremes and the histogram is bimodal.

    Args:
        rng: Seeded random number generator.
        n: Number of days.

    Returns:
        Temperatures in Fahrenheit with one decimal, one per line.
    """
    anomalies = ar1_series(rng, n, 0.75, 8.0)
    seasonal = (27.0 - 35.0 * math.cos(2.0 * math.pi * (day - 10) / DAYS_PER_YEAR) for day in range(n))
    return format_floats((s + a for s, a in zip(seasonal, anomalies, strict=True)), 1)


def rainfall_daily_mm(rng: random.Random, n: int) -> list[str]:
    """Daily rainfall from a wet/dry Markov chain with gamma-distributed wet-day amounts.

    Over half of all days are dry (exactly 0.0), so the median and MAD are both zero.
    Wet days cluster into spells, which gives positive autocorrelation.

    Args:
        rng: Seeded random number generator.
        n: Number of days.

    Returns:
        Rainfall in millimeters with one decimal, one per line.
    """
    wet = False
    values = []
    for _ in range(n):
        values.append(max(0.1, rng.gammavariate(0.75, 9.0)) if wet else 0.0)
        wet = rng.random() < (0.60 if wet else 0.25)
    return format_floats(values, 1)


def call_center_calls_hourly(rng: random.Random, n: int) -> list[str]:
    """Hourly call counts: Poisson arrivals whose rate follows business hours, weekends, and a holiday rush.

    Args:
        rng: Seeded random number generator.
        n: Number of hours.

    Returns:
        Integer call counts, one per line.
    """
    values = []
    for hour in range(n):
        hour_of_day = hour % HOURS_PER_DAY
        day = hour // HOURS_PER_DAY
        daytime = max(0.0, math.sin(math.pi * (hour_of_day - 7) / 13.0))
        rate = 3.0 + 38.0 * daytime**1.5
        if day % 7 >= 5:
            rate *= 0.45
        if day % 365 >= 320:
            rate *= 1.35
        values.append(poisson(rng, rate))
    return format_ints(values)


def wind_speed_mph(rng: random.Random, n: int) -> list[str]:
    """Hourly wind speed as the magnitude of two persistent AR(1) velocity components.

    The magnitude of two independent normal components is Rayleigh distributed (a Weibull
    with shape 2), the standard model for wind speed.

    Args:
        rng: Seeded random number generator.
        n: Number of hours.

    Returns:
        Speeds in miles per hour with one decimal, one per line.
    """
    east = ar1_series(rng, n, 0.97, 8.0)
    north = ar1_series(rng, n, 0.97, 8.0)
    return format_floats((math.hypot(u, v) for u, v in zip(east, north, strict=True)), 1)


def server_cpu_pct(rng: random.Random, n: int) -> list[str]:
    """Per-minute CPU utilization with a business-hours cycle and a nightly batch job at 100%.

    Args:
        rng: Seeded random number generator.
        n: Number of minutes.

    Returns:
        Utilization percentages from 0 to 100 with one decimal, one per line.
    """
    noise = ar1_series(rng, n, 0.95, 4.0)
    values = []
    for minute in range(n):
        minute_of_day = minute % MINUTES_PER_DAY
        if 120 <= minute_of_day < 150:
            values.append(100.0)
            continue
        hour = minute_of_day / 60.0
        business = max(0.0, math.sin(math.pi * (hour - 8.0) / 10.0)) if 8.0 <= hour <= 18.0 else 0.0
        if (minute // MINUTES_PER_DAY) % 7 >= 5:
            business *= 0.35
        values.append(clamp(15.0 + 55.0 * business + noise[minute], 0.0, 100.0))
    return format_floats(values, 1)


def tide_height_ft(rng: random.Random, n: int) -> list[str]:
    """Half-hourly tide heights from the M2 and S2 constituents plus a slow weather surge.

    The two constituents have slightly different periods (12.42 h and 12.00 h), so they
    drift in and out of phase, producing the spring-neap cycle.

    Args:
        rng: Seeded random number generator.
        n: Number of half-hour readings.

    Returns:
        Heights in feet with two decimals, one per line.
    """
    surge = ar1_series(rng, n, 0.98, 0.25)
    values = []
    for i in range(n):
        hours = i * 0.5
        m2 = 2.5 * math.cos(2.0 * math.pi * hours / 12.42)
        s2 = 1.1 * math.cos(2.0 * math.pi * hours / 12.0)
        values.append(4.0 + m2 + s2 + surge[i])
    return format_floats(values, 2)


def queue_wait_s(rng: random.Random, n: int) -> list[str]:
    """Customer waiting times in a single-server queue at 90% utilization (M/M/1).

    Uses Lindley's recursion: the next customer waits for the current customer's wait plus
    service time, minus the gap until they arrive, but never less than zero. About 10% of
    customers do not wait at all.

    Args:
        rng: Seeded random number generator.
        n: Number of customers.

    Returns:
        Waits in seconds with three decimals, one per line.
    """
    wait = 0.0
    values = []
    for _ in range(n):
        values.append(wait)
        wait = max(0.0, wait + rng.expovariate(1.0) - rng.expovariate(0.9))
    return format_floats(values, 3)
