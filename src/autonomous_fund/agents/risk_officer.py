"""Risk officer agent. It interprets risk state, but hard constraints remain deterministic."""

from __future__ import annotations

from autonomous_fund.agents.base import Agent, AgentContext, AgentDecision


class RiskOfficerAgent(Agent):
    agent_id = "risk-officer"
    capabilities = frozenset({"read_market_data", "research"})

    def run(self, context: AgentContext) -> AgentDecision:
        portfolio = context.portfolio_snapshot
        drawdown = float(portfolio.get("drawdown", 0.0))
        daily = float(portfolio.get("daily_return", 0.0))
        if drawdown >= 0.08 or daily <= -0.015:
            action = "de-risk"
            confidence = 0.9
            rationale = "Portfolio is near hard loss limits; reduce discretionary risk and investigate drivers."
        else:
            action = "maintain"
            confidence = 0.7
            rationale = "Portfolio is within configured soft risk bands."
        return AgentDecision(self.agent_id, action, rationale, confidence)
