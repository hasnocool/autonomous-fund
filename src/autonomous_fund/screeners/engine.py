"""Run all compatible screeners over an instrument universe."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from autonomous_fund.screeners.definitions import ScreenResult, ScreenerDefinition
from autonomous_fund.screeners.regimes import MarketRegime, RegimeClassifier


@dataclass(frozen=True, slots=True)
class ScreenerReport:
    regime: MarketRegime
    results: tuple[ScreenResult, ...]

    @property
    def ranked(self) -> tuple[ScreenResult, ...]:
        return tuple(sorted(self.results, key=lambda x: x.score, reverse=True))


class ScreenerEngine:
    def __init__(self, screeners: tuple[ScreenerDefinition, ...], classifier: RegimeClassifier | None = None) -> None:
        self._screeners = screeners
        self._classifier = classifier or RegimeClassifier()

    def screen(self, symbol: str, frame: pd.DataFrame) -> ScreenerReport:
        regime = self._classifier.classify(frame)
        results = tuple(
            result
            for screener in self._screeners
            if (result := screener.evaluate(frame, symbol, regime)) is not None
        )
        return ScreenerReport(regime=regime, results=results)

    def screen_universe(self, frames: dict[str, pd.DataFrame]) -> tuple[ScreenerReport, ...]:
        reports = [self.screen(symbol, frame) for symbol, frame in frames.items()]
        return tuple(sorted(reports, key=lambda report: max((r.score for r in report.results), default=0), reverse=True))
