"""
orchestrator.py
---------------
Main Multi-Agent Financial Intelligence Orchestrator (Member 1 Lead).

Tasks handled:
1. Orchestrates Member 2 (Technicals), Member 3 (RAG/SEBI), and Member 4 (User Risk Profile) concurrently.
2. Implements Synthesis Prompt / Consensus Logic comparing technicals vs RAG disclosures.
3. Implements Degraded-State Simulation (degraded_mode=True/False) with graceful fallback & alert badge.
4. Generates performance telemetry log (Latencies, Portfolio Risk Impact, Confidence).
5. Exposes the primary deliverable:
       run_pipeline(ticker: str, persona_id: str, degraded_mode: bool = False) -> Dict[str, Any]
"""

import time
import uuid
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from member_interfaces import (
    TechnicalAgentContract,
    RagAgentContract,
    UserProfileAgentContract
)
from synthesis_engine import SynthesisEngine
from metrics_logger import session_logger
from persona_telemetry import calculate_portfolio_hhi

class FinancialIntelligenceOrchestrator:
    """
    Central orchestration engine coordinating specialized agents.
    """

    def __init__(self, technical_provider=None, rag_provider=None, profile_provider=None):
        # Pluggable providers: easily swap default mock contracts with Member 2, 3, 4 actual code!
        self.technical_provider = technical_provider or TechnicalAgentContract.analyze
        self.rag_provider = rag_provider or RagAgentContract.query
        self.profile_provider = profile_provider or UserProfileAgentContract.get_profile

    def execute_pipeline(
        self,
        ticker: str,
        persona_id: str,
        degraded_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the multi-agent pipeline with asynchronous sub-agent dispatch.
        """
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        start_time = time.perf_counter()
        agent_latencies: Dict[str, float] = {}

        # 1. Concurrently Dispatch Sub-Agents (Member 2, Member 3, Member 4)
        tech_result = {}
        rag_result = {}
        profile_result = {}

        def fetch_technicals():
            t0 = time.perf_counter()
            res = self.technical_provider(ticker, degraded=degraded_mode)
            lat = round((time.perf_counter() - t0) * 1000, 2)
            return "technical", res, lat

        def fetch_rag():
            t0 = time.perf_counter()
            res = self.rag_provider(ticker, degraded=degraded_mode)
            lat = round((time.perf_counter() - t0) * 1000, 2)
            return "rag", res, lat

        def fetch_profile():
            t0 = time.perf_counter()
            res = self.profile_provider(persona_id)
            lat = round((time.perf_counter() - t0) * 1000, 2)
            return "profile", res, lat

        # Dispatch via ThreadPoolExecutor for concurrent execution
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_agent = {
                executor.submit(fetch_technicals): "technical",
                executor.submit(fetch_rag): "rag",
                executor.submit(fetch_profile): "profile"
            }

            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    name, data, latency_ms = future.result()
                    agent_latencies[name] = latency_ms
                    if name == "technical":
                        tech_result = data
                    elif name == "rag":
                        rag_result = data
                    elif name == "profile":
                        profile_result = data
                except Exception as ex:
                    # Fail-safe catch for unhandled exceptions in member modules
                    agent_latencies[agent_name] = 0.0
                    if agent_name == "rag":
                        rag_result = {
                            "agent": "RegulatoryRagAgent",
                            "status": "UNAVAILABLE",
                            "sentiment": "UNKNOWN",
                            "document_chunks": [],
                            "citations": [],
                            "error": str(ex)
                        }
                    elif agent_name == "technical":
                        tech_result = {
                            "agent": "TechnicalAnalysisAgent",
                            "status": "ERROR",
                            "signal": "NEUTRAL",
                            "confidence": 0.3,
                            "citations": []
                        }
                    elif agent_name == "profile":
                        profile_result = UserProfileAgentContract.get_profile("moderate")

        # 2. Synthesis Prompt / Consensus Logic
        synthesis = SynthesisEngine.synthesize(
            ticker=ticker,
            technical_data=tech_result,
            rag_data=rag_result,
            user_profile=profile_result,
            degraded_mode=degraded_mode
        )

        # 3. Calculate Portfolio Impact Score
        portfolio = profile_result.get("current_portfolio", {})
        holdings = portfolio.get("holdings", {})
        current_alloc = holdings.get(ticker.upper(), {}).get("allocation_pct", 0.0)
        max_allowed = profile_result.get("max_single_stock_allocation_pct", 10.0)
        
        # Calculate HHI portfolio concentration metric
portfolio_hhi = calculate_portfolio_hhi(portfolio)

portfolio_impact = {
    "risk_concentration_score": portfolio_hhi,
    "portfolio_hhi": portfolio_hhi,
    "current_allocation_pct": current_alloc,
    "max_allowed_allocation_pct": max_allowed,
    "concentration_flag": "OVER_LIMIT" if current_alloc >= max_allowed else "HEALTHY",
    "sources_count": len(synthesis.get("source_attributions", []))
}

        # 4. Session Metrics Logging
        end_time = time.perf_counter()
        session_metric = session_logger.record_session(
            session_id=session_id,
            ticker=ticker,
            persona_id=persona_id,
            degraded_mode=degraded_mode,
            start_time=start_time,
            end_time=end_time,
            agent_latencies_ms=agent_latencies,
            consensus_confidence=synthesis.get("confidence_score", 0.5),
            portfolio_impact=portfolio_impact
        )

        # 5. Build Complete Master Response Dictionary
        response = {
            "session_id": session_id,
            "pipeline_status": synthesis.get("status"),
            "alert_badge": synthesis.get("alert_badge"),
            "ticker": ticker.upper(),
            "persona_id": persona_id,
            "degraded_mode": degraded_mode,
            
            # Agent Inputs Received
            "agent_inputs": {
                "technical_agent": tech_result,
                "regulatory_rag_agent": rag_result,
                "user_profile_agent": profile_result
            },
            
            # Synthesized Intelligence & Action
            "synthesized_intelligence": {
                "consensus_type": synthesis.get("consensus_type"),
                "recommendation": synthesis.get("recommendation"),
                "confidence_score": synthesis.get("confidence_score"),
                "executive_summary": synthesis.get("executive_summary"),
                "personalized_rationale": synthesis.get("personalized_rationale"),
                "reasoning_chain": synthesis.get("reasoning_chain")
            },
            
            # Source Attribution
            "source_attributions": synthesis.get("source_attributions"),
            
            # Session Metrics (3+ Required Metrics)
            "performance_metrics": session_metric["metrics"]
        }

        return response


# Global orchestrator instance
_orchestrator_instance = FinancialIntelligenceOrchestrator()


def run_pipeline(ticker: str, persona_id: str, degraded_mode: bool = False) -> Dict[str, Any]:
    """
    Official Deliverable Function for Member 1:
    
    Parameters:
      - ticker (str): e.g. "RELIANCE", "TCS", "HDFCBANK"
      - persona_id (str): e.g. "p_conservative", "p_aggressive", "p_moderate"
      - degraded_mode (bool): If True, simulates upstream network/RAG outages and produces graceful fallback.
      
    Returns:
      - Complete Python dict containing agent signals, synthesized recommendation, citations, and metrics.
    """
    return _orchestrator_instance.execute_pipeline(
        ticker=ticker,
        persona_id=persona_id,
        degraded_mode=degraded_mode
    )


if __name__ == "__main__":
    import json
    print("=" * 70)
    print("RUNNING STANDALONE ORCHESTRATOR DEMO (MEMBER 1 DELIVERABLE)")
    print("=" * 70)
    
    # Test 1: Normal Execution
    print("\n[TEST 1: Normal Execution - RELIANCE with Conservative Persona]")
    res1 = run_pipeline("RELIANCE", "p_conservative", degraded_mode=False)
    print(f"Status: {res1['pipeline_status']}")
    print(f"Recommendation: {res1['synthesized_intelligence']['recommendation']}")
    print(f"Confidence: {res1['synthesized_intelligence']['confidence_score']}")
    print(f"Summary: {res1['synthesized_intelligence']['executive_summary']}")
    print(f"Attributions: {res1['source_attributions']}")
    print(f"Latency: {res1['performance_metrics']['total_pipeline_latency_ms']} ms")
    
    # Test 2: Degraded Mode Execution
    print("\n[TEST 2: Degraded State Simulation - RELIANCE with degraded_mode=True]")
    res2 = run_pipeline("RELIANCE", "p_conservative", degraded_mode=True)
    print(f"Status: {res2['pipeline_status']}")
    print(f"Alert Badge: {res2['alert_badge']}")
    print(f"Recommendation: {res2['synthesized_intelligence']['recommendation']}")
    print(f"Summary: {res2['synthesized_intelligence']['executive_summary']}")
    print(f"Data Completeness: {res2['performance_metrics']['data_completeness_score']}")

