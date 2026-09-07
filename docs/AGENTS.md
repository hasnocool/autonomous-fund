# Agent Responsibilities and Permissions

Agents are advisory by default. Capabilities are explicit and should be enforced by a separate policy layer.

| Agent | Purpose | Default capabilities |
|---|---|---|
| CIO | Aggregate research into portfolio proposals | read, research, propose |
| Quant Researcher | Factor/strategy hypothesis generation | read, research |
| Strategy Discovery | Generate strategy candidates | research |
| Validation / Devil's Advocate | Attempt to falsify candidates | research |
| Regime | Classify market state | read, research |
| Risk Officer | Interpret risk state and veto proposals | read, research |
| Execution | Convert approved targets to executable orders | read, execute only through broker service |
| Post-trade | Analyze fills/slippage | read, research |
| Attribution | Decompose P&L | read, research |
| Model Governance | Track model lineage/drift | read, research |
| Data Quality | Detect data defects | read, research |
| Counterparty | Monitor venue/custody risk | read, research |
| Treasury | Recommend balance allocations | read, research; transfers require separate human/policy authorization |
| Security | Detect anomalous operations | read, research; freeze signal |

## Multi-agent debate

For material portfolio changes, gather independent bull, bear, macro, quant, and risk assessments. A devil's-advocate stage attempts to invalidate the thesis. The CIO produces a proposal, but the deterministic risk gate remains authoritative.

## Agent output contract

Every decision should contain:

- agent identifier and version
- request/correlation identifier
- evidence/data references
- action type
- proposed state change, if any
- confidence
- concise rationale
- timestamp

Raw chain-of-thought is not required for auditability; store the decision rationale and evidence references needed to reproduce the decision.
