"""Connect regime screeners to candidate generation for research."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from autonomous_fund.screeners import ScreenerEngine, build_default_screeners
from autonomous_fund.screeners.definitions import ScreenResult


@dataclass(frozen=True, slots=True)
class Candidate:
    symbol: str
    regime: str
    score: float
    signals: tuple[str, ...]


class CandidatePipeline:
    """Generate ranked research candidates without placing trades."""

    def __init__(self) -> None:
        self.engine = ScreenerEngine(build_default_screeners())

    def run(self, frames: dict[str, pd.DataFrame], minimum_score: float = 60.0) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        for report in self.engine.screen_universe(frames):
            for result in report.ranked:
                if result.score < minimum_score:
                    continue
                candidates.append(
                    Candidate(
                        symbol=result.symbol,
                        regime=result.regime.value,
                        score=result.score,
                        signals=result.reasons,
                    )
                )
        return tuple(sorted(candidates, key=lambda item: item.score, reverse=True))

    @staticmethod
    def group_by_regime(candidates: tuple[Candidate, ...]) -> dict[str, tuple[Candidate, ...]]:
        groups: dict[str, list[Candidate]] = {}
        for candidate in candidates:
            groups.setdefault(candidate.regime, []).append(candidate)
        return {regime: tuple(items) for regime, items in groups.items()}
