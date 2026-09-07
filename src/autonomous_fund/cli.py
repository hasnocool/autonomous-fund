"""Command-line entry point for local research and paper trading."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import typer

from autonomous_fund.agents.cio import CIOAgent
from autonomous_fund.agents.base import AgentContext
from autonomous_fund.agents.risk_officer import RiskOfficerAgent
from autonomous_fund.backtesting.engine import run_backtest
from autonomous_fund.core.config import Settings
from autonomous_fund.core.events import EventLog
from autonomous_fund.core.portfolio import empty_portfolio
from autonomous_fund.core.risk import RiskEngine, RiskLimits
from autonomous_fund.core.models import Order, OrderType, Side, StrategyCandidate
from autonomous_fund.data.synthetic import generate_bars
from autonomous_fund.execution.broker import BrokerService
from autonomous_fund.execution.paper import PaperVenue
from autonomous_fund.research.pipeline import ResearchPipeline, ResearchPolicy
from autonomous_fund.strategies.momentum import MovingAverageMomentum

app = typer.Typer(no_args_is_help=True)


@app.command()
def health() -> None:
    """Validate that the package imports and runtime is available."""
    typer.echo("autonomous-fund: healthy")


@app.command()
def backtest(symbol: str = "BTC/USDT", bars: int = 1000) -> None:
    """Run the transparent baseline momentum backtest on synthetic data."""
    result = run_backtest(MovingAverageMomentum(), generate_bars(symbol, bars))
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def research(config: Path = typer.Option("config/research.toml", exists=True)) -> None:
    """Evaluate a candidate strategy through the research gate."""
    settings = Settings.from_toml(config)
    pipeline = ResearchPipeline(ResearchPolicy(min_trades=settings.research.min_trades))
    candidate = StrategyCandidate(
        strategy_id="momentum-ma",
        family="trend",
        thesis="Fast moving average above slow moving average indicates persistent trend.",
        parameters={"fast": 20, "slow": 100},
    )
    result = pipeline.evaluate(candidate, MovingAverageMomentum(), generate_bars("BTC/USDT", settings.data.lookback_bars))
    typer.echo(result.model_dump_json(indent=2))


@app.command("paper-run")
def paper_run(config: Path = typer.Option("config/paper.toml", exists=True)) -> None:
    """Run one paper order cycle with a hard deterministic risk gate."""
    settings = Settings.from_toml(config)
    portfolio = empty_portfolio(settings.fund.starting_cash)
    event_log = EventLog("data/events.jsonl")
    risk = RiskEngine(RiskLimits(**settings.risk.model_dump()))
    broker = BrokerService(PaperVenue(settings.execution.slippage_bps, settings.execution.fee_bps), risk, event_log)
    price = generate_bars("BTC/USDT", 120)[-1].close
    order = Order(
        id=str(uuid4()),
        symbol="BTC/USDT",
        side=Side.BUY,
        quantity=min(0.01, settings.risk.max_order_notional / price),
        order_type=OrderType.MARKET,
        strategy_id="demo-paper",
        expected_price=price,
    )
    updated = broker.execute(portfolio, order)
    typer.echo(updated.model_dump_json(indent=2))


@app.command("agents")
def agents() -> None:
    """Demonstrate advisory agents operating without execution permissions."""
    context = AgentContext("demo", {"drawdown": 0.01, "daily_return": 0.002}, {"candidates": []})
    typer.echo(CIOAgent().run(context).rationale)
    typer.echo(RiskOfficerAgent().run(context).rationale)
