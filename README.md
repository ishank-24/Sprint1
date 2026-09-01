# 🚀 Multi-Agent Autonomous Financial Intelligence System (PS-01)
### IEEE RAS Hackverse Hackathon | VIT Chennai
**Sprint 1 – Pipeline Orchestrator & Degraded-Mode Prototype**

This repository contains the Sprint 1 prototype implementation of the Multi-Agent Autonomous Financial Intelligence System (PS-01) developed for the IEEE RAS Hackverse Hackathon at VIT Chennai.

The system combines multiple specialized financial intelligence agents to analyze a stock from different perspectives, synthesize their outputs, personalize recommendations according to investor risk profiles, and maintain safe operation even when one or more data sources become unavailable.

---

### 👨‍💻 Member 1: Sourav
**Pipeline Orchestrator & Synthesis Engine Lead**

**Core Responsibilities:**
* Pipeline orchestration across multiple agents
* Parallel execution of financial intelligence modules
* Multi-agent signal consensus and synthesis
* Signal contradiction detection
* Degraded-mode fail-safe handling
* Personalized recommendation integration
* Performance and risk telemetry logging
* Transparent reasoning chain generation

**Core Deliverable Files:**
* `orchestrator.py`
* `synthesis_engine.py`
* `metrics_logger.py`

---

### 🎯 Project Objective
Financial decision-making often depends on multiple sources of information, including:
* Market and technical indicators
* Regulatory disclosures
* Earnings transcripts
* Investor risk tolerance
* Portfolio concentration
* Market uncertainty

Instead of relying on a single model or data source, this system uses a **Multi-Agent Architecture**. Each specialized agent analyzes a different aspect of financial intelligence, and the Pipeline Orchestrator coordinates these agents before passing their results to the Synthesis Engine.

The system then generates:
* A consensus-based recommendation
* A confidence score
* Personalized investment reasoning
* Regulatory and portfolio safeguards
* Source attributions
* Performance telemetry
* Degraded-mode alerts when information is unavailable

---

### 👥 Team Roles & Module Mapping

| Member | Role | Core Deliverable File | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Sourav** | Pipeline Orchestrator & Synthesis Engine | `orchestrator.py`, `synthesis_engine.py`, `metrics_logger.py` | Signal consensus, degraded-mode fail-safes, latency, risk and quality telemetry |
| **Parv** | Quant, Technicals & Signal Agent | `agents/quant_agent.py` | Technical indicators, trend calculations and momentum signals |
| **Utsav** | Regulatory, Earnings Transcript & RAG Agent | `agents/rag_agent.py` | FAISS vector indexing, SEBI disclosures and transcript analysis |
| **Madhav** | Behavioral Profiling & Risk Telemetry | `persona_telemetry.py` | Investor risk scoring, portfolio concentration limits and F&O safeguards |
| **Ishank** | Streamlit UI & Dashboard | `app.py` | Interactive dashboard, decision visualization, dynamic alerts and citations |

---

```

### ⚙️ How the System Works

#### Step 1: User Request

The user provides:

```text
Ticker Symbol + Investor Persona
```

Example:

```python
ticker = "RELIANCE"
persona_id = "p_conservative"
```

---

#### Step 2: Pipeline Orchestrator

The `orchestrator.py` module coordinates the entire system.

It sends requests to the three specialized agents:

```text
Technical Agent
Regulatory RAG Agent
Investor Risk Agent
```

The agents execute independently and provide their results to the Synthesis Engine.

---

#### Step 3: Multi-Agent Analysis

##### 📈 Technical & Quant Agent

Analyzes:

* Price trends
* Technical indicators
* Momentum
* Bullish signals
* Bearish signals
* Market confidence

Example output:

```python
{
    "signal": "BULLISH",
    "confidence": 0.82,
    "indicators": {},
    "citations": []
}
```

---

##### 📚 Regulatory & RAG Agent

Analyzes:

* SEBI disclosures
* Regulatory information
* Earnings transcripts
* Company announcements
* Financial risks

Example output:

```python
{
    "sentiment": "POSITIVE",
    "document_chunks": [],
    "citations": []
}
```

---

##### 👤 Behavioral & Risk Agent

Analyzes the investor profile, including:

* Risk tolerance
* Maximum single-stock allocation
* Existing portfolio concentration
* Investment constraints
* Retail F&O safeguards

Example output:

```python
{
    "risk_tolerance": "CONSERVATIVE",
    "max_single_stock_allocation_pct": 10.0,
    "current_portfolio": {}
}
```

---

### 🧩 Synthesis Engine

The `synthesis_engine.py` module combines the outputs from all agents.

It determines whether the signals **converge or diverge**.

#### Signal Convergence

Example:

```text
Technical Agent → BULLISH
Regulatory Agent → POSITIVE
```

Result:

```text
SIGNAL_CONVERGENCE
```

#### Signal Divergence

Example:

```text
Technical Agent → BULLISH
Regulatory Agent → CAUTIOUS
```

Result:

```text
SIGNAL_DIVERGENCE_WARNING
```

The system does not blindly generate a BUY recommendation when agents disagree. Instead, it can generate warning alerts, reduce confidence, and provide safer recommendations.

---

### 🚨 Signal Contradiction Detection

The system detects contradictions between different agents.

Example:

```text
Technical Signal:
BULLISH BREAKOUT

Regulatory Signal:
CAUTIOUS / NEGATIVE
```

The output may trigger:

```text
CONTRADICTION_ALERT: TECHNICAL_VS_REGULATORY
```

This ensures that strong technical momentum does not hide regulatory or fundamental risks.

---

### 🛡️ Degraded-Mode Operation

One of the primary responsibilities of the Pipeline Orchestrator is **Degraded Mode handling**.

If a critical data source becomes unavailable, the pipeline should not crash.

Example:

```python
run_pipeline(
    ticker="RELIANCE",
    persona_id="p_conservative",
    degraded_mode=True
)
```

The system continues operating using the available intelligence.

Expected status:

```text
DEGRADED_OPERATIONAL
```

Example alert:

```text
DEGRADED_STATE_ALERT: RAG_FEED_UNAVAILABLE
```

This ensures that the system remains operational while clearly informing the user that the decision was made using incomplete information.

---

### 🚀 Setup and Installation

#### 1. Prerequisites

Make sure the following are installed:

* Python **3.9, 3.10, or 3.11**
* Git

---

#### 2. Clone the Repository

Open your terminal or VS Code terminal and run:

```bash
git clone https://github.com/ishank-24/Sprint1.git
```

Navigate into the project:

```bash
cd Sprint1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 🖥️ Running the Application

#### Running the Streamlit Dashboard

To launch the interactive dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

Default address:

```text
http://localhost:8501
```

---

### 🧪 Running the Automated Test Suite

Run:

```bash
python tests/test_orchestrator.py
```

If your terminal is already inside the `tests` folder:

```bash
python test_orchestrator.py
```

The test suite verifies:

* End-to-end pipeline execution
* Persona-based recommendation differences
* Signal contradiction detection
* Degraded-mode fallback
* Performance telemetry

---

### 📁 Repository Structure

```text
Sprint1/
│
├── app.py
│   └── Ishank – Streamlit UI and Visual Dashboard
│
├── orchestrator.py
│   └── Sourav – Main Pipeline Orchestrator
│
├── synthesis_engine.py
│   └── Sourav – Multi-Agent Consensus and Recommendation Engine
│
├── metrics_logger.py
│   └── Sourav – Latency, Risk and Quality Telemetry
│
├── member_interfaces.py
│   └── Agent Interface Contracts and Protocols
│
├── persona_telemetry.py
│   └── Madhav – Investor Profiling and Portfolio Risk Controls
│
├── requirements.txt
│
├── .env.example
│
├── .gitignore
│
├── README.md
│
├── agents/
│   ├── __init__.py
│   ├── quant_agent.py
│   │   └── Parv – Technical and Quantitative Signals
│   │
│   └── rag_agent.py
│       └── Utsav – FAISS RAG and Regulatory Intelligence
│
├── tests/
│   └── test_orchestrator.py
│
└── data/
    └── RELIANCE_q3_transcript.txt
```

---

### 🔑 Primary Deliverable

The main function for executing the complete intelligence pipeline is:

```python
from orchestrator import run_pipeline
```

Example:

```python
result = run_pipeline(
    ticker="RELIANCE",
    persona_id="p_conservative",
    degraded_mode=False
)
```

---

### 📦 Output Schema

The `run_pipeline()` function returns a comprehensive Python dictionary.

```python
{
    "pipeline_status": "",
    "alert_badge": "",
    "synthesized_intelligence": {},
    "source_attributions": [],
    "performance_metrics": {}
}
```

---

### 1️⃣ Pipeline Status

Possible values:

```text
HEALTHY
```

or:

```text
DEGRADED_OPERATIONAL
```

---

### 2️⃣ Alert Badge

The system dynamically generates alerts.

Examples:

```text
None
```

```text
CONTRADICTION_ALERT: TECHNICAL_VS_REGULATORY
```

```text
DEGRADED_STATE_ALERT: RAG_FEED_UNAVAILABLE
```

---

### 🧠 Synthesized Intelligence

The main intelligence output contains:

```python
"synthesized_intelligence": {
    "consensus_type": "",
    "recommendation": "",
    "confidence_score": 0.0,
    "executive_summary": "",
    "personalized_rationale": "",
    "reasoning_chain": []
}
```

#### Consensus Type

Possible classifications include:

```text
SIGNAL_CONVERGENCE
SIGNAL_DIVERGENCE_WARNING
VALUE_DIVERGENCE
REGULATORY_RISK_WARNING
```

#### Recommendation

Possible recommendations include:

```text
BUY
ACCUMULATE_STAGGERED
CAUTIOUS_HOLD
AVOID_OR_TRIM
```

The recommendation depends on:

* Technical signals
* Regulatory sentiment
* Investor persona
* Portfolio concentration
* Data availability
* Overall confidence

---

### 📊 Confidence Score

The confidence score ranges between:

```text
0.0 → Very Low Confidence
1.0 → Very High Confidence
```

The score is influenced by:

* Agent agreement
* Signal strength
* Data completeness
* Signal contradictions
* Degraded-mode operation

---

### ⚡ Executive Summary

The system generates a concise summary designed to be understood quickly.

Example:

```text
Technical indicators indicate positive momentum, but regulatory
information introduces moderate uncertainty. Considering the
conservative investor profile and current portfolio exposure,
a cautious staggered allocation is recommended.
```

---

### 👤 Personalized Rationale

The recommendation is adjusted according to the investor persona.

Example factors:

```text
Risk Profile: CONSERVATIVE

Maximum Single Stock Allocation: 10%

Current Portfolio Exposure: 7%

Available Allocation Headroom: 3%
```

The system also considers:

* Portfolio concentration
* Risk tolerance
* Allocation limits
* Retail F&O safeguards

---

### 🔍 Transparent Reasoning Chain

The system provides an explainable reasoning sequence.

Example:

```text
Step 1:
Technical agent detected bullish momentum.

Step 2:
Regulatory agent found positive disclosures.

Step 3:
Signals showed convergence.

Step 4:
Investor profile identified as conservative.

Step 5:
Portfolio allocation limit was evaluated.

Step 6:
Final recommendation generated.
```

This allows users to understand **why the recommendation was generated**.

---

### 📚 Source Attributions

The pipeline preserves citations and source references.

Example:

```python
[
    "NSE_LIVE_TICK_FEED",
    "SEBI_DISCLOSURE_REG30",
    "EARNINGS_TRANSCRIPT_Q3FY26"
]
```

This improves:

* Transparency
* Traceability
* Grounding
* Trustworthiness

---

### 📈 Performance Metrics

The system records multiple performance metrics.

Example:

```python
"performance_metrics": {
    "total_pipeline_latency_ms": 0,
    "technical_agent_latency_ms": 0,
    "rag_agent_latency_ms": 0,
    "profile_agent_latency_ms": 0,
    "portfolio_risk_concentration_score": 0.0,
    "portfolio_risk_flag": "",
    "data_completeness_score": 1.0,
    "consensus_confidence_score": 0.0
}
```

---

### ⏱️ Latency Monitoring

The system tracks:

* Total pipeline latency
* Technical agent latency
* RAG agent latency
* Behavioral agent latency

This supports responsive multi-agent execution.

---

### 📉 Portfolio Risk Monitoring

The system calculates:

```text
portfolio_risk_concentration_score
```

Possible flags:

```text
HEALTHY
```

or:

```text
OVER_LIMIT
```

This helps prevent excessive portfolio concentration.

---

### 📊 Data Completeness Score

Normal operation:

```text
1.0
```

Degraded operation:

```text
0.50
```

This explicitly informs the synthesis engine and the user about missing intelligence sources.

---

### 🔌 Teammate Integration Guide

The architecture supports direct integration of the real modules developed by other team members.

```python
from orchestrator import FinancialIntelligenceOrchestrator

orchestrator = FinancialIntelligenceOrchestrator(
    technical_provider=my_member2_module.analyze_stock,
    rag_provider=my_member3_module.query_sebi_rag,
    profile_provider=my_member4_module.fetch_user_profile
)

result = orchestrator.execute_pipeline(
    "RELIANCE",
    "p_aggressive",
    degraded_mode=False
)
```

This design allows each team member to independently develop their module and integrate it into the central pipeline.

---

### 🔗 Agent Integration Contracts

#### 📈 Member 2 – Technical Agent

Must accept:

```python
(ticker: str, degraded: bool = False)
```

Must return:

```python
{
    "signal": "BULLISH | BEARISH | NEUTRAL",
    "confidence": float,
    "indicators": dict,
    "citations": list
}
```

---

#### 📚 Member 3 – Regulatory RAG Agent

Must accept:

```python
(ticker: str, degraded: bool = False)
```

Must return:

```python
{
    "sentiment": "POSITIVE | CAUTIOUS | NEGATIVE",
    "document_chunks": list,
    "citations": list
}
```

---

#### 👤 Member 4 – Behavioral & Risk Agent

Must accept:

```python
(persona_id: str)
```

Must return:

```python
{
    "risk_tolerance": "CONSERVATIVE | MODERATE | AGGRESSIVE",
    "max_single_stock_allocation_pct": float,
    "current_portfolio": dict
}
```

---

### 🧪 Automated Evaluation Scenarios

The automated test suite demonstrates the primary judging criteria.

#### Scenario 1: Normal Pipeline Execution

Tests:

```text
End-to-End Multi-Agent Execution
```

Expected:

* Full agent execution
* Synthesized intelligence
* Reasoning chain
* Source citations
* Performance metrics

---

#### Scenario 2: Behavioral Persona Divergence

Tests whether the same stock produces different recommendations for different investors.

Example:

```text
Stock: RELIANCE

Conservative Persona → CAUTIOUS_HOLD

Aggressive Persona → ACCUMULATE_STAGGERED
```

This demonstrates genuine recommendation personalization.

---

#### Scenario 3: Signal Contradiction

Example:

```text
Technical Signal: BULLISH

Regulatory Signal: CAUTIOUS
```

Expected alert:

```text
CONTRADICTION_ALERT: TECHNICAL_VS_REGULATORY
```

The system should reduce confidence and generate a safer recommendation.

---

#### Scenario 4: Degraded State Simulation

Run:

```python
degraded_mode=True
```

Expected:

```text
Pipeline continues operating.
```

Status:

```text
DEGRADED_OPERATIONAL
```

Alert:

```text
DEGRADED_STATE_ALERT
```

The system should not crash and should preserve available source attribution.

---

#### Scenario 5: Performance Telemetry

Verifies:

* Pipeline latency
* Agent latency
* Portfolio risk
* Data completeness
* Consensus confidence

---

### 🛡️ Key System Features

#### ✅ Multi-Agent Architecture

Multiple specialized agents analyze different dimensions of financial intelligence.

#### ✅ Signal Consensus

The synthesis engine identifies whether agents agree or disagree.

#### ✅ Contradiction Detection

Conflicting signals trigger warnings rather than blindly generating recommendations.

#### ✅ Personalized Intelligence

Recommendations change depending on the user's:

* Risk tolerance
* Portfolio concentration
* Allocation limits

#### ✅ Degraded-Mode Safety

The pipeline remains operational even when a data source fails.

#### ✅ Transparent Reasoning

Every recommendation includes a reasoning chain.

#### ✅ Source Attribution

Available regulatory and financial sources are preserved.

#### ✅ Performance Monitoring

Latency, risk and data quality metrics are continuously tracked.

---

### 🎯 Example Pipeline Flow

```text
USER
 │
 │ Ticker + Persona
 ▼
PIPELINE ORCHESTRATOR
 │
 ├───────────────┐
 │               │
 ▼               ▼
TECHNICAL      REGULATORY
AGENT          RAG AGENT
 │               │
 └───────┬───────┘
         │
         ▼
BEHAVIORAL & RISK AGENT
         │
         ▼
SYNTHESIS ENGINE
         │
         ▼
SIGNAL CONSENSUS
         │
         ▼
CONTRADICTION CHECK
         │
         ▼
PERSONALIZED RECOMMENDATION
         │
         ▼
DEGRADED MODE CHECK
         │
         ▼
METRICS LOGGER
         │
         ▼
FINAL GROUNDED OUTPUT
```

---

### 🏆 Sprint 1 Deliverable Summary

#### Sourav – Pipeline Orchestrator & Degraded-Mode Lead

**Primary Contributions:**

```text
✓ Multi-Agent Pipeline Orchestration
✓ Agent Integration Architecture
✓ Signal Consensus Engine
✓ Signal Contradiction Detection
✓ Personalized Recommendation Flow
✓ Degraded-Mode Fail-Safes
✓ Source Attribution Preservation
✓ Performance Telemetry
✓ Portfolio Risk Monitoring
✓ Transparent Reasoning Chain
```

---

### 🔮 Future Improvements

Future versions of the system can include:

* Real-time NSE market data integration
* Live SEBI disclosure feeds
* Advanced portfolio optimization
* Machine learning-based confidence scoring
* Multi-stock portfolio analysis
* Real-time news intelligence
* Event-driven risk detection
* Advanced financial knowledge graphs
* Reinforcement learning for adaptive recommendations

---

### 🏁 Final Vision

The **Multi-Agent Autonomous Financial Intelligence System** is designed to move beyond traditional single-source stock recommendations.

By combining:

```text
Market Intelligence
+
Regulatory Intelligence
+
Investor Behavior
+
Portfolio Risk Controls
+
Multi-Agent Consensus
+
Fail-Safe Degraded Operation
```

The system aims to generate financial intelligence that is:

```text
✓ Personalized
✓ Transparent
✓ Grounded
✓ Risk-Aware
✓ Resilient
✓ Explainable
```

---

## 👥 Team

**IEEE RAS Hackverse Hackathon – VIT Chennai**

### Multi-Agent Autonomous Financial Intelligence System (PS-01)

**Sprint 1**
