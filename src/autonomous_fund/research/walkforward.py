"""Walk-forward split utilities with chronological, leakage-resistant windows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class WalkForwardSplit(Generic[T]):
    train: list[T]
    validation: list[T]
    test: list[T]


def make_splits(items: list[T], n_splits: int = 5, train_ratio: float = 0.6, validation_ratio: float = 0.2) -> list[WalkForwardSplit[T]]:
    if n_splits < 2:
        raise ValueError("n_splits must be >= 2")
    if not 0 < train_ratio < 1 or not 0 < validation_ratio < 1 or train_ratio + validation_ratio >= 1:
        raise ValueError("train_ratio + validation_ratio must be < 1")
    n = len(items)
    test_ratio = 1.0 - train_ratio - validation_ratio
    min_window = int(n * (train_ratio + validation_ratio + test_ratio))
    if min_window < 30:
        raise ValueError("insufficient samples")
    step = max(1, int(n * test_ratio / n_splits))
    splits: list[WalkForwardSplit[T]] = []
    start = 0
    for _ in range(n_splits):
        train_end = start + max(1, int(n * train_ratio))
        valid_end = train_end + max(1, int(n * validation_ratio))
        test_end = valid_end + max(1, int(n * test_ratio / n_splits))
        if test_end > n:
            break
        splits.append(WalkForwardSplit(items[start:train_end], items[train_end:valid_end], items[valid_end:test_end]))
        start += step
    return splits
