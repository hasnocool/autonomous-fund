"""Deterministic synthetic market generator for local development and tests."""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta, timezone

from autonomous_fund.strategies.base import Bar


def generate_bars(symbol: str = "BTC/USDT", n: int = 1000, seed: int = 42) -> list[Bar]:
    rng = random.Random(seed)
    price = 100.0
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    output: list[Bar] = []
    for i in range(n):
        regime = 0.0004 if (i // 120) % 2 == 0 else -0.0002
        return_pct = regime + rng.gauss(0.0, 0.008)
        price = max(0.01, price * math.exp(return_pct))
        output.append(Bar(start + timedelta(hours=i), symbol, price, rng.uniform(1e3, 5e3)))
    return output
