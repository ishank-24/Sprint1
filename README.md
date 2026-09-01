# Sprint1
# Multi-Agent Autonomous Financial Intelligence System (PS-01)
## Sourav: Pipeline Orchestrator & Degraded-Mode Lead Prototype

This directory contains the complete prototype implementation for **Sourav (Pipeline Orchestrator & Degraded-Mode Lead)** for the IEEE RAS Hackverse Hackathon (VIT Chennai).

---

## 👥 Team Roles & Module Mapping

| Name | Role | Core Deliverable File | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Sourav** | Pipeline Orchestrator & Synthesis Engine | `orchestrator.py`, `synthesis_engine.py`, `metrics_logger.py` | Signal consensus, degraded-mode fail-safes, latency & risk telemetry |
| **Parv** | Quant, Technicals & Signal Agent | `agents/quant_agent.py` | Technical indicators, trend calculations, momentum signals |
| **Utsav** | Regulatory, Earnings Transcript & RAG Agent | `agents/rag_agent.py` | FAISS vector indexing, SEBI disclosures, transcript chunking |
| **Madhav** | Behavioral Profiling & Risk Telemetry | `persona_telemetry.py` | Investor risk scoring, portfolio concentration limits, F&O filters |
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

## 📁 Repository Structure

```text
Sprint1/
│
├── app.py                      # Ishank (Streamlit UI & Visual Dashboard)
├── orchestrator.py             # Sourav (Pipeline Orchestrator)
├── synthesis_engine.py        # Sourav (Consensus Engine & Degraded Fallbacks)
├── metrics_logger.py           # Telemetry (Latency, Portfolio Risk & Quality Logger)
├── member_interfaces.py        # Abstract Type Protocols & Contracts for Agents
├── persona_telemetry.py        # Madhav (User Profiling & Risk Controls)
├── requirements.txt            # System dependencies
├── .env.example                # Sample environment configuration file
├── .gitignore                  # Git exclusion configuration
├── README.md                   # System documentation
│
├── agents/                     # Modular multi-agent engines
│   ├── __init__.py
│   ├── quant_agent.py          # Parv (Technicals & Quantitative Signals)
│   └── rag_agent.py            # Utsav (FAISS Vector RAG & Regulatory Disclosures)
│
├── tests/                      # Automated scenario testing suite
│   └── test_orchestrator.py
│
└── data/                       # Grounding knowledge corpus
    └── RELIANCE_q3_transcript.txt
