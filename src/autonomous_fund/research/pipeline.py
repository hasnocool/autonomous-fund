"""Research pipeline enforcing Idea -> Backtest -> Validation -> Promotion stages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
import random

from autonomous_fund.core.models import BacktestResult, StrategyCandidate
from autonomous_fund.strategies.base import Bar, Strategy


@dataclass(frozen=True)
class ResearchPolicy:
    min_trades: int = 30
    max_drawdown: float = 0.20
    min_sharpe: float = 0.5


def synthetic_bars(symbol: str, n: int = 500, seed: int = 7) -> list[Bar]:
    rng = random.Random(seed)
    price = 100.0
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    bars: list[Bar] = []
    for i in range(n):
        drift = 0.0003 if (i // 80) % 2 == 0 else -0.0001
        shock = rng.gauss(0.0, 0.01)
        price *= math.exp(drift + shock)
        bars.append(Bar(start + timedelta(hours=i), symbol, price, 1_000 + rng.random() * 500))
    return bars


class ResearchPipeline:
    def __init__(self, policy: ResearchPolicy | None = None) -> None:
        self.policy = policy or ResearchPolicy()

    def evaluate(self, candidate: StrategyCandidate, strategy: Strategy, bars: list[Bar]) -> BacktestResult:
        if len(bars) < 100:
            raise ValueError("insufficient bars for evaluation")
        train_end = int(len(bars) * 0.6)
        test = bars[train_end:]
        equity = 1.0
        peak = equity
        returns: list[float] = []
        trades = 0
        position = 0
        for i in range(100, len(test)):
            window = test[max(0, i - 100):i]
            signal = strategy.generate(window)
            desired = 1 if signal and signal.target_weight > 0 else -1 if signal and signal.target_weight < 0 else 0
            if desired != position:
                trades += 1
                position = desired
            if i + 1 < len(test):
                r = test[i + 1].close / test[i].close - 1.0
                strategy_return = position * r
                equity *= 1.0 + strategy_return
                returns.append(strategy_return)
                peak = max(peak, equity)
        total_return = equity - 1.0
        mean = sum(returns) / max(1, len(returns))
        var = sum((r - mean) ** 2 for r in returns) / max(1, len(returns) - 1)
        vol = math.sqrt(var) * math.sqrt(24 * 365)
        ann = (equity ** (365 * 24 / max(1, len(test)))) - 1.0
        sharpe = (mean / math.sqrt(var) * math.sqrt(len(returns))) if var > 0 else 0.0
        max_dd = 1.0 - min((peak and equity / peak) or 0.0, 1.0)
        reasons: list[str] = []
        if trades < self.policy.min_trades:
            reasons.append("insufficient trades")
        if sharpe < self.policy.min_sharpe:
            reasons.append("sharpe below promotion threshold")
        if max_dd > self.policy.max_drawdown:
            reasons.append("drawdown above promotion threshold")
        return BacktestResult(
            strategy_id=candidate.strategy_id,
            start=test[0].timestamp,
            end=test[-1].timestamp,
            total_return=total_return,
            annualized_return=ann,
            volatility=vol,
            sharpe=sharpe,
            max_drawdown=max_dd,
            trade_count=trades,
            turnover=trades / max(1, len(test)),
            passed=not reasons,
            rejection_reasons=reasons,
        )
