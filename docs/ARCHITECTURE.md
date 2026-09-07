# Architecture

## System layers

```text
                    ┌──────────────────────────────┐
                    │   Research / Agent Layer     │
                    │ CIO · Quant · Macro · ML     │
                    └──────────────┬───────────────┘
                                   │ proposals
                    ┌──────────────▼───────────────┐
                    │  Strategy / Portfolio Layer  │
                    │ targets · allocations · mode │
                    └──────────────┬───────────────┘
                                   │ candidate orders
                    ┌──────────────▼───────────────┐
                    │    Deterministic Risk Gate   │
                    │ limits · drawdown · exposure │
                    └──────────────┬───────────────┘
                                   │ approved orders
                    ┌──────────────▼───────────────┐
                    │     Execution / Broker       │
                    │ paper · sandbox · live       │
                    └──────────────┬───────────────┘
                                   │ fills
       ┌───────────────────────────▼────────────────────────┐
       │ Portfolio Accounting + Ledger + Audit Event Store │
       └───────────────────────────┬────────────────────────┘
                                   │ metrics / state
                    ┌──────────────▼───────────────┐
                    │ Monitoring / Governance      │
                    └──────────────────────────────┘
```

## Trust boundaries

**Agent layer:** untrusted advice. Agents have no direct exchange credentials and cannot bypass risk.

**Deterministic domain layer:** authoritative policy and accounting. This layer is the source of truth for exposure, P&L, limits, and allowed state transitions.

**Execution layer:** the only component permitted to communicate with a trading venue. It accepts only validated orders and returns normalized fills/errors.

**Secrets/custody:** broker credentials, wallet keys, and withdrawal permissions live outside agent prompts and source code. Live keys should be trade-only by default and have no withdrawal permission.

## Event lineage

Every proposed order should eventually be traceable as:

`market snapshot → features → signal → strategy version → agent proposal → portfolio target → risk decision → broker order → fill → accounting → performance attribution`

## Service boundaries

- `data`: market data ingestion, normalization, quality.
- `research`: experiments, strategy discovery, validation.
- `models`: ML/model registry and feature definitions.
- `portfolio`: optimization and target construction.
- `risk`: hard constraints and risk state.
- `execution`: venue abstraction, routing, order management.
- `treasury`: balances and transfers.
- `monitoring`: health, alerts, drift, reconciliation.
- `governance`: approvals, audit exports, model/strategy lifecycle.
- `agents`: bounded advisory orchestration.

## Deployment target

Start as a single process with SQLite/JSONL + local Parquet. Split services only when load, fault isolation, or operational requirements justify the complexity. The core domain packages must remain dependency-light so that research code cannot silently weaken execution controls.
