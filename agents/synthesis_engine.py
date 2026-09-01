"""
synthesis_engine.py
-------------------
Implements the Multi-Perspective Synthesis & Consensus Engine:
1. Compares Technical Signals (Member 2) against Regulatory RAG Findings (Member 3).
2. Evaluates User Risk Tolerance, Behavioral Biases, & Concentration Limits (Member 4).
3. Detects Convergence vs Divergence / Conflicts.
4. Handles Degraded-State Fallback Reasoning with an explicit Alert Badge.
5. Generates fully cited, retail-friendly, personalized action points.
"""

from typing import Dict, Any, List, Tuple, Optional


class SynthesisEngine:
    """
    Synthesizes signals from technicals, fundamentals/filings, and user profile.
    """

    @classmethod
    def synthesize(
        cls,
        ticker: str,
        technical_data: Dict[str, Any],
        rag_data: Dict[str, Any],
        user_profile: Dict[str, Any],
        degraded_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Main synthesis logic producing final recommendation, reasoning chain, and attribution.
        """
        ticker = ticker.upper()
        
        # 1. Parse Sub-Agent Data
        tech_signal = technical_data.get("signal", "NEUTRAL").upper()
        tech_conf = technical_data.get("confidence", 0.5)
        tech_indicators = technical_data.get("indicators", {})
        
        rag_status = rag_data.get("status", "HEALTHY")
        rag_sentiment = rag_data.get("sentiment", "NEUTRAL").upper()
        rag_chunks = rag_data.get("document_chunks", [])
        rag_alerts = rag_data.get("regulatory_alerts", [])
        
        risk_tolerance = user_profile.get("risk_tolerance", "MODERATE").upper()
        max_alloc_pct = user_profile.get("max_single_stock_allocation_pct", 10.0)
        current_portfolio = user_profile.get("current_portfolio", {})
        holdings = current_portfolio.get("holdings", {})
        current_stock_alloc = holdings.get(ticker, {}).get("allocation_pct", 0.0)
        current_stock_pnl = holdings.get(ticker, {}).get("unrealized_pnl_pct", 0.0)
        derivatives_allowed = user_profile.get("behavioral_traits", {}).get("derivatives_allowed", False)

        # 2. Check Concentration Capacity
        alloc_headroom_pct = max(0.0, max_alloc_pct - current_stock_alloc)
        is_overallocated = current_stock_alloc >= max_alloc_pct

        # Collect citations
        all_citations: List[str] = []
        all_citations.extend(technical_data.get("citations", []))
        all_citations.extend(rag_data.get("citations", []))
        all_citations.append(f"USER_PORTFOLIO_MODEL_{user_profile.get('persona_id', 'DEFAULT')}")

        # 3. Handle Degraded Mode Scenario
        if degraded_mode or rag_status == "UNAVAILABLE" or not rag_chunks:
            return cls._generate_degraded_synthesis(
                ticker=ticker,
                tech_signal=tech_signal,
                tech_conf=tech_conf,
                technical_data=technical_data,
                user_profile=user_profile,
                current_stock_alloc=current_stock_alloc,
                max_alloc_pct=max_alloc_pct,
                is_overallocated=is_overallocated,
                citations=all_citations
            )

        # 4. Standard Multi-Perspective Consensus Logic
        action, consensus_type, confidence, summary, reasoning_chain, retail_alert_badge = cls._resolve_consensus(
            tech_signal=tech_signal,
            tech_conf=tech_conf,
            rag_sentiment=rag_sentiment,
            rag_conf=rag_data.get("confidence", 0.7),
            risk_tolerance=risk_tolerance,
            is_overallocated=is_overallocated,
            current_stock_alloc=current_stock_alloc,
            max_alloc_pct=max_alloc_pct,
            derivatives_allowed=derivatives_allowed,
            ticker=ticker,
            technical_data=technical_data,
            rag_data=rag_data
        )

        return {
            "status": "HEALTHY",
            "alert_badge": retail_alert_badge,
            "ticker": ticker,
            "consensus_type": consensus_type,
            "recommendation": action,
            "confidence_score": confidence,
            "executive_summary": summary,
            "personalized_rationale": {
                "persona_id": user_profile.get("persona_id"),
                "user_name": user_profile.get("user_name"),
                "risk_profile": risk_tolerance,
                "current_allocation_pct": current_stock_alloc,
                "max_allowed_allocation_pct": max_alloc_pct,
                "allocation_headroom_pct": round(alloc_headroom_pct, 2),
                "unrealized_pnl_pct": current_stock_pnl,
                "derivatives_warning": None if derivatives_allowed else "SEBI 2024 Advisory: 89% retail traders lose money in F&O. High-risk derivative setups strictly filtered out for your conservative profile."
            },
            "reasoning_chain": reasoning_chain,
            "source_attributions": list(set(all_citations))
        }

    @classmethod
    def _resolve_consensus(
        cls,
        tech_signal: str,
        tech_conf: float,
        rag_sentiment: str,
        rag_conf: float,
        risk_tolerance: str,
        is_overallocated: bool,
        current_stock_alloc: float,
        max_alloc_pct: float,
        derivatives_allowed: bool,
        ticker: str,
        technical_data: Dict[str, Any],
        rag_data: Dict[str, Any]
    ) -> Tuple[str, str, float, str, List[Dict[str, str]], Optional[str]]:
        """
        Compares signals and applies risk profile rules.
        """
        reasoning_chain = []
        alert_badge = None

        # Step 1: Record Technical Observation
        reasoning_chain.append({
            "stage": "Technical Momentum Assessment",
            "finding": f"Technical indicator score indicates {tech_signal} momentum (Confidence: {int(tech_conf*100)}%). Key factors: {', '.join(technical_data.get('key_observations', []))}",
            "source": ", ".join(technical_data.get("citations", ["NSE_FEEDS"]))
        })

        # Step 2: Record Regulatory / RAG Observation
        rag_doc_snippets = [c.get("snippet", "") for c in rag_data.get("document_chunks", [])]
        reasoning_chain.append({
            "stage": "Regulatory & Disclosure Verification",
            "finding": f"SEBI / Earnings RAG sentiment is {rag_sentiment}. Context: {' '.join(rag_doc_snippets[:1])}",
            "source": ", ".join(rag_data.get("citations", ["SEBI_DISCLOSURES"]))
        })

        # Case A: Alignment (Bullish Technicals + Positive RAG)
        if tech_signal == "BULLISH" and rag_sentiment in ["POSITIVE", "BULLISH"]:
            consensus_type = "SIGNAL_CONVERGENCE"
            blended_conf = round((tech_conf * 0.45) + (rag_conf * 0.55), 2)
            
            if is_overallocated:
                action = "HOLD_MAX_CAPACITY_REACHED"
                alert_badge = "PORTFOLIO_CAP_REACHED"
                summary = f"Strong bullish convergence detected for {ticker}, but your current portfolio allocation ({current_stock_alloc}%) has reached or exceeded your configured limit of {max_alloc_pct}%. We recommend HOLDING existing position without adding new exposure."
            elif risk_tolerance == "CONSERVATIVE":
                action = "ACCUMULATE_STAGGERED"
                summary = f"Positive alignment between technical indicators and recent SEBI disclosures. For your Conservative mandate, accumulate in staggered tranches (SIP-style) to manage entry volatility."
            else: # AGGRESSIVE or MODERATE
                action = "BUY"
                summary = f"Strong multi-agent conviction. Price momentum supported by confirmed corporate disclosures (EBITDA expansion / capacity commissioning)."

        # Case B: Contradiction / Conflict (Bullish Technicals + Cautious/Negative RAG)
        elif tech_signal == "BULLISH" and "CAUTIOUS" in rag_sentiment:
            consensus_type = "SIGNAL_DIVERGENCE_WARNING"
            blended_conf = round(min(tech_conf, rag_conf) * 0.85, 2)
            alert_badge = "CONTRADICTION_ALERT: TECHNICAL_VS_REGULATORY"
            
            action = "CAUTIOUS_HOLD"
            summary = f"DIVERGENCE DETECTED: While short-term price technicals appear bullish, regulatory filings highlight underlying headwinds (e.g. CD ratio discipline / margin compression). Capital safety is prioritized."
            
            reasoning_chain.append({
                "stage": "Conflict Resolution Engine",
                "finding": f"Technical breakout is contradicted by conservative regulatory guidance in recent filings. Overriding aggressive buy signal to prevent retail trap.",
                "source": "ORCHESTRATOR_CONSENSUS_RULESET"
            })

        # Case C: Bearish Technicals + Cautious/Negative RAG
        elif tech_signal == "BEARISH" and "CAUTIOUS" in rag_sentiment:
            consensus_type = "BEARISH_ALIGNMENT"
            blended_conf = round((tech_conf * 0.5) + (rag_conf * 0.5), 2)
            action = "AVOID_OR_TRIM"
            alert_badge = "DOWNSIDE_RISK_ALERT"
            summary = f"Negative alignment: Weak technical momentum accompanied by soft earnings commentary. High risk of further drawdown."

        # Case D: Bearish Technicals + Positive Long-term RAG
        elif tech_signal == "BEARISH" and rag_sentiment in ["POSITIVE", "BULLISH"]:
            consensus_type = "VALUE_DIVERGENCE"
            blended_conf = 0.68
            if risk_tolerance == "AGGRESSIVE":
                action = "ACCUMULATE_ON_DIPS"
                summary = f"Short-term technical pullback against robust corporate fundamentals presents a value accumulation opportunity for growth portfolios."
            else:
                action = "WAIT_FOR_STABILIZATION"
                summary = f"Fundamentals remain solid, but technical selling pressure is active. Conservative mandate dictates waiting for price stabilization before entering."

        # Default Neutral
        else:
            consensus_type = "NEUTRAL_CONSOLIDATION"
            blended_conf = 0.60
            action = "HOLD_MONITOR"
            summary = f"Signals are currently balanced. Maintain watchlist status and monitor next quarterly disclosures."

        # Step 3: Record Persona Alignment Stage
        reasoning_chain.append({
            "stage": "User Risk & Behavioral Optimization",
            "finding": f"Decision filtered for {risk_tolerance} profile. Single-stock allocation: {current_stock_alloc}% / {max_alloc_pct}% max allowed. Action output: {action}.",
            "source": f"USER_PROFILE_AGENT_{risk_tolerance}"
        })

        return action, consensus_type, blended_conf, summary, reasoning_chain, alert_badge

    @classmethod
    def _generate_degraded_synthesis(
        cls,
        ticker: str,
        tech_signal: str,
        tech_conf: float,
        technical_data: Dict[str, Any],
        user_profile: Dict[str, Any],
        current_stock_alloc: float,
        max_alloc_pct: float,
        is_overallocated: bool,
        citations: List[str]
    ) -> Dict[str, Any]:
        """
        Graceful degraded fallback when RAG vector DB or external feeds are down.
        """
        alert_badge = "DEGRADED_STATE_ALERT: RAG_FEED_UNAVAILABLE"
        risk_tolerance = user_profile.get("risk_tolerance", "MODERATE").upper()
        
        # In degraded mode, default to high caution (retail capital safety)
        if tech_signal == "BULLISH" and not is_overallocated:
            if risk_tolerance == "AGGRESSIVE":
                action = "SPECULATIVE_WATCHLIST"
                rec_text = "Technical feed shows positive momentum, but regulatory RAG disclosures could not be verified. Exercise caution."
            else:
                action = "WAIT_FOR_FULL_DATA"
                rec_text = "Market feed available but regulatory grounding is temporarily offline. Action paused to preserve capital."
        else:
            action = "NEUTRAL_HOLD"
            rec_text = "Operating under degraded data mode. Maintain current allocations until full filing verification is restored."

        reasoning_chain = [
            {
                "stage": "Degraded State Interceptor",
                "finding": "Regulatory RAG / Document store is unreachable. Invoking fail-safe fallback logic without pipeline crash.",
                "source": "PIPELINE_ORCHESTRATOR_DEGRADED_FAILSAFE"
            },
            {
                "stage": "Partial Technical Assessment",
                "finding": f"Relying on cached/available technical signals ({tech_signal}, Conf: {tech_conf}).",
                "source": ", ".join(technical_data.get("citations", ["NSE_PRICE_FEED"]))
            },
            {
                "stage": "Retail Protection Filter",
                "finding": "Aggressive buy recommendations automatically disabled while regulatory filings cannot be cross-referenced.",
                "source": "SAFETY_RULESET_SEBI_PROTECTION"
            }
        ]

        return {
            "status": "DEGRADED_OPERATIONAL",
            "alert_badge": alert_badge,
            "ticker": ticker,
            "consensus_type": "DEGRADED_FALLBACK",
            "recommendation": action,
            "confidence_score": round(tech_conf * 0.6, 2), # Penalize confidence due to missing RAG
            "executive_summary": rec_text,
            "personalized_rationale": {
                "persona_id": user_profile.get("persona_id"),
                "user_name": user_profile.get("user_name"),
                "risk_profile": risk_tolerance,
                "current_allocation_pct": current_stock_alloc,
                "max_allowed_allocation_pct": max_alloc_pct,
                "degradation_notice": "Output generated without SEBI / Earnings RAG verification. Confidence discounted by 40%."
            },
            "reasoning_chain": reasoning_chain,
            "source_attributions": [c for c in citations if c]
        }
