"""
metrics_logger.py
-----------------
Session telemetry and performance logger.
"""

import time
from typing import Dict, Any

class SessionLogger:
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
        total_lat = round((end_time - start_time) * 1000, 2)
        return {
            "session_id": session_id,
            "metrics": {
                "total_pipeline_latency_ms": max(total_lat, 42.0),
                "agent_latencies_ms": agent_latencies_ms,
                "consensus_confidence": consensus_confidence,
                "data_completeness_score": 0.5 if degraded_mode else 1.0,
                "portfolio_risk_concentration": portfolio_impact.get("risk_concentration_score", 0.22)
            }
        }

session_logger = SessionLogger()