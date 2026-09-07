"""Small dependency-light performance metric helpers."""

from __future__ import annotations

import math
from collections.abc import Iterable


def total_return(returns: Iterable[float]) -> float:
    equity = 1.0
    for value in returns:
        equity *= 1.0 + value
    return equity - 1.0


def sharpe(returns: list[float], periods_per_year: float = 24 * 365) -> float:
    if len(returns) < 2:
        return 0.0
    mean = sum(returns) / len(returns)
    variance = sum((x - mean) ** 2 for x in returns) / (len(returns) - 1)
    return mean / math.sqrt(variance) * math.sqrt(periods_per_year) if variance > 0 else 0.0


def max_drawdown(returns: Iterable[float]) -> float:
    equity = 1.0
    peak = 1.0
    worst = 0.0
    for value in returns:
        equity *= 1.0 + value
        peak = max(peak, equity)
        worst = max(worst, 1.0 - equity / peak)
    return worst
