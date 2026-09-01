# Behavioral Profiling & Telemetry

## Purpose

The behavioral personalization layer adapts financial intelligence according to the user's investment profile. This allows identical market evidence to produce different advice for different users.

## Profile A — Conservative / Long-term SIP

- Risk tolerance: Conservative
- Strategy: Long-term SIP
- Higher sensitivity to fundamental stability and downside risk
- Lower tolerance for leverage and short-term volatility
- Technical / Fundamental / Sentiment weights: 25% / 55% / 20%

## Profile B — High-Risk / Intraday F&O

- Risk tolerance: Aggressive
- Strategy: Intraday F&O
- Higher tolerance for volatility
- Greater emphasis on short-term momentum and sentiment
- Technical / Fundamental / Sentiment weights: 45% / 20% / 35%

## Persona Decision Logic

The `apply_persona(signals, rag_output, profile_id)` function converts bullish, neutral and bearish evidence into normalized scores.

- Bullish / Positive = +1
- Neutral = 0
- Bearish / Negative = -1

These scores are multiplied by the selected persona's weights to produce a weighted signal score.

Portfolio allocation limits can act as a safety override.

## Portfolio Risk Concentration

Portfolio concentration is measured using the Herfindahl-Hirschman Index:

HHI = sum(weight_i²)

The system uses the HHI to identify low, moderate and high portfolio concentration.

## Session Telemetry

The system records:

1. Execution latency using `time.perf_counter()`
2. Portfolio risk concentration score
3. Final recommendation confidence
4. Number of sources consulted
5. Whether the pipeline completed within 60 seconds

## Integration

The `fetch_user_profile(profile_id)` function provides the user's behavioral profile to the orchestration layer.

The `apply_persona()` function provides explicit persona-aware weighting and recommendation logic.

Together, behavioral profiling and telemetry make the financial intelligence personalized, measurable and explainable.
