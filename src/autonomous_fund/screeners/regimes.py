"""Market regime classification for adaptive screening."""

from __future__ import annotations

from enum import StrEnum

import pandas as pd


class MarketRegime(StrEnum):
    BULL_TREND = "bull_trend"
    BEAR_TREND = "bear_trend"
    RANGE = "range"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    CRISIS = "crisis"
    RECOVERY = "recovery"
    UNKNOWN = "unknown"


class RegimeClassifier:
    """Deterministic baseline classifier; ML regime models can replace/augment it later."""

    def classify(self, frame: pd.DataFrame) -> MarketRegime:
        required = {"close"}
        if not required.issubset(frame.columns) or len(frame) < 60:
            return MarketRegime.UNKNOWN

        close = frame["close"].astype(float)
        ret20 = close.iloc[-1] / close.iloc[-21] - 1.0
        ret60 = close.iloc[-1] / close.iloc[-61] - 1.0
        daily_vol = close.pct_change().rolling(20).std().iloc[-1]
        long_vol = close.pct_change().rolling(60).std().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if pd.isna(daily_vol) or pd.isna(long_vol):
            return MarketRegime.UNKNOWN
        if ret20 < -0.15 and daily_vol > long_vol * 1.5:
            return MarketRegime.CRISIS
        if ret20 > 0.08 and ret60 < 0.0:
            return MarketRegime.RECOVERY
        if daily_vol > 0.06:
            return MarketRegime.HIGH_VOLATILITY
        if daily_vol < 0.015:
            return MarketRegime.LOW_VOLATILITY
        if close.iloc[-1] > ma20 > ma50 and ret20 > 0.0 and ret60 > 0.0:
            return MarketRegime.BULL_TREND
        if close.iloc[-1] < ma20 < ma50 and ret20 < 0.0 and ret60 < 0.0:
            return MarketRegime.BEAR_TREND
        return MarketRegime.RANGE
