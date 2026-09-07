# Autonomous Fund

Autonomous research, portfolio construction, risk, execution, and treasury platform for systematic crypto and equity trading.

> **Safety boundary:** the initial implementation is paper-trading-first. Live trading adapters are deliberately permissioned and require explicit configuration, deterministic risk checks, and operational controls.

## Goals

- Collect and validate market data from public APIs and configured brokers/exchanges.
- Discover classical and machine-learning strategies.
- Benchmark strategy changes before promotion.
- Run walk-forward validation and stress tests.
- Construct portfolios across strategies and assets.
- Apply deterministic risk limits before any order is allowed.
- Execute through paper/sandbox/live adapters behind a common interface.
- Maintain an auditable decision → risk approval → order → fill → P&L trail.
- Produce research, risk, performance, and governance reports.

## Architecture

AI/agent services propose and analyze; deterministic services enforce policy and perform state-changing operations.

`Market Data → Features → Research/Agents → Strategies → Validation → Portfolio → Risk Gate → Execution → Ledger → Analytics`

## Status

The repository is being built as a modular platform. The current milestone establishes the domain model, configuration, deterministic risk gate, paper broker, strategy interfaces, research workflow, and service boundaries.

See:

- `docs/PLAN.md` — scope and phased roadmap
- `docs/ARCHITECTURE.md` — system architecture and trust boundaries
- `docs/RISK.md` — risk policy and live-trading guardrails
- `docs/AGENTS.md` — agent responsibilities and permissions
- `docs/DEVELOPMENT.md` — local development and testing

## Quick start

```bash
uv sync --extra dev
uv run autonomous-fund health
uv run pytest
```

Run the paper engine:

```bash
uv run autonomous-fund paper-run --config config/paper.toml
```

Generate a sample research run:

```bash
uv run autonomous-fund research --config config/research.toml
```

## License

TBD.
