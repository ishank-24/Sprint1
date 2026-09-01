"""
persona_telemetry.py
--------------------
Telemetry & Herfindahl-Hirschman Index (HHI) portfolio concentration calculations.
"""

from typing import Dict, Any

def calculate_portfolio_hhi(portfolio: Dict[str, Any]) -> float:
    """Calculates normalized HHI concentration metric (0.0 to 1.0)."""
    holdings = portfolio.get("holdings", {})
    if not holdings:
        return 0.15
    total_shares_sq = sum((h.get("allocation_pct", 0) / 100) ** 2 for h in holdings.values())
    return round(float(total_shares_sq), 2)