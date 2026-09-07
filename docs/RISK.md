# Risk Policy

The risk layer is deterministic and must fail closed. Agent recommendations are never sufficient to authorize an order.

## Hard controls

- Maximum gross and net exposure.
- Maximum position weight.
- Maximum strategy allocation.
- Maximum order notional.
- Minimum cash buffer.
- Daily loss stop.
- Portfolio drawdown stop.
- Stale/missing market-data rejection.
- Unknown balance/reconciliation rejection.
- Duplicate-order/idempotency checks.
- Venue health and rate-limit checks.

## Live-trading protections

1. Separate read-only, trade, and custody permissions.
2. Disable withdrawals on trading API keys whenever possible.
3. Keep a kill switch outside the agent process.
4. Require reconciliation before opening new risk after restart.
5. Rate-limit orders and cap total notional per interval.
6. Use allowlisted symbols and venues.
7. Require explicit promotion from paper to live-small before production.

## De-risking

As drawdown or volatility rises, reduce target gross exposure and disable fragile strategies. At the configured hard drawdown limit, new opening risk must stop until an explicit recovery policy allows it.

## Testing requirements

The risk engine must be tested with boundary values, rejected orders, restart/reconciliation scenarios, missing data, and broker failures. A risk-service failure is treated as a rejection, not an approval.
