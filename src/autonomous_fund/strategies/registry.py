"""Strategy registry for immutable strategy/version lookup."""

from __future__ import annotations

from autonomous_fund.strategies.base import Strategy


class StrategyRegistry:
    def __init__(self) -> None:
        self._strategies: dict[str, Strategy] = {}

    def register(self, strategy: Strategy) -> None:
        key = f"{strategy.strategy_id}@{strategy.version}"
        if key in self._strategies:
            raise ValueError(f"strategy already registered: {key}")
        self._strategies[key] = strategy

    def get(self, strategy_id: str, version: str) -> Strategy:
        return self._strategies[f"{strategy_id}@{version}"]

    def list(self) -> list[str]:
        return sorted(self._strategies)
