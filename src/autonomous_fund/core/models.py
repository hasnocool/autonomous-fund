"""Core immutable-ish domain models shared by agents and deterministic services."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class AssetClass(str, Enum):
    CRYPTO = "crypto"
    EQUITY = "equity"
    ETF = "etf"
    FX = "fx"
    FUTURE = "future"
    OPTION = "option"
    CASH = "cash"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class Signal(BaseModel):
    model_config = ConfigDict(frozen=True)

    symbol: str
    strategy_id: str
    side: Side
    score: float = Field(ge=-1.0, le=1.0)
    target_weight: float = Field(ge=-1.0, le=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str = ""


class Position(BaseModel):
    symbol: str
    asset_class: AssetClass
    quantity: float = 0.0
    avg_price: float = 0.0
    mark_price: float = 0.0
    strategy_id: str | None = None

    @property
    def market_value(self) -> float:
        return self.quantity * self.mark_price


class PortfolioState(BaseModel):
    cash: float
    equity: float
    peak_equity: float
    positions: dict[str, Position] = Field(default_factory=dict)
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    gross_exposure: float = 0.0
    net_exposure: float = 0.0
    daily_start_equity: float | None = None

    @property
    def drawdown(self) -> float:
        if self.peak_equity <= 0:
            return 0.0
        return max(0.0, 1.0 - self.equity / self.peak_equity)

    @property
    def daily_return(self) -> float:
        if not self.daily_start_equity:
            return 0.0
        return self.equity / self.daily_start_equity - 1.0


class Order(BaseModel):
    id: str
    symbol: str
    side: Side
    quantity: float = Field(gt=0)
    order_type: OrderType = OrderType.MARKET
    limit_price: float | None = Field(default=None, gt=0)
    strategy_id: str
    expected_price: float = Field(gt=0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Fill(BaseModel):
    order_id: str
    symbol: str
    side: Side
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fee: float = Field(ge=0)
    slippage: float = Field(ge=0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RiskDecision(BaseModel):
    approved: bool
    reasons: list[str] = Field(default_factory=list)
    projected_weight: float | None = None
    projected_gross: float | None = None
    projected_net: float | None = None


class BacktestResult(BaseModel):
    strategy_id: str
    start: datetime
    end: datetime
    total_return: float
    annualized_return: float
    volatility: float
    sharpe: float
    max_drawdown: float
    trade_count: int
    turnover: float
    passed: bool = False
    rejection_reasons: list[str] = Field(default_factory=list)


class StrategyCandidate(BaseModel):
    strategy_id: str
    family: str
    version: str = "0.1.0"
    parameters: dict[str, float | int | str | bool] = Field(default_factory=dict)
    thesis: str
    expected_edge: float = 0.0

    @field_validator("strategy_id")
    @classmethod
    def normalize_id(cls, value: str) -> str:
        return value.strip().lower().replace(" ", "-")
