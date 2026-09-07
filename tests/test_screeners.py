"""Tests for regime classification and screening."""

import numpy as np
import pandas as pd

from autonomous_fund.screeners import MarketRegime, RegimeClassifier, ScreenerEngine, build_default_screeners


def make_frame(length: int = 120, trend: float = 0.001) -> pd.DataFrame:
    close = 100 * np.exp(np.cumsum(np.full(length, trend)))
    return pd.DataFrame({"close": close, "high": close * 1.01, "low": close * 0.99, "volume": 1000.0})


def test_bull_regime() -> None:
    assert RegimeClassifier().classify(make_frame(trend=0.003)) == MarketRegime.BULL_TREND


def test_bear_regime() -> None:
    assert RegimeClassifier().classify(make_frame(trend=-0.003)) == MarketRegime.BEAR_TREND


def test_screening_produces_regime_compatible_results() -> None:
    report = ScreenerEngine(build_default_screeners()).screen("TEST", make_frame(trend=0.002))
    assert report.regime == MarketRegime.BULL_TREND
    assert report.results
    assert all(result.score >= 0 for result in report.results)
