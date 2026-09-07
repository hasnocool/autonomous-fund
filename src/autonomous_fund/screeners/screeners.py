"""Built-in classical screeners designed for different market regimes."""

from __future__ import annotations

import pandas as pd

from autonomous_fund.screeners.definitions import ScreenerDefinition
from autonomous_fund.screeners.regimes import MarketRegime


def _trend(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    ma20, ma50 = c.rolling(20).mean().iloc[-1], c.rolling(50).mean().iloc[-1]
    ret20 = c.iloc[-1] / c.iloc[-21] - 1.0
    score = 50 + min(25, max(-25, ret20 * 150))
    score += 15 if c.iloc[-1] > ma20 > ma50 else 0
    return score, (f"20d return={ret20:.1%}", "price above rising moving averages" if score > 65 else "trend is not fully confirmed")


def _breakout(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c, h = frame["close"].astype(float), frame["high"].astype(float)
    prior_high = h.rolling(55).max().shift(1).iloc[-1]
    distance = c.iloc[-1] / prior_high - 1.0 if prior_high else 0.0
    score = 50 + min(40, max(-40, distance * 500))
    return score, (f"55-bar breakout distance={distance:.2%}", "price is breaking recent highs" if distance > 0 else "below recent breakout level")


def _mean_reversion(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    ma20 = c.rolling(20).mean().iloc[-1]
    sd20 = c.rolling(20).std().iloc[-1]
    z = (c.iloc[-1] - ma20) / sd20 if sd20 else 0.0
    score = min(100, abs(z) * 35)
    return score, (f"20d z-score={z:.2f}", "stretched away from mean" if abs(z) > 1.5 else "limited mean-reversion signal")


def _volatility_compression(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    v20 = c.pct_change().rolling(20).std().iloc[-1]
    v60 = c.pct_change().rolling(60).std().iloc[-1]
    ratio = v20 / v60 if v60 else 1.0
    score = max(0, min(100, 100 - ratio * 100))
    return score, (f"volatility ratio={ratio:.2f}", "compressed volatility" if ratio < 0.75 else "volatility not compressed")


def _relative_strength(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    r5, r20, r60 = c.iloc[-1] / c.iloc[-6] - 1, c.iloc[-1] / c.iloc[-21] - 1, c.iloc[-1] / c.iloc[-61] - 1
    score = 50 + min(50, max(-50, (r5 + r20 + r60) * 120))
    return score, (f"5/20/60d returns={r5:.1%}/{r20:.1%}/{r60:.1%}", "persistent relative strength" if score > 65 else "mixed strength")


def _oversold_bounce(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    ret5 = c.iloc[-1] / c.iloc[-6] - 1
    ret20 = c.iloc[-1] / c.iloc[-21] - 1
    bounce = ret5 if ret5 > 0 else 0
    score = min(100, max(0, 50 - ret20 * 100 + bounce * 300))
    return score, (f"5d return={ret5:.1%}, 20d return={ret20:.1%}", "downtrend showing short-term bounce" if ret20 < 0 and ret5 > 0 else "bounce pattern weak")


def _panic_defense(frame: pd.DataFrame) -> tuple[float, tuple[str, ...]]:
    c = frame["close"].astype(float)
    ret5 = c.iloc[-1] / c.iloc[-6] - 1
    vol = c.pct_change().rolling(20).std().iloc[-1]
    score = min(100, max(0, 50 - ret5 * 150 + vol * 500))
    return score, (f"5d return={ret5:.1%}, 20d vol={vol:.2%}", "defensive signal elevated" if score > 70 else "no extreme panic signal")


def build_default_screeners() -> tuple[ScreenerDefinition, ...]:
    all_trend = frozenset({MarketRegime.BULL_TREND, MarketRegime.RECOVERY, MarketRegime.RANGE})
    all_risk = frozenset({MarketRegime.BEAR_TREND, MarketRegime.HIGH_VOLATILITY, MarketRegime.CRISIS})
    return (
        ScreenerDefinition("trend-following", all_trend, _trend),
        ScreenerDefinition("breakout", frozenset({MarketRegime.BULL_TREND, MarketRegime.RECOVERY}), _breakout),
        ScreenerDefinition("mean-reversion", frozenset({MarketRegime.RANGE, MarketRegime.LOW_VOLATILITY}), _mean_reversion),
        ScreenerDefinition("volatility-compression", frozenset({MarketRegime.LOW_VOLATILITY, MarketRegime.RANGE}), _volatility_compression),
        ScreenerDefinition("relative-strength", frozenset({MarketRegime.BULL_TREND, MarketRegime.RECOVERY}), _relative_strength),
        ScreenerDefinition("oversold-bounce", frozenset({MarketRegime.BEAR_TREND, MarketRegime.CRISIS}), _oversold_bounce),
        ScreenerDefinition("panic-defense", all_risk, _panic_defense),
    )
