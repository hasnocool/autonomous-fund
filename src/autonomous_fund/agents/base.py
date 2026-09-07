"""Agent contracts and explicit capability boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

Capability = Literal["read_market_data", "research", "propose_order", "approve_order", "execute_order", "transfer_funds"]


@dataclass(frozen=True)
class AgentContext:
    request_id: str
    portfolio_snapshot: dict[str, Any] = field(default_factory=dict)
    market_snapshot: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentDecision:
    agent_id: str
    action: str
    rationale: str
    confidence: float
    proposed: dict[str, Any] = field(default_factory=dict)


class Agent(ABC):
    agent_id: str
    capabilities: frozenset[Capability] = frozenset({"read_market_data", "research"})

    @abstractmethod
    def run(self, context: AgentContext) -> AgentDecision:
        raise NotImplementedError
