"""
test_orchestrator.py
--------------------
Automated Test & Demonstration Suite for Member 1 Deliverables:
1. Normal Multi-Agent Execution (RELIANCE + Conservative Persona)
2. Behavioral Profiling Divergence (Identical Market Inputs -> Different Persona Outputs)
3. Signal Contradiction / Conflict Handling (Bullish Technicals vs Cautious Filings)
4. Degraded-State Simulation (degraded_mode=True / RAG Outage -> Graceful Fallback + Alert Badge)
5. Session Telemetry & Performance Metric Auditing (3+ Metrics)
"""

import unittest
import json
import time
from orchestrator import run_pipeline, FinancialIntelligenceOrchestrator
from metrics_logger import session_logger


class TestMember1Orchestrator(unittest.TestCase):

    def test_01_normal_pipeline_execution(self):
        """Test standard multi-agent execution with healthy signals."""
        result = run_pipeline(ticker="RELIANCE", persona_id="p_conservative", degraded_mode=False)
        
        self.assertIn("session_id", result)
        self.assertEqual(result["pipeline_status"], "HEALTHY")
        self.assertEqual(result["ticker"], "RELIANCE")
        
        # Verify synthesized intelligence
        synth = result["synthesized_intelligence"]
        self.assertIn(synth["recommendation"], ["BUY", "ACCUMULATE_STAGGERED", "HOLD_MAX_CAPACITY_REACHED"])
        self.assertGreaterEqual(synth["confidence_score"], 0.70)
        self.assertIsNotNone(synth["executive_summary"])
        self.assertTrue(len(synth["reasoning_chain"]) >= 3)
        
        # Verify citations are present and non-empty
        citations = result["source_attributions"]
        self.assertTrue(len(citations) >= 2)
        print("\n[TEST 1 PASSED] Standard Pipeline Execution Successful.")
        print(f"  Recommendation: {synth['recommendation']}")
        print(f"  Citations: {citations}")

    def test_02_persona_divergence_on_identical_inputs(self):
        """
        Hackathon Requirement:
        Demonstrably producing different outputs for different user profiles on identical market inputs.
        """
        ticker = "RELIANCE"
        res_conservative = run_pipeline(ticker=ticker, persona_id="p_conservative", degraded_mode=False)
        res_aggressive = run_pipeline(ticker=ticker, persona_id="p_aggressive", degraded_mode=False)
        
        rec_cons = res_conservative["synthesized_intelligence"]["recommendation"]
        rec_aggr = res_aggressive["synthesized_intelligence"]["recommendation"]
        
        rat_cons = res_conservative["synthesized_intelligence"]["personalized_rationale"]
        rat_aggr = res_aggressive["synthesized_intelligence"]["personalized_rationale"]
        
        # Verify personas produced distinct customized directives
        self.assertNotEqual(rat_cons["risk_profile"], rat_aggr["risk_profile"])
        self.assertEqual(rat_cons["risk_profile"], "CONSERVATIVE")
        self.assertEqual(rat_aggr["risk_profile"], "AGGRESSIVE")
        
        # Conservative gets staggered/capital-preservation advice while Aggressive gets direct aggressive BUY
        print(f"\n[TEST 2 PASSED] Persona Divergence Verified on {ticker}:")
        print(f"  Conservative Output ({rat_cons['user_name']}): {rec_cons} | Mandate Cap: {rat_cons['max_allowed_allocation_pct']}%")
        print(f"  Aggressive Output   ({rat_aggr['user_name']}): {rec_aggr} | Mandate Cap: {rat_aggr['max_allowed_allocation_pct']}%")

    def test_03_signal_contradiction_handling(self):
        """
        Hackathon Requirement:
        Detects conflicts (e.g. Bullish price momentum contradicted by SEBI/regulatory headwinds).
        """
        result = run_pipeline(ticker="HDFCBANK", persona_id="p_moderate", degraded_mode=False)
        synth = result["synthesized_intelligence"]
        
        # HDFC Bank has Bullish technicals but Cautious regulatory disclosures (RBI CD ratio & NIM pressure)
        self.assertIn("DIVERGENCE", synth["consensus_type"])
        self.assertIn("CAUTIOUS", synth["recommendation"])
        self.assertIsNotNone(result["alert_badge"])
        self.assertIn("CONTRADICTION", result["alert_badge"])
        
        print("\n[TEST 3 PASSED] Signal Contradiction Resolution Verified:")
        print(f"  Consensus Type: {synth['consensus_type']}")
        print(f"  Alert Badge: {result['alert_badge']}")
        print(f"  Executive Summary: {synth['executive_summary']}")

    def test_04_degraded_state_simulation_no_crash(self):
        """
        Hackathon Requirement:
        Graceful handling of degraded-data scenario with alert badge without crashing.
        """
        # Execute with degraded_mode=True
        result = run_pipeline(ticker="RELIANCE", persona_id="p_conservative", degraded_mode=True)
        
        self.assertEqual(result["degraded_mode"], True)
        self.assertEqual(result["pipeline_status"], "DEGRADED_OPERATIONAL")
        self.assertIsNotNone(result["alert_badge"])
        self.assertIn("DEGRADED_STATE_ALERT", result["alert_badge"])
        
        # Verify fallback recommendation exists and confidence is penalized
        synth = result["synthesized_intelligence"]
        self.assertIn(synth["recommendation"], ["WAIT_FOR_FULL_DATA", "NEUTRAL_HOLD", "SPECULATIVE_WATCHLIST"])
        self.assertLessEqual(synth["confidence_score"], 0.65)
        
        # Verify no uncited outputs (technical cache citation remains intact)
        self.assertTrue(len(result["source_attributions"]) > 0)
        
        # Verify performance metric reflects degraded completeness
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["data_completeness_score"], 0.50)
        
        print("\n[TEST 4 PASSED] Degraded State Graceful Fallback Verified:")
        print(f"  Pipeline Status: {result['pipeline_status']}")
        print(f"  Alert Badge: {result['alert_badge']}")
        print(f"  Fallback Recommendation: {synth['recommendation']}")
        print(f"  Data Completeness: {metrics['data_completeness_score']}")

    def test_05_performance_metrics_logging(self):
        """
        Hackathon Requirement:
        A performance log capturing at least three measurable metrics per session.
        """
        result = run_pipeline(ticker="TCS", persona_id="p_conservative", degraded_mode=False)
        metrics = result["performance_metrics"]
        
        # Metric 1: Latencies (<60s retail compliance)
        self.assertIn("total_pipeline_latency_ms", metrics)
        self.assertIn("agent_latencies_ms", metrics)
        self.assertTrue(metrics["sub_60s_compliance"])
        
        # Metric 2: Portfolio Risk Concentration Impact Score
        self.assertIn("portfolio_risk_concentration_score", metrics)
        self.assertIn("concentration_flag", metrics)
        
        # Metric 3: Consensus Confidence & Completeness
        self.assertIn("consensus_confidence_score", metrics)
        self.assertIn("data_completeness_score", metrics)
        
        print("\n[TEST 5 PASSED] Performance Telemetry Verified (3+ Required Metrics):")
        print(f"  1. Total Pipeline Latency: {metrics['total_pipeline_latency_ms']} ms (Sub-60s: {metrics['sub_60s_compliance']})")
        print(f"  2. Portfolio Risk Concentration: {metrics['portfolio_risk_concentration_score']} ({metrics['concentration_flag']})")
        print(f"  3. Consensus Confidence: {metrics['consensus_confidence_score']} | Completeness: {metrics['data_completeness_score']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
