"""TOML configuration loading with validated runtime settings."""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class FundConfig(BaseModel):
    name: str
    base_currency: str = "USD"
    mode: str = "research"
    starting_cash: float = Field(gt=0)


class RiskConfig(BaseModel):
    max_gross_exposure: float = Field(gt=0)
    max_net_exposure: float = Field(gt=0)
    max_position_weight: float = Field(gt=0, le=1)
    max_strategy_weight: float = Field(gt=0, le=1)
    max_daily_loss: float = Field(gt=0, le=1)
    max_drawdown: float = Field(gt=0, le=1)
    max_order_notional: float = Field(gt=0)
    min_cash_buffer: float = Field(ge=0, le=1)


class ExecutionConfig(BaseModel):
    venue: str = "paper"
    slippage_bps: float = Field(ge=0)
    fee_bps: float = Field(ge=0)


class ResearchConfig(BaseModel):
    train_ratio: float = Field(gt=0, lt=1)
    validation_ratio: float = Field(gt=0, lt=1)
    test_ratio: float = Field(gt=0, lt=1)
    walk_forward_splits: int = Field(ge=2)
    min_trades: int = Field(ge=1)


class DataConfig(BaseModel):
    timeframe: str
    lookback_bars: int = Field(ge=100)


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    fund: FundConfig
    risk: RiskConfig
    execution: ExecutionConfig
    research: ResearchConfig
    data: DataConfig

    @classmethod
    def from_toml(cls, path: str | Path) -> "Settings":
        with Path(path).open("rb") as handle:
            return cls.model_validate(tomllib.load(handle))
