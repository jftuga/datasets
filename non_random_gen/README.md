# non_random_gen

A generator for simulated "real-world" datasets used to exercise [go-stats-calculator](https://github.com/jftuga/go-stats-calculator). It writes 30 files, one number per line, into `../non-random/`, along with a `README.md` there that catalogs each dataset and indexes them by statistical feature.

The random files in `../random/` are uniform or power-skewed draws from [randrange](https://github.com/jftuga/randrange). This generator instead simulates real processes, such as queues, tides, seasonal weather, mixtures, power laws, capped scores, and a flaky sensor log. That produces shapes the random files cannot: multimodal histograms, left skew, ceiling pile-ups, true discrete modes, positive and negative autocorrelation, trends, pre-sorted input, exact symmetry, z-score masking, zero MAD, and malformed lines.

## Requirements

- Python 3.14
- Standard library only; no third-party packages

## Usage

Run from the repository root:

```bash
python3.14 non_random_gen/generate_non_random.py                 # all datasets plus ../non-random/README.md
python3.14 non_random_gen/generate_non_random.py --list          # print the catalog
python3.14 non_random_gen/generate_non_random.py --only queue_wait_s tide_height_ft
python3.14 non_random_gen/generate_non_random.py --seed 7        # a different, still reproducible, variant
```

| Option | Meaning |
|--------|---------|
| `--seed N` | Base seed for every dataset (default `1`). |
| `--only NAME ...` | Generate only the named datasets. Unknown names are rejected. The data README is left untouched. |
| `--list` | Print each dataset's name, count, and process, then exit. |

A full run takes about one second and writes about 9.3 MB.

## Reproducibility

Each dataset gets its own `random.Random`, seeded with `base_seed * 2**32 + crc32(name)`. CRC32 is used instead of `hash()` because string hashing is randomized per process. As a result:

- Regenerating one file with `--only` produces the same bytes as a full run.
- Adding, removing, or reordering datasets does not change the others.
- Output is byte-identical only on the same Python version, since `random`'s sampling algorithms may change between releases.

## Files

| File | Responsibility |
|------|----------------|
| `dataset_spec.py` | `DatasetSpec` record (name, count, process, shape, features, generator) and the `Feature` tag vocabulary. |
| `sampling.py` | Samplers missing from the stdlib (Poisson, Student's t, stationary AR(1)), `clamp`, and number formatters. |
| `discrete_generators.py` | Independent discrete data: goals, dice, star ratings, exam scores. |
| `distribution_generators.py` | Independent draws with distinctive shapes: mixtures, Gompertz, exponential, Gutenberg-Richter, Pareto, Student's t, lognormal mixtures. |
| `time_series_generators.py` | Order-dependent data: Markov chains, seasonality, geometric Brownian motion, non-homogeneous Poisson, tides, the Lindley queue recursion. |
| `edge_case_generators.py` | Real-world stories built to trigger specific `stats` behaviors: zero variance, masking, sorted input, exact symmetry, skipped lines. |
| `catalog.py` | The ordered tuple of all 30 `DatasetSpec` entries. |
| `readme_writer.py` | Renders `../non-random/README.md` from the catalog. |
| `generate_non_random.py` | The argparse CLI entry point. |

Every generator has the same signature, `(rng: random.Random, n: int) -> list[str]`, and returns finished output lines. Returning strings rather than floats lets edge-case generators emit malformed lines, and keeps formatting decisions (decimals, negative-zero normalization) with the data they describe.

## Adding a dataset

1. Write a generator with the standard signature in the module that fits its kind.
2. Append a `DatasetSpec` to `CATALOG` in `catalog.py` with its name, count, process, expected shape, and feature tags.
3. Run a full generation. The CLI, `--list`, and the data README pick it up automatically.
4. Run `stats` on the new file and confirm every claim in the shape text and every feature tag. Then try a few other `--seed` values, because claims that rest on a narrow margin, such as which of two adjacent values is the mode, can flip.

## How the claims were verified

The shape descriptions and feature tags were not taken on faith. A throwaway script (not part of this folder) regenerated every dataset under base seeds 1 through 16. For each seed it checked 38 numeric claims against `stats -j` output, plus `stats -l` acceptance of the six files tagged for log scale. The numeric claims cover modes, MAD of zero, kurtosis thresholds and ranges, symmetry, masking behavior, outlier direction, percentile ratios, input order, and autocorrelation. Histogram and trendline descriptions, and the multimodal and trend tags, cannot be checked that way. They were checked by eye against the glyph output for the default seed only. Claims that held for some seeds but not others were either reworded or fixed in the generator. One example: radioactive decay intervals could round to `0.0000` and break `-l`, so a 100 microsecond counter dead time was added.

Kurtosis tags follow the thresholds `stats` uses: platykurtic below -1, leptokurtic above 1. Dice sums and adult heights have negative excess kurtosis (about -0.6 and -0.5), but `stats` labels them mesokurtic. They are tagged as near-normal references instead.

## Known finding in go-stats-calculator

`flat_rate_shipping_usd.txt` (20 copies of `4.99`) reproduces a bug in `stats` v1.14.0 that is still present in v1.15.0. The floating-point mean comes out as `4.989999999999999`, so the variance is about `8e-31` instead of exactly 0. The zero-variance guards evidently test for exactly zero and do not fire, so skewness (1.08), kurtosis (-2.24), autocorrelation (0.95), and CV are computed from rounding noise. A constant integer dataset such as twenty `5`s is handled correctly. A tolerance check, such as treating the variance as zero when `max == min` or when it is negligible relative to `mean**2`, would fix it.

## Suggested study order

Foundation first, complexity last:

1. `dataset_spec.py`
2. `sampling.py`
3. `discrete_generators.py`
4. `distribution_generators.py`
5. `time_series_generators.py`
6. `edge_case_generators.py`
7. `catalog.py`
8. `readme_writer.py`
9. `generate_non_random.py`
