# non-random datasets

Simulated "real-world" datasets for exploring [go-stats-calculator](https://github.com/jftuga/go-stats-calculator). Unlike the uniform and power-skewed files in the sibling [`random/`](../random/) folder, each file here simulates a real process: queueing, seasonality, mixtures, power laws, discrete counts, capped measurements, and flaky sensors. Each one produces a distinctive statistical shape, including order-dependent shapes that only the trendline, autocorrelation, EMA, and input-order lines can reveal.

Files hold one number per line. The exception is `sensor_temp_log_c.txt`, which deliberately includes a header, `ERR` and `NaN` lines, and blank lines.

## Regenerating

Run from the repository root (the parent of this folder):

```bash
python3.14 non_random_gen/generate_non_random.py              # all files plus this README
python3.14 non_random_gen/generate_non_random.py --list       # show the catalog
python3.14 non_random_gen/generate_non_random.py --only queue_wait_s tide_height_ft
```

Output is reproducible: every dataset uses its own seed, derived from the base seed and the dataset name, so regenerating one file with `--only` gives the same bytes as a full run. Byte-identical output is guaranteed only on the same Python version, because `random`'s sampling algorithms can change between releases. The `--only` flag leaves this README untouched. This README was generated with base seed `1`.

## Datasets

| File | Count | Real-world process | Expected shape |
|------|------:|--------------------|----------------|
| `flat_rate_shipping_usd.txt` | 20 | Shipping charge on each order under a flat-rate policy. | Every value is 4.99, but the float mean is 4.989999999999999, so stats v1.14.0 and v1.15.0 see a tiny nonzero variance and report noise for skewness, kurtosis, CV, and autocorrelation. |
| `pressure_gauge_masking_psi.txt` | 14 | Tire pressures near 32 psi, plus two readings from a faulty gauge. | Two adjacent high outliers mask each other: missed by -z 2.5, caught by IQR and Mod Z; the cluster is so tight that one low reading may be flagged too. |
| `weekly_flu_cases.txt` | 260 | Weekly influenza cases over five July-to-June seasons. | Long quiet baseline with one sharp winter peak per season; right skew, periodic trendline. |
| `old_faithful_wait_min.txt` | 272 | Minutes between geyser eruptions; short waits are followed by long ones. | Bimodal (about 54 and 80 minutes) with negative lag-1 autocorrelation. |
| `cumulative_downloads.txt` | 365 | Running total of app downloads, with daily downloads growing exponentially. | Non-decreasing: input order ascending, trendline and autocorrelation describe the sort. |
| `goals_per_match.txt` | 380 | Total goals in each match of a 380-match league season. | Small Poisson counts (mean about 2.75): mode 2 or 3, right skew, very few distinct values. |
| `exam_scores.txt` | 400 | Exam scores for a large course, capped at 100. | Normal body with excess mass piled at 100 (the mode): ceiling effect and left skew. |
| `leaderboard_scores_sorted.txt` | 500 | Game leaderboard exported best-first; score decays as a power of rank. | Descending input order, extreme right skew, outliers at the top ranks. |
| `likert_ratings.txt` | 1,500 | Product review star ratings from 1 to 5. | J-shaped: mode 5 holds over half the data (MAD 0), secondary bump at 1, few middling ratings. |
| `ac_mains_voltage.txt` | 2,000 | 120 V RMS, 60 Hz mains waveform sampled at 4 kHz. | Exactly symmetric about 0 V; U-shaped arcsine histogram, kurtosis near -1.5, CV N/A. |
| `daily_stock_prices.txt` | 2,520 | Ten years of daily closing prices (geometric Brownian motion). | Wandering trend with lag-1 autocorrelation near 1; EMA diverges from the mean. |
| `daily_log_returns.txt` | 2,520 | Ten years of daily stock log returns with fat tails (Student's t, 3 df). | Mean near zero makes CV huge and meaningless; large excess kurtosis, many z-score outliers, tiny magnitudes. |
| `dice_2d6_sums.txt` | 3,600 | Sums of two six-sided dice. | Discrete triangular distribution: mode 7, nearly symmetric, kurtosis about -0.6 (mesokurtic by stats' thresholds). |
| `fairbanks_daily_temp_f.txt` | 3,650 | Ten years of daily mean temperature in a subarctic city. | Strong annual cycle: bimodal histogram, negative winter values, high autocorrelation; use -b 40 to see the cycle in the trendline. |
| `rainfall_daily_mm.txt` | 3,650 | Ten years of daily rainfall; wet and dry days come in spells. | Over half the days are exactly 0: median 0, MAD 0, geometric mean suppressed, heavy tail. |
| `city_populations.txt` | 5,000 | Populations of settlements in a region (Pareto power law). | Spans several orders of magnitude; mean far above median; ideal for -l. |
| `radioactive_decay_intervals_s.txt` | 7,500 | Seconds between Geiger counter clicks. | Exponential with a 100 microsecond dead time: skewness near 2, excess kurtosis around 6 (sample estimates vary from about 4 to 7), CV near 100%. |
| `call_center_calls_hourly.txt` | 8,760 | Calls per hour for a year: business hours, quiet weekends, holiday rush. | Quiet overnight hours dominate (low mode) with a long daytime tail; strong daily periodicity; late-year trendline lift. |
| `wind_speed_mph.txt` | 8,760 | Hourly wind speed for a year (Rayleigh, persistent weather). | Moderate right skew, bounded at 0, high autocorrelation. |
| `server_cpu_pct.txt` | 10,080 | Per-minute CPU utilization for one week, with a nightly batch job. | Daily cycle, quieter weekend, right skew, and a pile-up at exactly 100 that becomes the mode. |
| `birth_weight_g.txt` | 15,000 | Birth weights: term births plus a lighter preterm group. | Left skew from the preterm tail; IQR outliers are mostly low, with a few high ones from the term-birth tail. |
| `tide_height_ft.txt` | 17,520 | Half-hourly tide heights for a year (M2 + S2 constituents, weather surge). | Broad high/low-water histogram, platykurtic, autocorrelation near 1; tidal cycles are too fast for the trendline to resolve. |
| `adult_height_cm.txt` | 20,000 | Adult heights from an even mix of men and women. | Mixture of two normals: broad, unimodal, skew near 0, kurtosis about -0.5 (mesokurtic by stats' thresholds). |
| `age_at_death_years.txt` | 30,000 | Age at death (Gompertz mortality) with a small infant-mortality spike. | Strong left skew with a broad mode around 80; a small cluster of 0s blocks -l. |
| `queue_wait_s.txt` | 40,000 | Customer waits in a single-server queue at 90% utilization. | About 10% exact zeros (mode 0), long tail, autocorrelation near 1, congestion waves. |
| `earthquake_magnitudes.txt` | 50,000 | Earthquake magnitudes above 2.5 (Gutenberg-Richter, b = 1). | Exponential decay from the cutoff; one-decimal values give a true mode of 2.5. |
| `sensor_temp_log_c.txt` | 86,400 | One day of 1 Hz room temperature from a flaky logger (header, ERR, NaN, blanks). | Malformed lines trigger the Skipped count; smooth daily cycle; autocorrelation near 1. |
| `transaction_amounts_usd.txt` | 100,000 | Card transactions with .99 charm pricing and about 3% refunds. | Heavy right tail, negative refunds (blocks -l), many exact repeats at .99 price points. |
| `file_sizes_bytes.txt` | 250,000 | Sizes of files on a disk, with many 4096-byte block-sized files. | Spans 1 B to hundreds of MB; mode 4096; histogram is a single spike until -l reveals a lognormal hump. |
| `http_latency_ms.txt` | 1,000,000 | HTTP request latencies: fast path, cache misses, and 30 s client timeouts. | Lognormal body; a 3% slow path lifts p99 far above the median; the timeout spike at 30000 is the mode. |

## Feature index

Which files to try when you want to see a particular property or `stats` behavior.

| Feature | Files |
|---------|-------|
| heavy right tail | `weekly_flu_cases`, `leaderboard_scores_sorted`, `rainfall_daily_mm`, `city_populations`, `radioactive_decay_intervals_s`, `queue_wait_s`, `earthquake_magnitudes`, `transaction_amounts_usd`, `file_sizes_bytes`, `http_latency_ms` |
| strictly positive, spans orders of magnitude (try -l) | `weekly_flu_cases`, `leaderboard_scores_sorted`, `city_populations`, `radioactive_decay_intervals_s`, `file_sizes_bytes`, `http_latency_ms` |
| left skew | `exam_scores`, `likert_ratings`, `birth_weight_g`, `age_at_death_years` |
| near-normal reference (mesokurtic) | `dice_2d6_sums`, `adult_height_cm` |
| multimodal histogram | `old_faithful_wait_min`, `likert_ratings`, `ac_mains_voltage`, `fairbanks_daily_temp_f` |
| platykurtic (thin tails) | `ac_mains_voltage`, `fairbanks_daily_temp_f`, `tide_height_ft` |
| leptokurtic (heavy tails) | `pressure_gauge_masking_psi`, `leaderboard_scores_sorted`, `daily_log_returns`, `rainfall_daily_mm`, `city_populations`, `radioactive_decay_intervals_s`, `birth_weight_g`, `age_at_death_years`, `queue_wait_s`, `earthquake_magnitudes`, `transaction_amounts_usd`, `file_sizes_bytes`, `http_latency_ms` |
| discrete values / true mode | `flat_rate_shipping_usd`, `old_faithful_wait_min`, `goals_per_match`, `exam_scores`, `likert_ratings`, `dice_2d6_sums`, `call_center_calls_hourly`, `age_at_death_years`, `earthquake_magnitudes`, `transaction_amounts_usd`, `file_sizes_bytes` |
| pile-up at a cap or floor | `exam_scores`, `rainfall_daily_mm`, `server_cpu_pct`, `queue_wait_s`, `http_latency_ms` |
| positive autocorrelation | `weekly_flu_cases`, `cumulative_downloads`, `ac_mains_voltage`, `daily_stock_prices`, `fairbanks_daily_temp_f`, `rainfall_daily_mm`, `call_center_calls_hourly`, `wind_speed_mph`, `server_cpu_pct`, `tide_height_ft`, `queue_wait_s`, `sensor_temp_log_c` |
| negative autocorrelation | `old_faithful_wait_min` |
| trend or seasonality (trendline, -e) | `weekly_flu_cases`, `cumulative_downloads`, `daily_stock_prices`, `fairbanks_daily_temp_f`, `call_center_calls_hourly`, `server_cpu_pct`, `queue_wait_s`, `sensor_temp_log_c` |
| pre-sorted input order | `cumulative_downloads`, `leaderboard_scores_sorted` |
| exact symmetry | `ac_mains_voltage` |
| z-score masking (try -z 2.5) | `pressure_gauge_masking_psi` |
| MAD is zero | `likert_ratings`, `rainfall_daily_mm` |
| zero variance | `flat_rate_shipping_usd` |
| malformed lines (Skipped) | `sensor_temp_log_c` |
| negative values | `ac_mains_voltage`, `daily_log_returns`, `fairbanks_daily_temp_f`, `transaction_amounts_usd` |
| small magnitudes | `daily_log_returns` |

## Notes

- The numeric claims (modes, MAD, kurtosis thresholds, symmetry, masking, input order, autocorrelation sign, and `-l` acceptance) were checked against `stats -j` output for base seeds 1 through 16. Histogram and trendline descriptions (bimodality, bumps, cycles, spikes) were checked visually for the default seed only. Exact numbers, such as the count of `ERR` lines, vary with the seed.
- Count is the number of values requested. For `sensor_temp_log_c.txt` it is the number of reading lines, about 210 of which are `ERR` or `NaN`; the file also has one header line and three blank lines, so `stats` reports roughly 86,190 values and 211 skipped lines.
- `stats -l` rejects any file containing a zero or negative value, and many files here do. Every file tagged "try -l" in the feature index is strictly positive.
