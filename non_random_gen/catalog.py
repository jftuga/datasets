"""The catalog of every non-random dataset, ordered by row count from smallest to largest.
Each entry pairs a generator with its file name, size, real-world story, expected
statistical shape, and feature tags. Adding a dataset means writing a generator and
appending one DatasetSpec here; the CLI and README pick it up automatically."""

import discrete_generators as discrete
import distribution_generators as dist
import edge_case_generators as edge
import time_series_generators as series
from dataset_spec import DatasetSpec
from dataset_spec import Feature as F

CATALOG: tuple[DatasetSpec, ...] = (
    DatasetSpec(
        "flat_rate_shipping_usd", 20,
        "Shipping charge on each order under a flat-rate policy.",
        "Every value is 4.99, but the float mean is 4.989999999999999, so stats v1.14.0 and v1.15.0 see a tiny nonzero variance and report noise for skewness, kurtosis, CV, and autocorrelation.",
        (F.ZERO_VARIANCE, F.DISCRETE), edge.flat_rate_shipping_usd,
    ),
    DatasetSpec(
        "pressure_gauge_masking_psi", 14,
        "Tire pressures near 32 psi, plus two readings from a faulty gauge.",
        "Two adjacent high outliers mask each other: missed by -z 2.5, caught by IQR and Mod Z; the cluster is so tight that one low reading may be flagged too.",
        (F.MASKING, F.LEPTOKURTIC), edge.pressure_gauge_masking_psi,
    ),
    DatasetSpec(
        "weekly_flu_cases", 260,
        "Weekly influenza cases over five July-to-June seasons.",
        "Long quiet baseline with one sharp winter peak per season; right skew, periodic trendline.",
        (F.TREND, F.POS_AUTOCORR, F.HEAVY_TAIL, F.LOG_SCALE), series.weekly_flu_cases,
    ),
    DatasetSpec(
        "old_faithful_wait_min", 272,
        "Minutes between geyser eruptions; short waits are followed by long ones.",
        "Bimodal (about 54 and 80 minutes) with negative lag-1 autocorrelation.",
        (F.MULTIMODAL, F.NEG_AUTOCORR, F.DISCRETE), series.old_faithful_wait_min,
    ),
    DatasetSpec(
        "cumulative_downloads", 365,
        "Running total of app downloads, with daily downloads growing exponentially.",
        "Non-decreasing: input order ascending, trendline and autocorrelation describe the sort.",
        (F.SORTED, F.TREND, F.POS_AUTOCORR), edge.cumulative_downloads,
    ),
    DatasetSpec(
        "goals_per_match", 380,
        "Total goals in each match of a 380-match league season.",
        "Small Poisson counts (mean about 2.75): mode 2 or 3, right skew, very few distinct values.",
        (F.DISCRETE,), discrete.goals_per_match,
    ),
    DatasetSpec(
        "exam_scores", 400,
        "Exam scores for a large course, capped at 100.",
        "Normal body with excess mass piled at 100 (the mode): ceiling effect and left skew.",
        (F.CEILING, F.LEFT_SKEW, F.DISCRETE), discrete.exam_scores,
    ),
    DatasetSpec(
        "leaderboard_scores_sorted", 500,
        "Game leaderboard exported best-first; score decays as a power of rank.",
        "Descending input order, extreme right skew, outliers at the top ranks.",
        (F.SORTED, F.HEAVY_TAIL, F.LEPTOKURTIC, F.LOG_SCALE), edge.leaderboard_scores_sorted,
    ),
    DatasetSpec(
        "likert_ratings", 1500,
        "Product review star ratings from 1 to 5.",
        "J-shaped: mode 5 holds over half the data (MAD 0), secondary bump at 1, few middling ratings.",
        (F.DISCRETE, F.MULTIMODAL, F.LEFT_SKEW, F.MAD_ZERO), discrete.likert_ratings,
    ),
    DatasetSpec(
        "ac_mains_voltage", 2000,
        "120 V RMS, 60 Hz mains waveform sampled at 4 kHz.",
        "Exactly symmetric about 0 V; U-shaped arcsine histogram, kurtosis near -1.5, CV N/A.",
        (F.SYMMETRY, F.PLATYKURTIC, F.MULTIMODAL, F.NEGATIVE, F.POS_AUTOCORR), edge.ac_mains_voltage,
    ),
    DatasetSpec(
        "daily_stock_prices", 2520,
        "Ten years of daily closing prices (geometric Brownian motion).",
        "Wandering trend with lag-1 autocorrelation near 1; EMA diverges from the mean.",
        (F.TREND, F.POS_AUTOCORR), series.daily_stock_prices,
    ),
    DatasetSpec(
        "daily_log_returns", 2520,
        "Ten years of daily stock log returns with fat tails (Student's t, 3 df).",
        "Mean near zero makes CV huge and meaningless; large excess kurtosis, many z-score outliers, tiny magnitudes.",
        (F.LEPTOKURTIC, F.NEGATIVE, F.SMALL_MAGNITUDE), dist.daily_log_returns,
    ),
    DatasetSpec(
        "dice_2d6_sums", 3600,
        "Sums of two six-sided dice.",
        "Discrete triangular distribution: mode 7, nearly symmetric, kurtosis about -0.6 (mesokurtic by stats' thresholds).",
        (F.DISCRETE, F.NEAR_NORMAL), discrete.dice_2d6_sums,
    ),
    DatasetSpec(
        "fairbanks_daily_temp_f", 3650,
        "Ten years of daily mean temperature in a subarctic city.",
        "Strong annual cycle: bimodal histogram, negative winter values, high autocorrelation; use -b 40 to see the cycle in the trendline.",
        (F.TREND, F.MULTIMODAL, F.NEGATIVE, F.POS_AUTOCORR, F.PLATYKURTIC), series.fairbanks_daily_temp_f,
    ),
    DatasetSpec(
        "rainfall_daily_mm", 3650,
        "Ten years of daily rainfall; wet and dry days come in spells.",
        "Over half the days are exactly 0: median 0, MAD 0, geometric mean suppressed, heavy tail.",
        (F.MAD_ZERO, F.CEILING, F.HEAVY_TAIL, F.LEPTOKURTIC, F.POS_AUTOCORR), series.rainfall_daily_mm,
    ),
    DatasetSpec(
        "city_populations", 5000,
        "Populations of settlements in a region (Pareto power law).",
        "Spans several orders of magnitude; mean far above median; ideal for -l.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.LOG_SCALE), dist.city_populations,
    ),
    DatasetSpec(
        "radioactive_decay_intervals_s", 7500,
        "Seconds between Geiger counter clicks.",
        "Exponential with a 100 microsecond dead time: skewness near 2, excess kurtosis around 6 (sample estimates vary from about 4 to 7), CV near 100%.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.LOG_SCALE), dist.radioactive_decay_intervals_s,
    ),
    DatasetSpec(
        "call_center_calls_hourly", 8760,
        "Calls per hour for a year: business hours, quiet weekends, holiday rush.",
        "Quiet overnight hours dominate (low mode) with a long daytime tail; strong daily periodicity; late-year trendline lift.",
        (F.DISCRETE, F.TREND, F.POS_AUTOCORR), series.call_center_calls_hourly,
    ),
    DatasetSpec(
        "wind_speed_mph", 8760,
        "Hourly wind speed for a year (Rayleigh, persistent weather).",
        "Moderate right skew, bounded at 0, high autocorrelation.",
        (F.POS_AUTOCORR,), series.wind_speed_mph,
    ),
    DatasetSpec(
        "server_cpu_pct", 10080,
        "Per-minute CPU utilization for one week, with a nightly batch job.",
        "Daily cycle, quieter weekend, right skew, and a pile-up at exactly 100 that becomes the mode.",
        (F.CEILING, F.TREND, F.POS_AUTOCORR), series.server_cpu_pct,
    ),
    DatasetSpec(
        "birth_weight_g", 15000,
        "Birth weights: term births plus a lighter preterm group.",
        "Left skew from the preterm tail; IQR outliers are mostly low, with a few high ones from the term-birth tail.",
        (F.LEFT_SKEW, F.LEPTOKURTIC), dist.birth_weight_g,
    ),
    DatasetSpec(
        "tide_height_ft", 17520,
        "Half-hourly tide heights for a year (M2 + S2 constituents, weather surge).",
        "Broad high/low-water histogram, platykurtic, autocorrelation near 1; tidal cycles are too fast for the trendline to resolve.",
        (F.PLATYKURTIC, F.POS_AUTOCORR), series.tide_height_ft,
    ),
    DatasetSpec(
        "adult_height_cm", 20000,
        "Adult heights from an even mix of men and women.",
        "Mixture of two normals: broad, unimodal, skew near 0, kurtosis about -0.5 (mesokurtic by stats' thresholds).",
        (F.NEAR_NORMAL,), dist.adult_height_cm,
    ),
    DatasetSpec(
        "age_at_death_years", 30000,
        "Age at death (Gompertz mortality) with a small infant-mortality spike.",
        "Strong left skew with a broad mode around 80; a small cluster of 0s blocks -l.",
        (F.LEFT_SKEW, F.LEPTOKURTIC, F.DISCRETE), dist.age_at_death_years,
    ),
    DatasetSpec(
        "queue_wait_s", 40000,
        "Customer waits in a single-server queue at 90% utilization.",
        "About 10% exact zeros (mode 0), long tail, autocorrelation near 1, congestion waves.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.CEILING, F.POS_AUTOCORR, F.TREND), series.queue_wait_s,
    ),
    DatasetSpec(
        "earthquake_magnitudes", 50000,
        "Earthquake magnitudes above 2.5 (Gutenberg-Richter, b = 1).",
        "Exponential decay from the cutoff; one-decimal values give a true mode of 2.5.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.DISCRETE), dist.earthquake_magnitudes,
    ),
    DatasetSpec(
        "sensor_temp_log_c", 86400,
        "One day of 1 Hz room temperature from a flaky logger (header, ERR, NaN, blanks).",
        "Malformed lines trigger the Skipped count; smooth daily cycle; autocorrelation near 1.",
        (F.SKIPPED, F.POS_AUTOCORR, F.TREND), edge.sensor_temp_log_c,
    ),
    DatasetSpec(
        "transaction_amounts_usd", 100000,
        "Card transactions with .99 charm pricing and about 3% refunds.",
        "Heavy right tail, negative refunds (blocks -l), many exact repeats at .99 price points.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.NEGATIVE, F.DISCRETE), dist.transaction_amounts_usd,
    ),
    DatasetSpec(
        "file_sizes_bytes", 250000,
        "Sizes of files on a disk, with many 4096-byte block-sized files.",
        "Spans 1 B to hundreds of MB; mode 4096; histogram is a single spike until -l reveals a lognormal hump.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.DISCRETE, F.LOG_SCALE), dist.file_sizes_bytes,
    ),
    DatasetSpec(
        "http_latency_ms", 1000000,
        "HTTP request latencies: fast path, cache misses, and 30 s client timeouts.",
        "Lognormal body; a 3% slow path lifts p99 far above the median; the timeout spike at 30000 is the mode.",
        (F.HEAVY_TAIL, F.LEPTOKURTIC, F.CEILING, F.LOG_SCALE), dist.http_latency_ms,
    ),
)
