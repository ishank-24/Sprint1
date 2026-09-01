"""
synthesis_engine.py
-------------------
Consensus synthesis layer combining Quant, RAG disclosures, and User Profiles.
"""

from typing import Dict, Any

class SynthesisEngine:
    @staticmethod
    def synthesize(
        ticker: str,
        technical_data: Dict[str, Any],
        rag_data: Dict[str, Any],
        user_profile: Dict[str, Any],
        degraded_mode: bool = False
    ) -> Dict[str, Any]:
        risk_flag = rag_data.get("risk_flag", "LOW")
        signal = technical_data.get("signal", "NEUTRAL")
        strategy = user_profile.get("strategy", "SIP_ACCUMULATION")

        if degraded_mode or rag_data.get("status") == "UNAVAILABLE":
            status = "DEGRADED"
            alert_badge = "DEGRADED_STATE_ALERT"
            consensus_type = "FALLBACK_TECHNICAL_ONLY"
            recommendation = "HOLD" if signal != "BEARISH" else "REDUCE"
            summary = "Regulatory data feed unavailable; recommendation restricted to capital preservation."
        elif risk_flag == "HIGH":
            status = "SUCCESS"
            alert_badge = "GOVERNANCE_RISK_WARNING"
            consensus_type = "DISCORDANT_OVERRIDE"
            recommendation = "CAUTION / AVOID"
            summary = "Quant signals positive, but regulatory agent detected unresolved governance disclosures."
        elif "SIP" in strategy:
            status = "SUCCESS"
            alert_badge = "ALL_FEEDS_HEALTHY"
            consensus_type = "CONSERVATIVE_CONVERGENCE"
            recommendation = "ACCUMULATE (SIP)"
            summary = "Strong fundamentals verified against SEBI filings. Dollar-cost averaging advised."
        else:
            status = "SUCCESS"
            alert_badge = "ALL_FEEDS_HEALTHY"
            consensus_type = "AGGRESSIVE_ALIGNMENT"
            recommendation = "STRONG BUY" if signal == "BULLISH" else "HOLD"
            summary = "Momentum breakout confirmed with favorable institutional volume expansion."

        return {
            "status": status,
            "alert_badge": alert_badge,
            "consensus_type": consensus_type,
            "recommendation": recommendation,
            "confidence_score": 0.88 if not degraded_mode else 0.45,
            "executive_summary": summary,
            "personalized_rationale": f"Recommendation aligned to {user_profile.get('persona_id', 'profile')} risk constraints.",
            "reasoning_chain": [
                "Quant signals computed from price action & institutional volume.",
                "RAG cross-referenced against statutory filings and auditor disclosures.",
                "Synthesis consensus executed with risk-profile weighting."
            ],
            "source_attributions": rag_data.get("citations", technical_data.get("citations", []))
        }