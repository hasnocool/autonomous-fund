"""Health state aggregation; unhealthy dependencies fail closed for trading."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheck:
    name: str
    healthy: bool
    detail: str = ""


@dataclass(frozen=True)
class SystemHealth:
    checks: tuple[HealthCheck, ...]

    @property
    def healthy(self) -> bool:
        return all(check.healthy for check in self.checks)

    @property
    def can_trade(self) -> bool:
        required = {"market-data", "risk-engine", "broker", "reconciliation"}
        return all(check.healthy for check in self.checks if check.name in required) and self.healthy
