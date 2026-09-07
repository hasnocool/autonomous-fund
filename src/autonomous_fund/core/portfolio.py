"""Portfolio accounting and target-weight helpers."""

from __future__ import annotations

from autonomous_fund.core.models import PortfolioState, Position


def mark_to_market(portfolio: PortfolioState, prices: dict[str, float]) -> PortfolioState:
    positions: dict[str, Position] = {}
    unrealized = 0.0
    gross = 0.0
    net = 0.0
    for symbol, position in portfolio.positions.items():
        price = prices.get(symbol, position.mark_price)
        updated = position.model_copy(update={"mark_price": price})
        positions[symbol] = updated
        unrealized += (price - position.avg_price) * position.quantity
        weight = updated.market_value / max(portfolio.equity, 1e-12)
        gross += abs(weight)
        net += weight
    equity = portfolio.cash + sum(p.market_value for p in positions.values())
    peak = max(portfolio.peak_equity, equity)
    return portfolio.model_copy(
        update={
            "positions": positions,
            "unrealized_pnl": unrealized,
            "equity": equity,
            "peak_equity": peak,
            "gross_exposure": gross,
            "net_exposure": net,
        }
    )


def empty_portfolio(cash: float) -> PortfolioState:
    return PortfolioState(
        cash=cash,
        equity=cash,
        peak_equity=cash,
        daily_start_equity=cash,
    )
