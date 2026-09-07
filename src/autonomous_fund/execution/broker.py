"""Order application service combining risk approval, execution, and accounting."""

from __future__ import annotations

from autonomous_fund.core.events import Event, EventLog
from autonomous_fund.core.models import Order, PortfolioState, Position, Side
from autonomous_fund.core.risk import RiskEngine
from autonomous_fund.execution.base import ExecutionVenue


class BrokerService:
    def __init__(self, venue: ExecutionVenue, risk: RiskEngine, event_log: EventLog) -> None:
        self.venue = venue
        self.risk = risk
        self.event_log = event_log

    def execute(self, portfolio: PortfolioState, order: Order) -> PortfolioState:
        decision = self.risk.approve(portfolio, order)
        self.event_log.append(Event("risk_decision", {"order": order.model_dump(mode="json"), "decision": decision.model_dump()}))
        if not decision.approved:
            raise PermissionError("risk rejected order: " + "; ".join(decision.reasons))

        fill = self.venue.submit(order, portfolio)
        sign = 1.0 if fill.side is Side.BUY else -1.0
        cash_delta = -sign * fill.quantity * fill.price - fill.fee
        existing = portfolio.positions.get(fill.symbol)
        old_qty = existing.quantity if existing else 0.0
        old_avg = existing.avg_price if existing else 0.0
        new_qty = old_qty + sign * fill.quantity
        realized = portfolio.realized_pnl
        if existing and sign < 0 and old_qty > 0:
            realized += (fill.price - old_avg) * min(fill.quantity, old_qty)
        avg = fill.price if new_qty == 0 else (old_avg * old_qty + sign * fill.quantity * fill.price) / new_qty
        positions = dict(portfolio.positions)
        if abs(new_qty) < 1e-12:
            positions.pop(fill.symbol, None)
        else:
            positions[fill.symbol] = Position(
                symbol=fill.symbol,
                asset_class=existing.asset_class if existing else order_asset_class(fill.symbol),
                quantity=new_qty,
                avg_price=avg,
                mark_price=fill.price,
                strategy_id=order.strategy_id,
            )
        updated = portfolio.model_copy(
            update={
                "cash": portfolio.cash + cash_delta,
                "positions": positions,
                "realized_pnl": realized,
            }
        )
        from autonomous_fund.core.portfolio import mark_to_market
        updated = mark_to_market(updated, {fill.symbol: fill.price})
        self.event_log.append(Event("fill", fill.model_dump(mode="json")))
        return updated


def order_asset_class(symbol: str):
    from autonomous_fund.core.models import AssetClass
    if symbol.upper().endswith("USD") or symbol.upper().endswith("USDT"):
        return AssetClass.CRYPTO
    return AssetClass.EQUITY
