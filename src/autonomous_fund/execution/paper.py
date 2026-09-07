"""Deterministic paper execution venue with configurable costs."""

from __future__ import annotations

import math

from autonomous_fund.core.models import Fill, Order, PortfolioState, Side
from autonomous_fund.execution.base import ExecutionVenue


class PaperVenue(ExecutionVenue):
    def __init__(self, slippage_bps: float = 5.0, fee_bps: float = 10.0) -> None:
        self.slippage_bps = slippage_bps
        self.fee_bps = fee_bps
        self._closed: set[str] = set()

    def submit(self, order: Order, portfolio: PortfolioState) -> Fill:
        if order.id in self._closed:
            raise ValueError(f"order {order.id} has already been closed")
        slip = self.slippage_bps / 10_000.0
        if order.side is Side.BUY:
            price = order.expected_price * (1.0 + slip)
        else:
            price = order.expected_price * (1.0 - slip)
        fee = order.quantity * price * self.fee_bps / 10_000.0
        slippage = abs(price - order.expected_price) * order.quantity
        self._closed.add(order.id)
        return Fill(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=price,
            fee=fee,
            slippage=slippage,
        )

    def cancel(self, order_id: str) -> None:
        self._closed.add(order_id)
