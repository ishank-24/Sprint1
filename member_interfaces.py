"""
member_interfaces.py
--------------------
Fallback and contract interfaces for sub-agent modules (Members 2, 3, 4).
"""

from typing import Dict, Any

class TechnicalAgentContract:
    @staticmethod
    def analyze(ticker: str, degraded: bool = False) -> Dict[str, Any]:
        rsi_val = 64.2 if "RELIANCE" in ticker else (71.6 if "TATA" in ticker else 48.3)
        return {
            "agent": "TechnicalAnalysisAgent",
            "status": "HEALTHY" if not degraded else "DEGRADED",
            "signal": "BULLISH" if rsi_val >= 55 else "NEUTRAL",
            "confidence": 0.85 if not degraded else 0.45,
            "rsi": rsi_val,
            "volume_multiplier": 2.4,
            "fii_dii_flow_cr": 1420.0,
            "citations": [f"NSE Technical Feed 15m Candles ({ticker})"]
        }

class RagAgentContract:
    @staticmethod
    def query(ticker: str, degraded: bool = False) -> Dict[str, Any]:
        if degraded:
            return {
                "agent": "RegulatoryRagAgent",
                "status": "UNAVAILABLE",
                "sentiment": "UNKNOWN",
                "risk_flag": "UNKNOWN",
                "document_chunks": [],
                "citations": ["SEBI Feed Offline - Last local cache T-1"]
            }
        return {
            "agent": "RegulatoryRagAgent",
            "status": "HEALTHY",
            "sentiment": "POSITIVE",
            "risk_flag": "LOW",
            "document_chunks": ["Capex allocations supported by core operations."],
            "citations": [f"SEBI Reg-30 Filing & Transcript ({ticker}), Page 14"]
        }

class UserProfileAgentContract:
    @staticmethod
    def get_profile(persona_id: str) -> Dict[str, Any]:
        is_conservative = "conservative" in str(persona_id).lower()
        return {
            "persona_id": persona_id,
            "risk_tolerance": "LOW" if is_conservative else "HIGH",
            "strategy": "SIP_ACCUMULATION" if is_conservative else "MOMENTUM_ALPHA",
            "max_single_stock_allocation_pct": 10.0 if is_conservative else 25.0,
            "current_portfolio": {
                "holdings": {
                    "RELIANCE": {"allocation_pct": 8.5},
                    "TATAMOTORS": {"allocation_pct": 4.0}
                }
            }
        }