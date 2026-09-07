# Autonomous Fund — Implementation Plan

## Mission

Build an autonomous systematic investment platform that can research markets, discover strategies, validate them, construct portfolios, enforce hard risk policy, execute orders, maintain a complete audit trail, and continuously evaluate whether strategies deserve capital.

## Non-negotiable architecture

1. **AI proposes; deterministic code disposes.** LLMs/agents may research, rank, explain, generate hypotheses, and propose targets. Deterministic risk, portfolio, execution, accounting, and security services decide what is permitted.
2. **Paper-first promotion.** No live adapter is enabled by default. Every strategy progresses through research, backtest, walk-forward validation, stress tests, paper trading, shadow/live-small-capital, then production.
3. **Every state change is auditable.** Record signal, strategy version, data snapshot/reference, agent reasoning summary, risk decision, order, fill, fee, slippage, and resulting portfolio state.
4. **Benchmark before mutation.** An ML overlay or strategy change survives only when it beats the locked baseline out-of-sample after costs and stress tests.
5. **Fail closed.** Missing data, stale prices, unknown balances, risk-service failure, broken permissions, and broker uncertainty block new risk.

## Scope

### Phase 0 — Foundation (implemented)

- Python 3.12 project layout.
- Typed domain models for signals, orders, fills, positions, portfolios, candidates, and results.
- TOML configuration with validation.
- Deterministic pre-trade risk engine.
- Paper execution venue with configurable slippage/fees.
- Broker application service joining risk → execution → accounting → audit events.
- Baseline moving-average momentum strategy.
- Dependency-light backtest harness.
- Research candidate evaluation pipeline.
- Initial CIO and Risk Officer agent boundaries.
- Unit tests for risk, paper execution, and audit logging.
- CLI for health, backtest, research, paper-run, and agents.

### Phase 1 — Data platform

- CCXT exchange adapters for crypto market data.
- Equities/ETF adapters.
- Historical bulk ingestion and incremental collectors.
- Canonical OHLCV/trades/order-book schemas.
- Data-quality checks: gaps, duplicates, timestamp drift, bad prices, split/dividend handling.
- DuckDB/Parquet lake plus optional PostgreSQL/Timescale operational store.
- Feature store with point-in-time correctness.

### Phase 2 — Research lab

- Strategy registry and immutable strategy versions.
- Momentum, mean reversion, breakout, trend, carry, pairs/stat-arb, volatility, and cross-sectional factors.
- Cost-aware backtesting with realistic fills.
- Walk-forward optimization.
- Bootstrap/Monte-Carlo robustness.
- Parameter perturbation and regime segmentation.
- Experiment metadata, artifacts, and reproducible seeds.
- Automatic research reports with tables and charts.

### Phase 3 — ML layer

- Feature screening and leakage detection.
- Baseline models: logistic/linear, random forest, gradient boosting.
- Probability calibration.
- Ensembles and regime-conditioned models.
- Model registry with dataset/feature/model hashes.
- Drift detection and retraining policy.
- Champion/challenger benchmarking.

### Phase 4 — Portfolio construction

- Strategy-level allocations.
- Asset-level target weights.
- Exposure/factor correlation estimation.
- Volatility targeting.
- Risk parity / HRP / minimum variance / max-Sharpe variants.
- CVaR and drawdown constraints.
- Liquidity-aware sizing.

### Phase 5 — Multi-agent investment process

- Macro Researcher.
- Crypto Market Structure Researcher.
- Equity Fundamental/Factor Researcher.
- News/Information Researcher.
- Quant Researcher.
- Strategy Discovery Agent.
- Validation/Devil's-Advocate Agent.
- Regime Agent.
- CIO/Portfolio Manager Agent.
- Risk Officer Agent with veto recommendation.
- Execution Agent.
- Post-trade Analyst.
- Strategy Attribution Agent.
- Research Librarian / Memory Agent.
- Model Governance Agent.
- Data Quality Agent.
- Security/Counterparty Agent.

### Phase 6 — Execution and treasury

- Smart order router.
- VWAP/TWAP and participation schedules.
- Limit/market execution policies.
- Venue health and latency monitoring.
- Broker/exchange reconciliation.
- Cash/stablecoin treasury allocation.
- Counterparty concentration limits.
- Withdrawal allowlists and transfer approval workflow.

### Phase 7 — Operations and governance

- Monitoring and alerting.
- Position/reconciliation dashboard.
- Immutable audit/event store.
- Kill switch and freeze-all-risk controls.
- Secret isolation and least-privilege API keys.
- Incident runbooks.
- Model/strategy retirement process.
- Compliance evidence export.

## Strategy lifecycle

`IDEA → SPEC → BACKTEST → WALK_FORWARD → STRESS → PAPER → SHADOW → SMALL_LIVE → PRODUCTION → REVIEW → RETIRED`

Every promotion requires a reproducible artifact bundle and a recorded decision. Strategies can be demoted automatically when drawdown, edge decay, turnover, slippage, or data quality breaches configured thresholds.

## Autonomous operating loops

### Daily

Data health → overnight event scan → research refresh → factor/regime update → portfolio rebalance proposal → risk review → execution window → reconciliation → P&L attribution → report.

### Weekly

Strategy leaderboard → correlation/overlap analysis → robustness refresh → champion/challenger review → capital reallocation proposal → infrastructure/cost review.

### Monthly

Full portfolio review → strategy retirement/addition decisions → model drift review → counterparty review → treasury review → governance/compliance package.

## Success criteria

The platform is ready for a controlled small-live pilot when it has deterministic risk enforcement, reproducible research, realistic cost modeling, point-in-time data, complete reconciliation, audited order lineage, functioning kill controls, and a documented approval process. Performance alone is not a release criterion.
