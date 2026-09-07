# Market-Regime Screeners

The fund treats screening as a first-class research layer. A screener does not place an order; it identifies instruments whose current market structure matches a tested hypothesis.

## Regime coverage

| Regime | Primary screeners | Intended research use |
|---|---|---|
| Bull trend | trend-following, breakout, relative-strength | trend continuation and leadership |
| Bear trend | oversold-bounce, panic-defense | tactical rebounds and defense |
| Range | mean-reversion, volatility-compression, trend | bounded-market opportunities |
| High volatility | panic-defense | risk reduction and defensive candidates |
| Low volatility | mean-reversion, volatility-compression | compression and breakout preparation |
| Crisis | oversold-bounce, panic-defense | capitulation, hedging, survival |
| Recovery | trend-following, breakout, relative-strength | early trend transition |
| Unknown | none | insufficient data; no strategy promotion |

## Screening pipeline

```text
Market data
   ↓
Data quality checks
   ↓
Regime classifier
   ↓
Compatible screener set
   ↓
Feature calculations
   ↓
Individual scores + reasons
   ↓
Cross-sectional ranking
   ↓
Strategy eligibility filters
   ↓
Research / backtest candidates
```

## Required production expansion

The baseline suite is deliberately deterministic. Production development should add:

- trend strength, ADX, moving-average slope, breakout persistence
- volatility regime, ATR, realized volatility, volatility-of-volatility
- volume/liquidity, dollar volume, spread, turnover
- relative strength versus benchmark and peer universe
- momentum across 1d/5d/20d/60d/120d horizons
- mean-reversion z-scores and Bollinger-style deviations
- funding/basis/open-interest screeners for crypto derivatives
- carry/term-structure screeners
- cross-exchange price dispersion and arbitrage candidates
- factor exposure and residual-return screeners for equities
- earnings/event and catalyst screeners
- short-interest / borrow constraints where available
- market breadth and leadership screeners
- correlation-breakdown and contagion screeners
- liquidity stress and exit-capacity screeners
- regime transition screeners, not just steady-state regimes

Every new screener must be benchmarked out-of-sample and must include explicit data requirements, costs, liquidity assumptions, failure modes, and promotion criteria.
