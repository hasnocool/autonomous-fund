"""CIO agent: synthesizes research into target portfolio proposals, never executes orders."""

from __future__ import annotations

from autonomous_fund.agents.base import Agent, AgentContext, AgentDecision


class CIOAgent(Agent):
    agent_id = "cio"
    capabilities = frozenset({"read_market_data", "research", "propose_order"})

    def run(self, context: AgentContext) -> AgentDecision:
        candidates = context.market_snapshot.get("candidates", [])
        ranked = sorted(candidates, key=lambda x: float(x.get("score", 0.0)), reverse=True)
        proposal = ranked[:5]
        return AgentDecision(
            agent_id=self.agent_id,
            action="allocate",
            confidence=0.5 if proposal else 0.0,
            rationale="Rank research candidates; final orders require deterministic portfolio and risk gates.",
            proposed={"targets": proposal},
        )
