"""Execution abstraction. State-changing broker operations stay behind this interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from autonomous_fund.core.models import Fill, Order, PortfolioState


class ExecutionVenue(ABC):
    @abstractmethod
    def submit(self, order: Order, portfolio: PortfolioState) -> Fill:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, order_id: str) -> None:
        raise NotImplementedError
