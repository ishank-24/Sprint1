"""
Member 4 - Behavioral Profiling & Telemetry

Provides:
1. Two static user personas.
2. Persona-aware recommendation weighting.
3. Portfolio concentration measurement using HHI.
4. Session latency/telemetry helpers.
5. A provider function compatible with orchestrator.py.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Mapping


PROFILES: Dict[str, Dict[str, Any]] = {
    "p_conservative": {
        "persona_id": "conservative_retail_01",
        "profile_id": "p_conservative",
        "user_name": "Conservative SIP Investor",
        "risk_tolerance": "CONSERVATIVE",
        "strategy": "LONG_TERM_SIP",
        "max_single_stock_allocation_pct": 5.0,
        "weights": {
            "technical": 0.25,
            "fundamental": 0.55,
            "sentiment": 0.20,
        },
        "behavioral_traits": {
            "loss_aversion_index": 0.88,
            "derivatives_allowed": False,
            "overtrading_risk": "LOW",
        },
        "mandate": (
            "Capital preservation, long-term SIP discipline, "
            "avoid excessive volatility and leverage."
        ),
        "current_portfolio": {
            "total_value_inr": 1250000,
            "cash_pct": 18.0,
            "holdings": {
                "RELIANCE": {"allocation_pct": 4.5, "unrealized_pnl_pct": 14.2},
                "TCS": {"allocation_pct": 6.0, "unrealized_pnl_pct": -3.5},
                "HDFCBANK": {"allocation_pct": 8.0, "unrealized_pnl_pct": 2.1},
            },
        },
    },
    "p_aggressive": {
        "persona_id": "aggressive_intraday_02",
        "profile_id": "p_aggressive",
        "user_name": "High-Risk Intraday F&O Investor",
        "risk_tolerance": "AGGRESSIVE",
        "strategy": "INTRADAY_FNO",
        "max_single_stock_allocation_pct": 15.0,
        "weights": {
            "technical": 0.45,
            "fundamental": 0.20,
            "sentiment": 0.35,
        },
        "behavioral_traits": {
            "loss_aversion_index": 0.35,
            "derivatives_allowed": True,
            "overtrading_risk": "MODERATE_HIGH",
        },
        "mandate": (
            "Momentum capture and high capital appreciation while "
            "maintaining strict warnings against over-leverage."
        ),
        "current_portfolio": {
            "total_value_inr": 350000,
            "cash_pct": 30.0,
            "holdings": {
                "RELIANCE": {"allocation_pct": 2.0, "unrealized_pnl_pct": 8.0},
                "TCS": {"allocation_pct": 0.0, "unrealized_pnl_pct": 0.0},
                "ZOMATO": {"allocation_pct": 14.0, "unrealized_pnl_pct": 32.5},
            },
        },
    },
}


def _resolve_profile(profile_id: str) -> Dict[str, Any]:
    key = str(profile_id).lower().strip()
    if key in PROFILES:
        return PROFILES[key]
    if "conservative" in key:
        return PROFILES["p_conservative"]
    if "aggressive" in key or "fno" in key or "intraday" in key:
        return PROFILES["p_aggressive"]
    raise ValueError(
        f"Unknown profile_id={profile_id!r}. "
        "Use 'p_conservative' or 'p_aggressive'."
    )


def fetch_user_profile(persona_id: str) -> Dict[str, Any]:
    """Provider compatible with FinancialIntelligenceOrchestrator."""
    profile = _resolve_profile(persona_id)
    return {
        "agent": "UserProfileAgent",
        "persona_id": profile["persona_id"],
        "profile_id": profile["profile_id"],
        "user_name": profile["user_name"],
        "risk_tolerance": profile["risk_tolerance"],
        "strategy": profile["strategy"],
        "max_single_stock_allocation_pct": profile[
            "max_single_stock_allocation_pct"
        ],
        "current_portfolio": profile["current_portfolio"],
        "behavioral_traits": profile["behavioral_traits"],
        "mandate": profile["mandate"],
    }


def _signal_to_score(signal: Any) -> float:
    value = str(signal).upper().strip()
    if value in {"BUY", "BULLISH", "POSITIVE", "STRONG_BUY"}:
        return 1.0
    if value in {"SELL", "BEARISH", "NEGATIVE", "STRONG_SELL"}:
        return -1.0
    return 0.0


def _get_signal(signals: Mapping[str, Any], key: str) -> Dict[str, Any]:
    value = signals.get(key, {})
    return value if isinstance(value, dict) else {}


def apply_persona(
    signals: Mapping[str, Any],
    rag_output: Mapping[str, Any] | None,
    profile_id: str,
) -> Dict[str, Any]:
    """
    Adjust a recommendation using the user's persona.

    signals can contain technical, fundamental, sentiment, and/or synthesis.
    rag_output can contain RAG sentiment, confidence, citations and risk_flag.
    """
    profile = _resolve_profile(profile_id)
    rag_output = rag_output or {}

    technical = _get_signal(signals, "technical")
    fundamental = _get_signal(signals, "fundamental")
    sentiment = _get_signal(signals, "sentiment")
    synthesis = _get_signal(signals, "synthesis")

    technical_signal = technical.get("signal", technical.get("momentum", "NEUTRAL"))
    fundamental_signal = fundamental.get(
        "signal",
        fundamental.get("sentiment", rag_output.get("sentiment", "NEUTRAL")),
    )
    sentiment_signal = sentiment.get(
        "signal",
        sentiment.get("sentiment", rag_output.get("sentiment", "NEUTRAL")),
    )

    scores = {
        "technical": _signal_to_score(technical_signal),
        "fundamental": _signal_to_score(fundamental_signal),
        "sentiment": _signal_to_score(sentiment_signal),
    }

    weights = profile["weights"]
    weighted_score = sum(scores[name] * weights[name] for name in weights)

    base_recommendation = synthesis.get("recommendation")
    if base_recommendation:
        base_recommendation = str(base_recommendation)

    holdings = profile["current_portfolio"].get("holdings", {})
    ticker = (
        technical.get("ticker")
        or fundamental.get("ticker")
        or sentiment.get("ticker")
        or synthesis.get("ticker")
        or rag_output.get("ticker")
        or ""
    ).upper()

    holding = holdings.get(ticker, {})
    current_alloc = float(
        holding.get("allocation_pct", 0.0) if isinstance(holding, dict) else 0.0
    )
    max_alloc = float(profile["max_single_stock_allocation_pct"])
    over_limit = current_alloc >= max_alloc

    if over_limit:
        recommendation = "HOLD_MAX_CAPACITY_REACHED"
        adjustment = "New exposure blocked because the profile allocation limit is reached."
    elif weighted_score >= 0.45:
        recommendation = "BUY"
        adjustment = "Bullish evidence dominates after persona-specific weighting."
    elif weighted_score <= -0.45:
        recommendation = "SELL"
        adjustment = "Bearish evidence dominates after persona-specific weighting."
    else:
        recommendation = "HOLD"
        adjustment = "Evidence is mixed after persona-specific weighting."

    # Preserve stronger safety decisions already produced by the synthesis layer.
    if base_recommendation in {
        "HOLD_MAX_CAPACITY_REACHED",
        "CAUTIOUS_HOLD",
        "WAIT_FOR_FULL_DATA",
        "NEUTRAL_HOLD",
        "AVOID_OR_TRIM",
    }:
        recommendation = base_recommendation

    raw_confidences = []
    for item in (technical, fundamental, sentiment):
        if item.get("confidence") is not None:
            try:
                raw_confidences.append(float(item["confidence"]))
            except (TypeError, ValueError):
                pass

    if rag_output.get("confidence") is not None:
        try:
            raw_confidences.append(float(rag_output["confidence"]))
        except (TypeError, ValueError):
            pass

    avg_confidence = (
        sum(raw_confidences) / len(raw_confidences)
        if raw_confidences
        else 0.60
    )

    confidence = avg_confidence
    if profile["risk_tolerance"] == "CONSERVATIVE":
        confidence *= 0.95
    if over_limit:
        confidence *= 0.85
    if str(rag_output.get("status", "")).upper() in {"UNAVAILABLE", "DEGRADED"}:
        confidence *= 0.60

    confidence = round(max(0.0, min(1.0, confidence)), 2)

    reason = (
        f"{profile['user_name']} uses {profile['strategy']} weighting: "
        f"technical={weights['technical']:.0%}, "
        f"fundamental={weights['fundamental']:.0%}, "
        f"sentiment={weights['sentiment']:.0%}. "
        f"Weighted signal score={weighted_score:.2f}. "
        f"Current {ticker or 'stock'} allocation={current_alloc:.1f}% "
        f"vs profile limit={max_alloc:.1f}%. {adjustment}"
    )

    return {
        "profile_id": profile["profile_id"],
        "risk_tolerance": profile["risk_tolerance"],
        "strategy": profile["strategy"],
        "recommendation": recommendation,
        "confidence_score": confidence,
        "weighted_signal_score": round(weighted_score, 3),
        "weights": weights,
        "current_allocation_pct": current_alloc,
        "max_single_stock_allocation_pct": max_alloc,
        "over_allocation_limit": over_limit,
        "reason": reason,
        "mandate": profile["mandate"],
        "sources": list(rag_output.get("citations", [])),
    }


def calculate_portfolio_hhi(portfolio: Mapping[str, Any]) -> float:
    """
    Calculate Herfindahl-Hirschman Index.

    Accepts:
      {"RELIANCE": 0.5, "TCS": 0.3, "HDFC": 0.2}
    or:
      {"holdings": {"RELIANCE": {"allocation_pct": 50}, ...}}
    """
    if not portfolio:
        return 0.0

    holdings = portfolio.get("holdings", portfolio)
    weights = []

    for value in holdings.values():
        if isinstance(value, Mapping):
            weight = value.get("allocation_pct", value.get("weight", 0.0))
        else:
            weight = value

        try:
            weight = float(weight)
        except (TypeError, ValueError):
            continue

        if weight > 1.0:
            weight /= 100.0

        if weight > 0:
            weights.append(weight)

    return round(sum(weight ** 2 for weight in weights), 4)


def classify_hhi(hhi: float) -> str:
    if hhi < 0.15:
        return "LOW"
    if hhi < 0.25:
        return "MODERATE"
    return "HIGH"


def start_timer() -> float:
    return time.perf_counter()


def stop_timer(start_time: float) -> float:
    return round((time.perf_counter() - start_time) * 1000, 2)


def create_telemetry(
    start_time: float,
    portfolio: Mapping[str, Any],
    confidence_score: float,
    sources_count: int = 0,
) -> Dict[str, Any]:
    hhi = calculate_portfolio_hhi(portfolio)

    return {
        "execution_latency_ms": stop_timer(start_time),
        "portfolio_risk_concentration_score": hhi,
        "portfolio_concentration_level": classify_hhi(hhi),
        "consensus_confidence_score": round(float(confidence_score), 2),
        "sources_consulted_count": int(sources_count),
    }


def build_session_telemetry(
    start_time: float,
    end_time: float,
    portfolio: Mapping[str, Any],
    confidence_score: float,
    sources_count: int = 0,
) -> Dict[str, Any]:
    hhi = calculate_portfolio_hhi(portfolio)
    elapsed = end_time - start_time

    return {
        "total_pipeline_latency_ms": round(elapsed * 1000, 2),
        "portfolio_risk_concentration_score": hhi,
        "portfolio_concentration_level": classify_hhi(hhi),
        "consensus_confidence_score": round(float(confidence_score), 2),
        "sources_consulted_count": int(sources_count),
        "sub_60s_compliance": elapsed < 60.0,
    }


if __name__ == "__main__":
    signals = {
        "technical": {"ticker": "RELIANCE", "signal": "BULLISH", "confidence": 0.84},
        "fundamental": {"signal": "POSITIVE", "confidence": 0.88},
        "sentiment": {"signal": "POSITIVE", "confidence": 0.80},
    }

    rag = {
        "ticker": "RELIANCE",
        "status": "HEALTHY",
        "sentiment": "POSITIVE",
        "confidence": 0.88,
        "citations": ["EARNINGS_TRANSCRIPT_Q3FY26"],
    }

    for profile_id in ("p_conservative", "p_aggressive"):
        result = apply_persona(signals, rag, profile_id)
        print(profile_id, "=>", result["recommendation"], result["confidence_score"])

    print(
        "HHI:",
        calculate_portfolio_hhi(
            {
                "holdings": {
                    "RELIANCE": {"allocation_pct": 50},
                    "TCS": {"allocation_pct": 30},
                    "HDFC": {"allocation_pct": 20},
                }
            }
        ),
    )
