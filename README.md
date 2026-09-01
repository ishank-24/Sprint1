# Sprint1
# Multi-Agent Autonomous Financial Intelligence System (PS-01)
## Sourav: Pipeline Orchestrator & Degraded-Mode Lead Prototype

This directory contains the complete prototype implementation for **Sourav (Pipeline Orchestrator & Degraded-Mode Lead)** for the IEEE RAS Hackverse Hackathon (VIT Chennai).

---

## 👥 Team Roles & Module Mapping

| Name | Role | Core Deliverable File | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Sourav** | Pipeline Orchestrator & Synthesis Engine | `orchestrator.py`, `agents/synthesis_engine.py` | Signal consensus, degraded-mode fail-safes, latency & risk telemetry |
| **Parv** | Quant, Technicals & Signal Agent | `agents/quant_agent.py` | Technical indicators, trend calculations, momentum signals |
| **Utsav** | Regulatory, Earnings Transcript & RAG Agent | `agents/rag_agent.py` | FAISS vector indexing, SEBI disclosures, transcript chunking |
| **Madhav** | Behavioral Profiling & Risk Telemetry | `agents/persona_telemetry.py` | Investor risk scoring, portfolio concentration limits, F&O filters |
| **Ishank** | Streamlit UI & Dashboard | `app.py` | Visual dashboard, decision trees, dynamic alert banners, citations |

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- **Python:** 3.9, 3.10, or 3.11 installed.
- **Git:** Installed on your system.

### 2. Installation & Setup
Open your terminal (or VS Code Terminal) and run:

`git clone https://github.com/ishank-24/Sprint1.git`  
`cd Sprint1`  
`pip install -r requirements.txt`  

---

### 3. Execution & Running the App

#### Running the Interactive Streamlit UI (Ishank)
To launch the frontend dashboard in your browser:  
`streamlit run app.py`  
*(The app will automatically open at http://localhost:8501)*

#### Running the Automated Test Suite (Evaluator Scenarios)
To verify end-to-end multi-agent execution, persona divergence, and degraded fallback handling:  
`python test_orchestrator.py`  

---

## 🚀 Key Deliverable
The primary deliverable function usage:

* **Function:** `run_pipeline(ticker="RELIANCE", persona_id="p_conservative", degraded_mode=False)`
* **Module:** `from orchestrator import run_pipeline`

### Output Schema:
`run_pipeline` returns a comprehensive Python dictionary containing:
1. **`pipeline_status`**: `"HEALTHY"` or `"DEGRADED_OPERATIONAL"`
2. **`alert_badge`**: Dynamic alert banner (e.g., `None`, `"CONTRADICTION_ALERT: TECHNICAL_VS_REGULATORY"`, or `"DEGRADED_STATE_ALERT: RAG_FEED_UNAVAILABLE"`)
3. **`synthesized_intelligence`**:
   - `consensus_type`: Multi-perspective consensus classification (`SIGNAL_CONVERGENCE`, `SIGNAL_DIVERGENCE_WARNING`, `VALUE_DIVERGENCE`, etc.)
   - `recommendation`: Actionable guidance (`BUY`, `ACCUMULATE_STAGGERED`, `CAUTIOUS_HOLD`, `AVOID_OR_TRIM`, etc.)
   - `confidence_score`: Blended conviction score between 0.0 and 1.0
   - `executive_summary`: Concise summary accessible in under 60 seconds
   - `personalized_rationale`: Breakdown with persona allocation limit, headroom, and SEBI retail F&O safeguards
   - `reasoning_chain`: Step-by-step transparent justification traceable to source evidence
4. **`source_attributions`**: List of all cited disclosures (e.g., `NSE_LIVE_TICK_FEED`, `SEBI_DISCLOSURE_REG30`, `EARNINGS_TRANSCRIPT_Q3FY26`)
5. **`performance_metrics`**:
   - `total_pipeline_latency_ms` & individual agent latencies (Sub-60s compliance)
   - `portfolio_risk_concentration_score` & flag (`HEALTHY` vs `OVER_LIMIT`)
   - `data_completeness_score` (1.0 in normal mode, 0.50 in degraded mode) & `consensus_confidence_score`

---

## 🛡️ SEBI Safety Guardrails & Fallback System

- **Retail F&O Filter:** Derivatives and complex options setups are automatically blocked for conservative/moderate profiles based on SEBI's 2024 retail trading advisory.
- **Portfolio Concentration Caps:** Restricts single-stock allocation above user-defined threshold limits (e.g., 10% max portfolio exposure).
- **Degraded-State Interceptor:** If external APIs or the vector database fail, the system drops into `DEGRADED_OPERATIONAL` mode. It disables aggressive buy recommendations and penalizes confidence scores by 40% rather than crashing.

---

## 📁 Repository Structure

- **app.py**: Ishank (Streamlit UI & Visual Dashboard)
- **orchestrator.py**: Sourav (Pipeline Orchestrator)
- **test_orchestrator.py**: Automated scenario evaluation suite
- **requirements.txt**: System dependencies
- **README.md**: System documentation
- **agents/**: Modular multi-agent engines
  - **quant_agent.py**: Parv (Technicals & Quantitative Signals)
  - **rag_agent.py**: Utsav (FAISS Vector RAG & Regulatory Disclosures)
  - **persona_telemetry.py**: Madhav (User Profiling & Risk Controls)
  - **synthesis_engine.py**: Sourav (Consensus & Degraded Fallbacks)
- **data/**: Grounding knowledge corpus (`RELIANCE_q3_transcript.txt`)

---

## 👥 Teammate Integration Guide (Plugging In Modules)

When Parv, Utsav, Madhav, and Ishank complete their respective modules, they plug directly into `orchestrator.py` via custom providers:

* **Parv (Technicals & Signals):** Must accept `(ticker: str, degraded: bool = False)` and return dict with `{"signal": "BULLISH"|"BEARISH"|"NEUTRAL", "confidence": float, "indicators": dict, "citations": list}`.
* **Utsav (RAG & SEBI Disclosures):** Must accept `(ticker: str, degraded: bool = False)` and return dict with `{"sentiment": "POSITIVE"|"CAUTIOUS"|"NEGATIVE", "document_chunks": list, "citations": list}`.
* **Madhav (User Risk & Behavioral):** Must accept `(persona_id: str)` and return dict with `{"risk_tolerance": "CONSERVATIVE"|"MODERATE"|"AGGRESSIVE", "max_single_stock_allocation_pct": float, "current_portfolio": dict}`.
* **Ishank (Frontend UI & Dashboard):** Renders live signals, step-by-step reasoning traces, portfolio allocation badges, and source attributions on Streamlit (`app.py`).

---

## 🧪 Verified Test Scenarios

1. **Scenario 1:** Normal Pipeline Execution (End-to-End with full reasoning chain & citations).
2. **Scenario 2:** Behavioral Persona Divergence (Identical stock data produces distinct recommendations for Conservative vs. Aggressive users).
3. **Scenario 3:** Signal Contradiction (Bullish price breakout conflicting with RBI/SEBI regulatory headwinds triggers warning alert badge).
4. **Scenario 4:** Degraded State Simulation (`degraded_mode=True` gracefully falls back with `DEGRADED_STATE_ALERT` without crashing or losing attribution).
5. **Scenario 5:** Performance Telemetry Logging (Verifies latency, risk concentration, and data completeness scores).
