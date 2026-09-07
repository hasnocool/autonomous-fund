"""Regime-specific screener definitions."""

from dataclasses import dataclass
from typing import Callable

import pandas as pd

from autonomous_fund.screeners.regimes import MarketRegime


@dataclass(frozen=True, slots=True)
class ScreenResult:
    symbol: str
    score: float
    regime: MarketRegime
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ScreenerDefinition:
    name: str
    regimes: frozenset[MarketRegime]
    evaluator: Callable[[pd.DataFrame], tuple[float, tuple[str, ...]]]

    def evaluate(self, frame: pd.DataFrame, symbol: str, regime: MarketRegime) -> ScreenResult | None:
        if regime not in self.regimes:
            return None
        score, reasons = self.evaluator(frame)
        return ScreenResult(symbol=symbol, score=max(0.0, min(100.0, score)), regime=regime, reasons=reasons)
