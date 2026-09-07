from pathlib import Path

from autonomous_fund.core.events import EventLog
from autonomous_fund.core.portfolio import empty_portfolio
from autonomous_fund.core.risk import RiskEngine, RiskLimits
from autonomous_fund.core.models import Order, OrderType, Side
from autonomous_fund.execution.broker import BrokerService
from autonomous_fund.execution.paper import PaperVenue


def test_paper_execution_records_fill(tmp_path: Path) -> None:
    log = EventLog(tmp_path / "events.jsonl")
    broker = BrokerService(PaperVenue(slippage_bps=0, fee_bps=0), RiskEngine(RiskLimits()), log)
    portfolio = empty_portfolio(100_000)
    order = Order(
        id="1", symbol="ABC", side=Side.BUY, quantity=10, order_type=OrderType.MARKET,
        strategy_id="test", expected_price=100,
    )
    updated = broker.execute(portfolio, order)
    assert updated.cash == 99_000
    assert updated.positions["ABC"].quantity == 10
    assert len(log.read()) == 2
