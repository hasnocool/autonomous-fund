"""Normalized market-data provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from autonomous_fund.strategies.base import Bar


class MarketDataProvider(ABC):
    @abstractmethod
    def bars(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> list[Bar]:
        raise NotImplementedError
