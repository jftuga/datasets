#!/usr/bin/env python3.14
"""Command-line entry point that writes the simulated real-world datasets to ../non-random.
Each dataset is generated with its own reproducible seed derived from a base seed and the
dataset name, so single files can be regenerated independently. A full run also writes
a README.md describing every dataset and the stats-tool features it exercises."""

import argparse
import random
import sys
import zlib
from pathlib import Path

from catalog import CATALOG
from dataset_spec import DatasetSpec
from readme_writer import render_readme

DEFAULT_SEED = 1
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "non-random"


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments.

    Returns:
        The parsed arguments, with ``only`` checked against the catalog.
    """
    parser = argparse.ArgumentParser(description=f"Generate simulated real-world datasets into {OUTPUT_DIR}.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help=f"base seed for all datasets (default: {DEFAULT_SEED})")
    parser.add_argument("--only", nargs="+", metavar="NAME", help="generate only these datasets; README is left untouched")
    parser.add_argument("--list", action="store_true", help="print the catalog and exit")
    args = parser.parse_args()
    if args.only:
        known = {spec.name for spec in CATALOG}
        unknown = sorted(set(args.only) - known)
        if unknown:
            parser.error(f"unknown dataset(s): {', '.join(unknown)} (use --list to see names)")
    return args


def select_specs(names: list[str] | None) -> list[DatasetSpec]:
    """Choose which catalog entries to generate.

    Args:
        names: Dataset names to keep, or None to keep every dataset.

    Returns:
        Matching specs in catalog order.
    """
    if not names:
        return list(CATALOG)
    wanted = set(names)
    return [spec for spec in CATALOG if spec.name in wanted]


def dataset_seed(base_seed: int, name: str) -> int:
    """Derive a stable per-dataset seed from the base seed and the dataset name.

    CRC32 is used instead of ``hash()`` because string hashing is randomized per process.

    Args:
        base_seed: The run's base seed.
        name: Dataset name.

    Returns:
        An integer seed unique to this dataset and base seed.
    """
    return base_seed * 2**32 + zlib.crc32(name.encode())


def write_dataset(spec: DatasetSpec, base_seed: int, out_dir: Path) -> tuple[Path, int]:
    """Generate one dataset and write it to ``<out_dir>/<name>.txt``.

    Args:
        spec: The dataset to generate.
        base_seed: The run's base seed.
        out_dir: Destination directory, which must already exist.

    Returns:
        Path of the written file and the number of lines written.
    """
    rng = random.Random(dataset_seed(base_seed, spec.name))
    lines = spec.generator(rng, spec.count)
    path = out_dir / f"{spec.name}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path, len(lines)


def print_catalog() -> None:
    """Print every dataset's name, count, and process description."""
    width = max(len(spec.name) for spec in CATALOG)
    for spec in CATALOG:
        print(f"{spec.name:<{width}}  {spec.count:>9,}  {spec.process}")


def main() -> None:
    """Run the generator CLI."""
    args = parse_args()
    if args.list:
        print_catalog()
        return
    OUTPUT_DIR.mkdir(exist_ok=True)
    for spec in select_specs(args.only):
        path, line_count = write_dataset(spec, args.seed, OUTPUT_DIR)
        print(f"wrote {path.name:<38} {line_count:>9,} lines", file=sys.stderr)
    if not args.only:
        readme = OUTPUT_DIR / "README.md"
        readme.write_text(render_readme(CATALOG, args.seed), encoding="utf-8")
        print(f"wrote {readme.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
