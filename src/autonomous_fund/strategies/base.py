"""Strategy interface: pure signal generation, no broker access."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from autonomous_fund.core.models import Signal


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    symbol: str
    close: float
    volume: float = 0.0


class Strategy(ABC):
    strategy_id: str
    version: str = "0.1.0"

    @abstractmethod
    def generate(self, bars: list[Bar]) -> Signal | None:
        raise NotImplementedError
