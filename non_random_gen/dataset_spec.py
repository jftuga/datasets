"""Defines the DatasetSpec record and the Feature vocabulary used to describe datasets.
A DatasetSpec ties a file name and row count to a generator function, plus the
human-readable story and statistical signature that go into the generated README.
Feature tags name the go-stats-calculator behaviors each dataset is meant to exercise."""

import random
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

type Generator = Callable[[random.Random, int], list[str]]


class Feature(StrEnum):
    """Statistical properties or stats-tool behaviors a dataset is designed to exhibit."""

    HEAVY_TAIL = "heavy right tail"
    LOG_SCALE = "strictly positive, spans orders of magnitude (try -l)"
    LEFT_SKEW = "left skew"
    NEAR_NORMAL = "near-normal reference (mesokurtic)"
    MULTIMODAL = "multimodal histogram"
    PLATYKURTIC = "platykurtic (thin tails)"
    LEPTOKURTIC = "leptokurtic (heavy tails)"
    DISCRETE = "discrete values / true mode"
    CEILING = "pile-up at a cap or floor"
    POS_AUTOCORR = "positive autocorrelation"
    NEG_AUTOCORR = "negative autocorrelation"
    TREND = "trend or seasonality (trendline, -e)"
    SORTED = "pre-sorted input order"
    SYMMETRY = "exact symmetry"
    MASKING = "z-score masking (try -z 2.5)"
    MAD_ZERO = "MAD is zero"
    ZERO_VARIANCE = "zero variance"
    SKIPPED = "malformed lines (Skipped)"
    NEGATIVE = "negative values"
    SMALL_MAGNITUDE = "small magnitudes"


@dataclass(frozen=True, slots=True)
class DatasetSpec:
    """Describes one dataset file: what it simulates, how big it is, and how to build it.

    Attributes:
        name: File stem; the dataset is written to ``<name>.txt``.
        count: Number of lines the generator is asked to produce.
        process: The real-world process being simulated.
        shape: The statistical signature the data is expected to show.
        features: Feature tags used to build the README cross-reference.
        generator: Function that takes a seeded RNG and a count and returns output lines.
    """

    name: str
    count: int
    process: str
    shape: str
    features: tuple[Feature, ...]
    generator: Generator
