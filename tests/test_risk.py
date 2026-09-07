from autonomous_fund.core.models import Order, OrderType, Side
from autonomous_fund.core.portfolio import empty_portfolio
from autonomous_fund.core.risk import RiskEngine, RiskLimits


def make_order(qty: float, price: float = 100.0) -> Order:
    return Order(
        id="test-order",
        symbol="TEST",
        side=Side.BUY,
        quantity=qty,
        order_type=OrderType.MARKET,
        strategy_id="test",
        expected_price=price,
    )


def test_risk_rejects_position_over_limit() -> None:
    p = empty_portfolio(1000.0)
    engine = RiskEngine(RiskLimits(max_position_weight=0.10, max_order_notional=10_000))
    decision = engine.approve(p, make_order(2.0))
    assert not decision.approved
    assert "max_position_weight" in " ".join(decision.reasons)


def test_risk_approves_small_order() -> None:
    p = empty_portfolio(1000.0)
    engine = RiskEngine(RiskLimits(max_position_weight=0.10, max_order_notional=10_000))
    decision = engine.approve(p, make_order(0.5))
    assert decision.approved
