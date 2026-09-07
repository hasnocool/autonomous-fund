"""Simple event-driven backtest harness kept independent from broker SDKs."""

from __future__ import annotations

import math

from autonomous_fund.core.models import BacktestResult
from autonomous_fund.strategies.base import Bar, Strategy


def run_backtest(strategy: Strategy, bars: list[Bar], fee_bps: float = 10.0) -> BacktestResult:
    if len(bars) < 120:
        raise ValueError("at least 120 bars are required")
    equity = 1.0
    peak = 1.0
    position = 0
    trades = 0
    returns: list[float] = []
    for i in range(100, len(bars) - 1):
        window = bars[i - 100 : i]
        signal = strategy.generate(window)
        desired = 1 if signal and signal.target_weight > 0 else -1 if signal and signal.target_weight < 0 else 0
        if desired != position:
            if desired:
                equity *= 1.0 - fee_bps / 10_000.0
            trades += 1
            position = desired
        r = bars[i + 1].close / bars[i].close - 1.0
        sr = position * r
        returns.append(sr)
        equity *= 1.0 + sr
        peak = max(peak, equity)
    mean = sum(returns) / max(1, len(returns))
    var = sum((x - mean) ** 2 for x in returns) / max(1, len(returns) - 1)
    vol = math.sqrt(var) * math.sqrt(24 * 365)
    sharpe = mean / math.sqrt(var) * math.sqrt(len(returns)) if var else 0.0
    max_dd = 0.0
    running = 1.0
    for r in returns:
        running *= 1.0 + r
        max_dd = max(max_dd, 1.0 - running / max(peak, running))
    years = max(1e-9, len(returns) / (24 * 365))
    annualized = equity ** (1 / years) - 1.0
    return BacktestResult(
        strategy_id=strategy.strategy_id,
        start=bars[100].timestamp,
        end=bars[-1].timestamp,
        total_return=equity - 1.0,
        annualized_return=annualized,
        volatility=vol,
        sharpe=sharpe,
        max_drawdown=max_dd,
        trade_count=trades,
        turnover=trades / max(1, len(returns)),
        passed=True,
    )
