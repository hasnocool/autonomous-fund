"""Deterministic pre-trade risk engine. No LLM calls belong in this module."""

from __future__ import annotations

from dataclasses import dataclass

from autonomous_fund.core.models import Order, PortfolioState, RiskDecision, Side


@dataclass(frozen=True)
class RiskLimits:
    max_gross_exposure: float = 1.0
    max_net_exposure: float = 1.0
    max_position_weight: float = 0.10
    max_strategy_weight: float = 0.35
    max_daily_loss: float = 0.02
    max_drawdown: float = 0.10
    max_order_notional: float = 10_000.0
    min_cash_buffer: float = 0.10


class RiskEngine:
    """Enforces hard portfolio and order constraints before execution."""

    def __init__(self, limits: RiskLimits) -> None:
        self.limits = limits

    def approve(self, portfolio: PortfolioState, order: Order) -> RiskDecision:
        reasons: list[str] = []
        notional = order.quantity * order.expected_price
        if notional > self.limits.max_order_notional:
            reasons.append("order notional exceeds max_order_notional")

        if portfolio.equity <= 0:
            reasons.append("portfolio equity is non-positive")
            return RiskDecision(approved=False, reasons=reasons)

        if portfolio.drawdown >= self.limits.max_drawdown:
            reasons.append("portfolio drawdown limit reached")
        if portfolio.daily_return <= -self.limits.max_daily_loss:
            reasons.append("daily loss limit reached")

        position = portfolio.positions.get(order.symbol)
        existing_qty = position.quantity if position else 0.0
        signed_delta = order.quantity if order.side is Side.BUY else -order.quantity
        projected_qty = existing_qty + signed_delta
        projected_value = projected_qty * order.expected_price
        projected_weight = projected_value / portfolio.equity
        if abs(projected_weight) > self.limits.max_position_weight + 1e-12:
            reasons.append("projected position exceeds max_position_weight")

        projected_cash = portfolio.cash - (notional if order.side is Side.BUY else -notional)
        if projected_cash / portfolio.equity < self.limits.min_cash_buffer - 1e-12:
            reasons.append("projected cash buffer below minimum")

        delta_weight = signed_delta * order.expected_price / portfolio.equity
        projected_net = portfolio.net_exposure + delta_weight
        projected_gross = portfolio.gross_exposure + abs(delta_weight)
        if abs(projected_net) > self.limits.max_net_exposure + 1e-12:
            reasons.append("projected net exposure exceeds limit")
        if projected_gross > self.limits.max_gross_exposure + 1e-12:
            reasons.append("projected gross exposure exceeds limit")

        return RiskDecision(
            approved=not reasons,
            reasons=reasons,
            projected_weight=projected_weight,
            projected_gross=projected_gross,
            projected_net=projected_net,
        )
