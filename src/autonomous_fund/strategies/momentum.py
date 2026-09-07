"""Baseline time-series momentum strategy used as a transparent benchmark."""

from __future__ import annotations

from autonomous_fund.core.models import Signal, Side
from autonomous_fund.strategies.base import Bar, Strategy


class MovingAverageMomentum(Strategy):
    strategy_id = "momentum-ma"
    version = "0.1.0"

    def __init__(self, fast: int = 20, slow: int = 100, target_weight: float = 0.25) -> None:
        if fast <= 1 or slow <= fast:
            raise ValueError("require 1 < fast < slow")
        self.fast = fast
        self.slow = slow
        self.target_weight = target_weight

    def generate(self, bars: list[Bar]) -> Signal | None:
        if len(bars) < self.slow:
            return None
        closes = [bar.close for bar in bars[-self.slow :]]
        fast_ma = sum(closes[-self.fast :]) / self.fast
        slow_ma = sum(closes) / self.slow
        side = Side.BUY if fast_ma > slow_ma else Side.SELL
        score = min(1.0, abs(fast_ma / slow_ma - 1.0) * 100.0) if slow_ma else 0.0
        return Signal(
            symbol=bars[-1].symbol,
            strategy_id=self.strategy_id,
            side=side,
            score=score if side is Side.BUY else -score,
            target_weight=self.target_weight if side is Side.BUY else -self.target_weight,
            timestamp=bars[-1].timestamp,
            rationale=f"fast_ma={fast_ma:.6f}, slow_ma={slow_ma:.6f}",
        )
