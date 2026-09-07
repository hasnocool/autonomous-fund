# Development

## Environment

Python 3.12 and `uv` are the reference local environment.

```bash
uv sync --extra all
uv run pytest
uv run ruff check .
uv run mypy src
```

## Local workflows

Backtest the baseline strategy:

```bash
uv run autonomous-fund backtest --symbol BTC/USDT --bars 2000
```

Run the research gate:

```bash
uv run autonomous-fund research
```

Run one paper execution cycle:

```bash
uv run autonomous-fund paper-run
```

## Repository layout

```text
config/                 validated TOML runtime profiles
src/autonomous_fund/
  agents/               bounded advisory agents
  backtesting/          event-driven backtests
  core/                 domain models, risk, portfolio, events, config
  data/                 market-data adapters/generators
  execution/            broker and venue abstractions
  research/             candidate evaluation and walk-forward tools
  reports/              metrics and report generation
  strategies/           pure signal-generation implementations
tests/                  deterministic unit tests
docs/                   architecture, roadmap, risk, agent policy
```

## Adding a strategy

Implement `Strategy.generate()` without importing broker/execution modules. Give the strategy a stable identifier and semantic version. Add unit tests and a benchmark/backtest configuration. Do not allow a strategy to write persistent trading state directly.

## Adding an agent

Subclass `Agent`, declare the smallest possible capability set, return an `AgentDecision`, and keep credentials and order submission outside the agent. Any state-changing proposal must pass through deterministic services.

## Promotion gate

A candidate is not production-ready because a backtest is profitable. Promotion requires out-of-sample evidence, realistic costs, robustness tests, walk-forward stability, operational readiness, and risk/governance approval.
