from agents.persona_telemetry import (
    apply_persona,
    calculate_portfolio_hhi,
    fetch_user_profile,
)


def test_profiles_exist():
    assert fetch_user_profile("p_conservative")["risk_tolerance"] == "CONSERVATIVE"
    assert fetch_user_profile("p_aggressive")["risk_tolerance"] == "AGGRESSIVE"


def test_hhi():
    portfolio = {
        "holdings": {
            "RELIANCE": {"allocation_pct": 50},
            "TCS": {"allocation_pct": 30},
            "HDFC": {"allocation_pct": 20},
        }
    }

    assert calculate_portfolio_hhi(portfolio) == 0.38


def test_persona_divergence():
    signals = {
        "technical": {
            "ticker": "RELIANCE",
            "signal": "BULLISH",
            "confidence": 0.84,
        },
        "fundamental": {
            "signal": "NEUTRAL",
            "confidence": 0.65,
        },
        "sentiment": {
            "signal": "BULLISH",
            "confidence": 0.80,
        },
    }

    rag = {
        "ticker": "RELIANCE",
        "status": "HEALTHY",
        "sentiment": "POSITIVE",
        "confidence": 0.88,
        "citations": ["TEST_FINANCIAL_DOCUMENT"],
    }

    conservative = apply_persona(
        signals,
        rag,
        "p_conservative"
    )

    aggressive = apply_persona(
        signals,
        rag,
        "p_aggressive"
    )

    assert conservative["recommendation"] in {
        "BUY",
        "HOLD",
        "HOLD_MAX_CAPACITY_REACHED",
    }

    assert aggressive["recommendation"] in {
        "BUY",
        "HOLD",
        "HOLD_MAX_CAPACITY_REACHED",
    }

    assert conservative["weights"] != aggressive["weights"]


if __name__ == "__main__":
    test_profiles_exist()
    test_hhi()
    test_persona_divergence()
    print("Member 4 tests passed.")
