"""Renders the README.md that documents the generated non-random datasets.
The README is built entirely from the catalog, so the dataset table and the
feature-to-file index always match what the generator produces. Rendering is kept
separate from file generation so either can change without touching the other."""

from dataset_spec import DatasetSpec, Feature

HEADER = """# non-random datasets

Simulated "real-world" datasets for exploring [go-stats-calculator](https://github.com/jftuga/go-stats-calculator). Unlike the uniform and power-skewed files in the sibling [`random/`](../random/) folder, each file here simulates a real process: queueing, seasonality, mixtures, power laws, discrete counts, capped measurements, and flaky sensors. Each one produces a distinctive statistical shape, including order-dependent shapes that only the trendline, autocorrelation, EMA, and input-order lines can reveal.

Files hold one number per line. The exception is `sensor_temp_log_c.txt`, which deliberately includes a header, `ERR` and `NaN` lines, and blank lines.

## Regenerating

Run from the repository root (the parent of this folder):

```bash
python3.14 non_random_gen/generate_non_random.py              # all files plus this README
python3.14 non_random_gen/generate_non_random.py --list       # show the catalog
python3.14 non_random_gen/generate_non_random.py --only queue_wait_s tide_height_ft
```

Output is reproducible: every dataset uses its own seed, derived from the base seed and the dataset name, so regenerating one file with `--only` gives the same bytes as a full run. Byte-identical output is guaranteed only on the same Python version, because `random`'s sampling algorithms can change between releases. The `--only` flag leaves this README untouched. This README was generated with base seed `{seed}`.
"""

NOTES = """## Notes

- The numeric claims (modes, MAD, kurtosis thresholds, symmetry, masking, input order, autocorrelation sign, and `-l` acceptance) were checked against `stats -j` output for base seeds 1 through 16. Histogram and trendline descriptions (bimodality, bumps, cycles, spikes) were checked visually for the default seed only. Exact numbers, such as the count of `ERR` lines, vary with the seed.
- Count is the number of values requested. For `sensor_temp_log_c.txt` it is the number of reading lines, about 210 of which are `ERR` or `NaN`; the file also has one header line and three blank lines, so `stats` reports roughly 86,190 values and 211 skipped lines.
- `stats -l` rejects any file containing a zero or negative value, and many files here do. Every file tagged "try -l" in the feature index is strictly positive.
"""


def render_readme(specs: tuple[DatasetSpec, ...], seed: int) -> str:
    """Build the complete README markdown for the dataset folder.

    Args:
        specs: All dataset specs in display order.
        seed: Base seed used for this generation run.

    Returns:
        The README contents as a single string ending in a newline.
    """
    sections = [HEADER.format(seed=seed), dataset_table(specs), feature_index(specs), NOTES]
    return "\n".join(sections)


def dataset_table(specs: tuple[DatasetSpec, ...]) -> str:
    """Render the markdown table that lists every dataset.

    Args:
        specs: All dataset specs in display order.

    Returns:
        A markdown section containing the dataset table.
    """
    rows = ["## Datasets", "", "| File | Count | Real-world process | Expected shape |", "|------|------:|--------------------|----------------|"]
    for spec in specs:
        rows.append(f"| `{spec.name}.txt` | {spec.count:,} | {spec.process} | {spec.shape} |")
    return "\n".join(rows) + "\n"


def feature_index(specs: tuple[DatasetSpec, ...]) -> str:
    """Render a table mapping each feature tag to the datasets that exhibit it.

    Args:
        specs: All dataset specs in display order.

    Returns:
        A markdown section containing the feature index table.
    """
    rows = ["## Feature index", "", "Which files to try when you want to see a particular property or `stats` behavior.", "", "| Feature | Files |", "|---------|-------|"]
    for feature in Feature:
        names = [f"`{spec.name}`" for spec in specs if feature in spec.features]
        if names:
            rows.append(f"| {feature} | {', '.join(names)} |")
    return "\n".join(rows) + "\n"
