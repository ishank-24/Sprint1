```markdown
<div align="center">

# ⚡ TRINETRA — 3D Cyber-HUD Multi-Agent Financial Intelligence
**Autonomous Multi-Perspective Market Analytics & Explainable Synthesis Engine**  
*HACKVERSE: INTO THE WEB · Problem Statement 01 (PS-01)*  
*VIT Chennai · IEEE RAS Hackathon 2026*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](#)
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20Passing-brightgreen.svg?logo=pytest&logoColor=white)](#)
[![Architecture](https://img.shields.io/badge/Architecture-Asynchronous%20Multi--Agent-00F0FF.svg)](#)

</div>

---

## 🧭 Executive Overview

Retail market participants frequently face conflicting market signals: strong bullish price action often conceals regulatory warnings, governance queries, and adverse auditor disclosures buried within complex statutory filings.

**TRINETRA** resolves this challenge through an asynchronous, fault-tolerant multi-agent architecture. The system orchestrates quantitative momentum tracking, dense RAG vector search across regulatory filings, and user risk profiling to deliver transparent, cited investment directives in under 500 milliseconds.

---

## 👥 Multi-Agent Architecture & Team Roles


```

```
                           ┌─────────────────────────────────┐
                           │       Streamlit Cyber-HUD       │
                           │   (3D Canvas & Explainability)  │
                           └────────────────┬────────────────┘
                                            │
                           ┌────────────────▼────────────────┐
                           │   Orchestrator Pipeline Core    │
                           │      (Concurrency & State)      │
                           └────────────────┬────────────────┘
                                            │
             ┌──────────────────────────────┼──────────────────────────────┐
             │                              │                              │
    ┌────────▼────────┐            ┌────────▼────────┐            ┌────────▼────────┐
    │  Quant Agent    │            │ Regulatory RAG  │            │ User Persona    │
    │ (15m Momentum,  │            │  (Vector Search │            │ (Risk Vectors & │
    │ Volume, Flows)  │            │  SEBI Filings)  │            │ Portfolio HHI)  │
    └─────────────────┘            └─────────────────┘            └─────────────────┘

```

```

| Role | Domain Lead | Responsibilities & Contract Standards |
| :--- | :--- | :--- |
| **Member 1** | **Sourav** | **Pipeline Orchestrator & Degraded Mode**: Concurrency dispatch, consensus synthesis engine, fallback state management, and performance telemetry logging. |
| **Member 2** | **Parv** | **Quantitative & Technical Analysis**: 15-minute candle momentum, dynamic 50-EMA support bands, volume standard deviation spikes ($>2\sigma$), and institutional flow tracking. |
| **Member 3** | **Utsav** | **Regulatory & Governance RAG**: Dense vector retrieval (`faiss-cpu` / `sentence-transformers`), document chunk extraction, and statutory citation mapping. |
| **Member 4** | **Madhav** | **Persona & Portfolio Risk**: Behavioral profile adaptation, single-stock allocation guardrails, and Herfindahl-Hirschman Index (HHI) concentration telemetry. |
| **Member 5** | **Ishank** | **Frontend & Explainability UI**: Interactive 3D particle canvas, Apple-inspired Dynamic Island state monitoring, glass-box audit timelines, and telemetry dashboards. |

---

## 🚀 Core Deliverable: Pipeline Orchestrator

The orchestrator exposes a pluggable execution entrypoint:

```python
from orchestrator import run_pipeline

# Execute multi-agent synthesis
result = run_pipeline(
    ticker="RELIANCE", 
    persona_id="p_conservative", 
    degraded_mode=False
)

```

### Complete Output Schema

`run_pipeline` returns a master dictionary with full citation attribution and performance telemetry:

```json
{
  "session_id": "sess_a81f3b0c",
  "pipeline_status": "SUCCESS",
  "alert_badge": "ALL_FEEDS_HEALTHY",
  "ticker": "RELIANCE",
  "persona_id": "p_conservative",
  "degraded_mode": false,
  "agent_inputs": {
    "technical_agent": {
      "agent": "TechnicalAnalysisAgent",
      "status": "HEALTHY",
      "signal": "BULLISH",
      "confidence": 0.85,
      "rsi": 64.2,
      "volume_multiplier": 2.4,
      "fii_dii_flow_cr": 1420.0
    },
    "regulatory_rag_agent": {
      "agent": "RegulatoryRagAgent",
      "status": "HEALTHY",
      "risk_flag": "LOW",
      "citations": ["SEBI Reg-30 Filing & Transcript (RELIANCE), Page 14"]
    },
    "user_profile_agent": {
      "persona_id": "p_conservative",
      "risk_tolerance": "LOW",
      "strategy": "SIP_ACCUMULATION",
      "max_single_stock_allocation_pct": 10.0
    }
  },
  "synthesized_intelligence": {
    "consensus_type": "CONSERVATIVE_CONVERGENCE",
    "recommendation": "ACCUMULATE (SIP)",
    "confidence_score": 0.88,
    "executive_summary": "Strong fundamentals verified against SEBI filings. Dollar-cost averaging advised.",
    "personalized_rationale": "Recommendation aligned to p_conservative risk constraints.",
    "reasoning_chain": [
      "Quant signals computed from price action & institutional volume.",
      "RAG cross-referenced against statutory filings and auditor disclosures.",
      "Synthesis consensus executed with risk-profile weighting."
    ]
  },
  "source_attributions": [
    "SEBI Reg-30 Filing & Transcript (RELIANCE), Page 14"
  ],
  "performance_metrics": {
    "total_pipeline_latency_ms": 312.4,
    "agent_latencies_ms": {
      "technical": 120.1,
      "rag": 185.4,
      "profile": 4.2
    },
    "consensus_confidence": 0.88,
    "data_completeness_score": 1.0,
    "portfolio_risk_concentration": 0.22
  }
}

```

---

## ✨ UI & Explainability Highlights

* **3D Interactive Particle Mesh**: Hardware-accelerated HTML5/Canvas background rendering real-time connected node physics.
* **Apple Dynamic Island Aura**: Real-time breathing status pill monitoring agent connection health and session time.
* **Glass-Box Step-by-Step Audit Log**: Transparent timeline tracing how quantitative indicators, RAG disclosures, and user personas converge into the final directive.
* **Simulated Upstream Failover**: Toggle to test system behavior during live SEBI feed outages, demonstrating zero-hallucination fallback modes.

---

## 🧪 Test Suite & Evaluation Benchmarks

Run the automated test suite across all five benchmark scenarios:

```cmd
py -m pytest tests/test_orchestrator.py -v

```

### Verified Scenarios

* **Scenario 1 (Normal Pipeline Execution)**: Validates concurrent agent dispatch, complete data attribution, and latency thresholds.
* **Scenario 2 (Persona Divergence on Identical Inputs)**: Confirms that identical market metrics yield distinct strategies for Conservative (SIP averaging) vs. Aggressive (leveraged breakout) profiles.
* **Scenario 3 (Signal Contradiction & Discordant Override)**: Verifies that technical buy signals are automatically downgraded when regulatory risks are detected.
* **Scenario 4 (Fault-Tolerant Degraded State)**: Tests system stability when `degraded_mode=True`, ensuring graceful degradation without ungrounded synthetic claims.
* **Scenario 5 (Comprehensive Performance Telemetry)**: Asserts logging of pipeline latency, per-agent latency breakdowns, data completeness scores, and HHI portfolio risk concentration.

---

## 🛠️ Setup & Execution

### 1. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<your-org>/Sprint1.git
cd Sprint1

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run Automated Tests

```bash
py -m pytest tests/test_orchestrator.py

```

### 4. Launch the Dashboard

```bash
streamlit run app.py

```

```

```