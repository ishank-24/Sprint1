"""
member_interfaces.py
--------------------
Standardized Interface Contracts & Default/Mock Implementations for:
- Member 2: Technical & Market Data Analysis Agent
- Member 3: Fundamentals & Regulatory RAG Agent (SEBI/Earnings)
- Member 4: Behavioral Profiling & Risk Management Agent

Member 1's orchestrator uses these interfaces to dispatch parallel calls
and gracefully degrade if real services fail or when degraded_mode is toggled.
"""

from typing import Dict, Any, List, Optional
import time


# ==========================================
# 1. MEMBER 2: Technical & Market Data Agent
# ==========================================
class TechnicalAgentContract:
    """
    Contract for Member 2:
    Evaluates real-time price, volume anomalies, momentum, and technical indicators (RSI, MACD, Moving Averages).
    """

    @staticmethod
    def analyze(ticker: str, degraded: bool = False) -> Dict[str, Any]:
        """
        Returns structured technical signal classification.
        """
        if degraded:
            # Simulated partial feed / delayed data
            return {
                "agent": "TechnicalAnalysisAgent",
                "ticker": ticker.upper(),
                "status": "DEGRADED",
                "signal": "NEUTRAL",
                "confidence": 0.40,
                "price": 1420.50,
                "indicators": {
                    "rsi_14": 51.2,
                    "macd_status": "DATA_UNAVAILABLE",
                    "sma_50_200": "NEUTRAL",
                    "volume_surge_ratio": 1.0
                },
                "key_observations": [
                    "Technical feed delayed by >15 mins.",
                    "Volume anomaly detector unavailable in fallback mode."
                ],
                "citations": ["NSE_PRICE_CACHE_SIMULATED"]
            }

        # Mock high-fidelity standard response
        ticker_upper = ticker.upper()
        if "RELIANCE" in ticker_upper or "RELI" in ticker_upper:
            return {
                "agent": "TechnicalAnalysisAgent",
                "ticker": "RELIANCE",
                "status": "HEALTHY",
                "signal": "BULLISH",
                "confidence": 0.84,
                "price": 2980.50,
                "indicators": {
                    "rsi_14": 62.4,
                    "macd_status": "BULLISH_CROSSOVER",
                    "sma_50_200": "GOLDEN_CROSS",
                    "volume_surge_ratio": 1.78
                },
                "key_observations": [
                    "Strong momentum with 1.78x average 20-day volume surge.",
                    "MACD line crossed above signal line on 1D timeframe.",
                    "Price trading 4.2% above 50-day EMA support."
                ],
                "citations": ["NSE_LIVE_TICK_FEED", "TECHNICAL_INDICATOR_ENGINE_V1"]
            }
        elif "TCS" in ticker_upper:
            return {
                "agent": "TechnicalAnalysisAgent",
                "ticker": "TCS",
                "status": "HEALTHY",
                "signal": "BEARISH",
                "confidence": 0.72,
                "price": 3840.10,
                "indicators": {
                    "rsi_14": 38.5,
                    "macd_status": "BEARISH_DIVERGENCE",
                    "sma_50_200": "TESTING_200_DMA",
                    "volume_surge_ratio": 0.85
                },
                "key_observations": [
                    "RSI trending down towards oversold territory (38.5).",
                    "Volume drying up on pullbacks.",
                    "Approaching key support at 200 DMA (3800 INR)."
                ],
                "citations": ["NSE_LIVE_TICK_FEED", "TECHNICAL_INDICATOR_ENGINE_V1"]
            }
        elif "HDFC" in ticker_upper:
            return {
                "agent": "TechnicalAnalysisAgent",
                "ticker": "HDFCBANK",
                "status": "HEALTHY",
                "signal": "BULLISH",
                "confidence": 0.79,
                "price": 1640.00,
                "indicators": {
                    "rsi_14": 58.0,
                    "macd_status": "POSITIVE_HISTOGRAM",
                    "sma_50_200": "CONSOLIDATING_ABOVE_50DMA",
                    "volume_surge_ratio": 1.35
                },
                "key_observations": [
                    "Consolidation breakout above key resistance at 1625 INR.",
                    "Consistent accumulation by institutional blocks."
                ],
                "citations": ["NSE_LIVE_TICK_FEED", "VOLUME_PROFILE_CLUSTER"]
            }
        else:
            return {
                "agent": "TechnicalAnalysisAgent",
                "ticker": ticker_upper,
                "status": "HEALTHY",
                "signal": "NEUTRAL",
                "confidence": 0.65,
                "price": 1000.00,
                "indicators": {
                    "rsi_14": 50.0,
                    "macd_status": "NEUTRAL",
                    "sma_50_200": "SIDEWAYS_CHANNEL",
                    "volume_surge_ratio": 1.02
                },
                "key_observations": [
                    "Price oscillating within historical Bollinger Bands.",
                    "No immediate breakout or breakdown detected."
                ],
                "citations": ["NSE_LIVE_TICK_FEED"]
            }


# =======================================================
# 2. MEMBER 3: Fundamentals & Regulatory RAG Agent (SEBI)
# =======================================================
class RagAgentContract:
    """
    Contract for Member 3:
    Queries document vector database / filings (SEBI disclosures, Q3/Q4 earnings transcripts, annual reports).
    """

    @staticmethod
    def query(ticker: str, degraded: bool = False) -> Dict[str, Any]:
        """
        Returns grounded RAG disclosures with exact source citations.
        """
        if degraded:
            # Simulated RAG network timeout or empty index lookup
            return {
                "agent": "RegulatoryRagAgent",
                "ticker": ticker.upper(),
                "status": "UNAVAILABLE",
                "sentiment": "UNKNOWN",
                "confidence": 0.0,
                "document_chunks": [],
                "regulatory_alerts": [],
                "error_message": "Vector store connection timed out (RAG feed empty / degraded state triggered).",
                "citations": []
            }

        ticker_upper = ticker.upper()
        if "RELIANCE" in ticker_upper or "RELI" in ticker_upper:
            return {
                "agent": "RegulatoryRagAgent",
                "ticker": "RELIANCE",
                "status": "HEALTHY",
                "sentiment": "POSITIVE",
                "confidence": 0.88,
                "document_chunks": [
                    {
                        "source": "SEBI_DISCLOSURE_REG30_2026_Q1",
                        "date": "2026-01-15",
                        "title": "Material Event: Green Hydrogen Gigafactory Commissioning Phase 1",
                        "snippet": "Reliance Industries announces commercial operations of 5GW electrolyzer manufacturing facility in Jamnagar under PLI scheme.",
                        "relevance_score": 0.94
                    },
                    {
                        "source": "EARNINGS_TRANSCRIPT_Q3FY26",
                        "date": "2026-01-22",
                        "title": "Jio & Retail ARPU Expansion and EBITDA Margin Growth",
                        "snippet": "Consolidated EBITDA grew 11.8% YoY; Jio ARPU reached INR 198.5 with sustained 5G subscriber migration.",
                        "relevance_score": 0.91
                    }
                ],
                "regulatory_alerts": [
                    "No pending SEBI show-cause or insider trading inquiries detected in last 180 days."
                ],
                "citations": [
                    "SEBI_DISCLOSURE_REG30_2026_Q1",
                    "EARNINGS_TRANSCRIPT_Q3FY26_PAGE_14"
                ]
            }
        elif "TCS" in ticker_upper:
            return {
                "agent": "RegulatoryRagAgent",
                "ticker": "TCS",
                "status": "HEALTHY",
                "sentiment": "CAUTIOUS",
                "confidence": 0.76,
                "document_chunks": [
                    {
                        "source": "EARNINGS_CALL_TRANSCRIPT_Q3FY26",
                        "date": "2026-01-12",
                        "title": "Management Guidance on BFSI Discretionary Tech Spend",
                        "snippet": "Management cited elongated decision cycles in US banking and cautious discretionary tech spending despite $8.1B total contract value pipeline.",
                        "relevance_score": 0.89
                    },
                    {
                        "source": "SEBI_INSIDER_TRADING_DISCLOSURE_DEC25",
                        "date": "2025-12-28",
                        "title": "Form C - Continual Disclosure under Regulation 7(2)",
                        "snippet": "Routine ESOP exercise and disposal by senior designated persons within pre-cleared trading window.",
                        "relevance_score": 0.78
                    }
                ],
                "regulatory_alerts": [
                    "Headwind highlighted in discretionary BFSI IT billing rates."
                ],
                "citations": [
                    "EARNINGS_CALL_TRANSCRIPT_Q3FY26_SECTION_3",
                    "SEBI_FORM_C_DEC25"
                ]
            }
        elif "HDFC" in ticker_upper:
            return {
                "agent": "RegulatoryRagAgent",
                "ticker": "HDFCBANK",
                "status": "HEALTHY",
                "sentiment": "CAUTIOUS_NEGATIVE",
                "confidence": 0.82,
                "document_chunks": [
                    {
                        "source": "RBI_COMPLIANCE_FILING_Q3",
                        "date": "2026-01-18",
                        "title": "Credit-to-Deposit (CD) Ratio Normalization Roadmap",
                        "snippet": "Bank maintains guidance to moderate loan growth below deposit accretion to bring CD ratio down from 104% towards 88% target over next 4-6 quarters.",
                        "relevance_score": 0.95
                    },
                    {
                        "source": "SEBI_DISCLOSURE_MERGER_AUDIT",
                        "date": "2025-11-30",
                        "title": "Post-Merger Harmonization of Non-Performing Assets & Provisions",
                        "snippet": "Higher standard asset provisioning on former HDFC Ltd mortgage book temporary compression on NIMs (3.4% vs 3.6% historical).",
                        "relevance_score": 0.87
                    }
                ],
                "regulatory_alerts": [
                    "Regulatory focus on CD ratio discipline; potential near-term Net Interest Margin (NIM) compression."
                ],
                "citations": [
                    "RBI_CD_RATIO_DISCLOSURE_2026",
                    "SEBI_MERGER_AUDIT_NOTE_12"
                ]
            }
        else:
            return {
                "agent": "RegulatoryRagAgent",
                "ticker": ticker_upper,
                "status": "HEALTHY",
                "sentiment": "NEUTRAL",
                "confidence": 0.60,
                "document_chunks": [
                    {
                        "source": "ANNUAL_REPORT_LATEST",
                        "date": "2025-06-30",
                        "title": "General Corporate Disclosures",
                        "snippet": "Standard compliance and balance sheet disclosures within statutory parameters.",
                        "relevance_score": 0.70
                    }
                ],
                "regulatory_alerts": [],
                "citations": ["ANNUAL_REPORT_LATEST"]
            }


# ========================================================
# 3. MEMBER 4: User Behavioral & Risk Profile Agent
# ========================================================
class UserProfileAgentContract:
    """
    Contract for Member 4:
    Retrieves user profile, risk capacity, portfolio exposure, and behavioral biases (e.g. FOMO, loss aversion).
    """

    @staticmethod
    def get_profile(persona_id: str) -> Dict[str, Any]:
        """
        Returns persona parameters, current portfolio holdings, risk tolerance, and behavioral flags.
        """
        persona_lower = str(persona_id).lower()
        if "conservative" in persona_lower or persona_id == "p_conservative":
            return {
                "agent": "UserProfileAgent",
                "persona_id": "conservative_retail_01",
                "user_name": "Ramesh K.",
                "age_bracket": "45-55",
                "risk_tolerance": "CONSERVATIVE",
                "max_single_stock_allocation_pct": 5.0,
                "current_portfolio": {
                    "total_value_inr": 1250000,
                    "cash_pct": 18.0,
                    "holdings": {
                        "RELIANCE": {"allocation_pct": 4.5, "unrealized_pnl_pct": 14.2},
                        "TCS": {"allocation_pct": 6.0, "unrealized_pnl_pct": -3.5},
                        "HDFCBANK": {"allocation_pct": 8.0, "unrealized_pnl_pct": 2.1}
                    }
                },
                "behavioral_traits": {
                    "loss_aversion_index": 0.88,  # High loss aversion
                    "derivatives_allowed": False,
                    "overtrading_risk": "LOW"
                },
                "mandate": "Capital preservation, dividend yield, strict stop-losses, avoid leveraged or volatile instruments."
            }
        elif "aggressive" in persona_lower or "growth" in persona_lower or persona_id == "p_aggressive":
            return {
                "agent": "UserProfileAgent",
                "persona_id": "aggressive_genz_02",
                "user_name": "Aanya S.",
                "age_bracket": "22-29",
                "risk_tolerance": "AGGRESSIVE",
                "max_single_stock_allocation_pct": 15.0,
                "current_portfolio": {
                    "total_value_inr": 350000,
                    "cash_pct": 30.0,
                    "holdings": {
                        "RELIANCE": {"allocation_pct": 2.0, "unrealized_pnl_pct": 8.0},
                        "TCS": {"allocation_pct": 0.0, "unrealized_pnl_pct": 0.0},
                        "ZOMATO": {"allocation_pct": 14.0, "unrealized_pnl_pct": 32.5}
                    }
                },
                "behavioral_traits": {
                    "loss_aversion_index": 0.35,  # High risk capacity
                    "derivatives_allowed": True,
                    "overtrading_risk": "MODERATE_HIGH"
                },
                "mandate": "High capital appreciation, momentum capture, willing to tolerate drawdown for alpha, strict warning on over-leverage."
            }
        else:
            # Default Balanced / Moderate
            return {
                "agent": "UserProfileAgent",
                "persona_id": "moderate_balanced_03",
                "user_name": "Priya M.",
                "age_bracket": "30-40",
                "risk_tolerance": "MODERATE",
                "max_single_stock_allocation_pct": 10.0,
                "current_portfolio": {
                    "total_value_inr": 750000,
                    "cash_pct": 15.0,
                    "holdings": {
                        "RELIANCE": {"allocation_pct": 7.0, "unrealized_pnl_pct": 6.5},
                        "HDFCBANK": {"allocation_pct": 5.0, "unrealized_pnl_pct": -1.2}
                    }
                },
                "behavioral_traits": {
                    "loss_aversion_index": 0.55,
                    "derivatives_allowed": False,
                    "overtrading_risk": "LOW"
                },
                "mandate": "Balanced wealth accumulation with diversification and disciplined risk-adjusted returns."
            }
