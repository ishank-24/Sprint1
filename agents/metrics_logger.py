"""
metrics_logger.py
-----------------
Captures session performance metrics required by the hackathon rubric:
1. Total agent response latency (ms) & individual sub-agent latencies
2. Portfolio risk concentration impact score (Pre vs Post transaction)
3. Data completeness & consensus confidence metrics
"""

from typing import Dict, Any, List
import time
from datetime import datetime, timezone


class SessionMetricsLogger:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def record_session(
        self,
        session_id: str,
        ticker: str,
        persona_id: str,
        degraded_mode: bool,
        start_time: float,
        end_time: float,
        agent_latencies_ms: Dict[str, float],
        consensus_confidence: float,
        portfolio_impact: Dict[str, Any]
    ) -> Dict[str, Any]:
        total_latency_ms = round((end_time - start_time) * 1000, 2)
        
        metric_record = {
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticker": ticker.upper(),
            "persona_id": persona_id,
            "degraded_mode": degraded_mode,
            "metrics": {
                # Metric 1: Latencies
                "total_pipeline_latency_ms": total_latency_ms,
                "agent_latencies_ms": agent_latencies_ms,
                "sub_60s_compliance": total_latency_ms < 60000.0,
                
                # Metric 2: Portfolio Risk Concentration Impact Score
                "portfolio_risk_concentration_score": portfolio_impact.get("risk_concentration_score", 0.0),
                "portfolio_exposure_delta_pct": portfolio_impact.get("exposure_delta_pct", 0.0),
                "concentration_flag": portfolio_impact.get("concentration_flag", "NORMAL"),
                
                # Metric 3: Data Completeness & Confidence Score
                "consensus_confidence_score": round(consensus_confidence, 2),
                "data_completeness_score": 0.50 if degraded_mode else 1.0,
                "sources_consulted_count": portfolio_impact.get("sources_count", 0)
            }
        }
        
        self.logs.append(metric_record)
        return metric_record


# Global shared instance
session_logger = SessionMetricsLogger()
