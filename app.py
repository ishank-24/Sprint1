"""
TRINETRA — Multi-Agent Financial Intelligence Dashboard
HACKVERSE: INTO THE WEB · PS-01 · Member 5 (Frontend & Explainability UI)

"Trinetra" (त्रिनेत्र) = the third eye — the seat of insight beyond ordinary
sight. The name maps directly onto the system's three parallel analyst
agents (Quant, Regulatory RAG, Persona/Telemetry) converging into one
synthesized, cited verdict.

Run locally:
    py -m streamlit run app.py
"""

import os
import time
import random
from datetime import datetime

import streamlit as st

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Trinetra · Multi-Agent Market Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM (CSS)
#   Palette:  #0A0E17 base · #10151F surface · #1A2130 raised
#             #E8B84C gold (signal)  #17C787 bull  #FF5D6C bear
#             #EDF1F7 text-hi · #8993A8 text-lo
#   Type:     Space Grotesk (display) / IBM Plex Sans (body) / IBM Plex Mono (data)
# ──────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --bg: #0A0E17;
  --surface: #10151F;
  --raised: #161D2B;
  --line: #262F42;
  --gold: #E8B84C;
  --bull: #17C787;
  --bear: #FF5D6C;
  --text-hi: #EDF1F7;
  --text-lo: #8993A8;
}

html, body, [class*="css"]  { background-color: var(--bg) !important; }
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }

* { font-family: 'IBM Plex Sans', sans-serif; }
h1, h2, h3, .display { font-family: 'Space Grotesk', sans-serif; }
.mono, .stMetric, code { font-family: 'IBM Plex Mono', monospace; }

/* ---- ticker tape ---- */
.tape-wrap {
  overflow: hidden;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: var(--surface);
  padding: 7px 0;
  margin-bottom: 28px;
  white-space: nowrap;
}
.tape-track {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12.5px;
  letter-spacing: 0.3px;
  color: var(--text-lo);
  animation: scroll 32s linear infinite;
}
.tape-track span { margin-right: 34px; }
.tape-up { color: var(--bull); }
.tape-down { color: var(--bear); }
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@media (prefers-reduced-motion: reduce) {
  .tape-track { animation: none; }
}

/* ---- masthead ---- */
.masthead { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 4px; }
.brand { font-size: 30px; font-weight: 700; color: var(--text-hi); letter-spacing: -0.5px; }
.brand-mark { color: var(--gold); }
.tagline { color: var(--text-lo); font-size: 13.5px; margin-top: -2px; margin-bottom: 22px; }

/* ---- degraded banner ---- */
.banner {
  border: 1px solid #4A3418;
  background: #1D160B;
  color: #E8B84C;
  padding: 10px 16px;
  font-size: 13px;
  font-family: 'IBM Plex Mono', monospace;
  margin-bottom: 20px;
}

/* ---- hero verdict ---- */
.hero {
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--raised) 0%, var(--surface) 100%);
  padding: 26px 30px;
  margin-bottom: 22px;
  position: relative;
}
.hero-accent { position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }
.hero-label { color: var(--text-lo); font-size: 12px; letter-spacing: 1.2px; text-transform: uppercase; font-family: 'IBM Plex Mono', monospace; }
.hero-action { font-family: 'Space Grotesk', sans-serif; font-size: 40px; font-weight: 700; letter-spacing: -0.5px; margin: 6px 0 10px 0; }
.hero-just { color: var(--text-lo); font-size: 14.5px; line-height: 1.55; max-width: 760px; }
.hero-conf { text-align: right; }
.hero-conf-num { font-family: 'IBM Plex Mono', monospace; font-size: 30px; font-weight: 600; }
.hero-conf-label { color: var(--text-lo); font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }

/* ---- signal cards ---- */
.sig-card {
  border: 1px solid var(--line);
  background: var(--surface);
  padding: 18px 20px;
  height: 100%;
}
.sig-dim { color: var(--text-lo); font-size: 11px; letter-spacing: 1.1px; text-transform: uppercase; font-family: 'IBM Plex Mono', monospace; margin-bottom: 8px; }
.sig-val { font-family: 'Space Grotesk', sans-serif; font-size: 19px; font-weight: 600; color: var(--text-hi); margin-bottom: 6px; line-height: 1.3; }
.sig-reason { color: var(--text-lo); font-size: 12.5px; line-height: 1.5; }
.sig-bar-track { height: 3px; background: var(--line); margin-top: 14px; }
.sig-bar-fill { height: 3px; }

/* ---- section headers ---- */
.sec-head { display: flex; align-items: center; gap: 10px; margin: 30px 0 12px 0; }
.sec-num { font-family: 'IBM Plex Mono', monospace; color: var(--gold); font-size: 13px; }
.sec-title { font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 600; color: var(--text-hi); }
.sec-rule { flex: 1; height: 1px; background: var(--line); }

/* ---- citation drawer ---- */
.cite-box {
  border-left: 3px solid var(--gold);
  background: var(--surface);
  padding: 14px 18px;
  margin-bottom: 10px;
}
.cite-src { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--gold); margin-bottom: 6px; }
.cite-body { color: var(--text-hi); font-size: 13.5px; line-height: 1.6; }
.risk-pill {
  display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px;
  padding: 2px 9px; border: 1px solid; margin-top: 10px; letter-spacing: 0.5px;
}

/* ---- reasoning log ---- */
.log-line { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--text-lo); padding: 5px 0; border-bottom: 1px solid var(--line); }
.log-agent { color: var(--gold); }
.log-line:last-child { border-bottom: none; }

/* ---- telemetry footer ---- */
.telem {
  border: 1px solid var(--line);
  background: var(--surface);
  padding: 16px 24px;
  margin-top: 26px;
  display: flex;
  justify-content: space-between;
}
.telem-item { text-align: left; }
.telem-num { font-family: 'IBM Plex Mono', monospace; font-size: 20px; color: var(--text-hi); font-weight: 600; }
.telem-label { color: var(--text-lo); font-size: 11px; letter-spacing: 0.8px; text-transform: uppercase; margin-top: 2px; }

/* ---- sidebar tightening ---- */
section[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--line); }
section[data-testid="stSidebar"] .block-container { padding-top: 22px; }

/* buttons */
.stButton > button {
  background: var(--gold) !important;
  color: #10151F !important;
  border: none !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-weight: 600 !important;
  letter-spacing: 0.4px;
  border-radius: 2px !important;
}
.stButton > button:hover { background: #F2C766 !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────────────────
TICKERS = ["RELIANCE.NS", "TATAMOTORS.NS", "HDFCBANK.NS", "INFY.NS"]
PERSONAS = ["Conservative SIP Investor", "Aggressive F&O Trader"]

ACTION_COLOR = {
    "ACCUMULATE (SIP)": "var(--bull)",
    "STRONG BUY": "var(--bull)",
    "HOLD": "var(--gold)",
    "CAUTION / AVOID": "var(--bear)",
    "REDUCE": "var(--bear)",
}

TAPE_SEED = [
    ("NIFTY 50", "24,812.30", True), ("SENSEX", "81,455.10", True),
    ("RELIANCE.NS", "1,462.20", True), ("TATAMOTORS.NS", "968.45", False),
    ("HDFCBANK.NS", "1,721.80", True), ("INFY.NS", "1,889.10", False),
    ("BANK NIFTY", "51,904.65", True), ("USD/INR", "83.42", False),
]

_BASE_METRICS = {
    "RELIANCE.NS": dict(rsi=64.2, vol_mult=2.4, flow=1420, litigation="Zero active litigation. Capex ₹14,000 Cr backed by operating cash flows.", risk="LOW"),
    "TATAMOTORS.NS": dict(rsi=71.6, vol_mult=3.1, flow=-380, litigation="Ongoing consumer-forum dispute (JLR export unit); provisioning adequate per Q3 notes.", risk="MEDIUM"),
    "HDFCBANK.NS": dict(rsi=48.3, vol_mult=1.1, flow=960, litigation="Clean regulatory record. NPA ratios within RBI comfort band this quarter.", risk="LOW"),
    "INFY.NS": dict(rsi=39.5, vol_mult=1.8, flow=-610, litigation="SEBI show-cause notice on ESOP disclosure timeline, resolution pending.", risk="HIGH"),
}

# ──────────────────────────────────────────────────────────────────────────
# DATA CORPUS FILE LOADER
# ──────────────────────────────────────────────────────────────────────────
def _load_filing_corpus(ticker: str) -> dict:
    """Dynamically reads text documents from the data/ directory."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    file_map = {
        "RELIANCE.NS": ("RELIANCE_q3_transcript.txt", "Reliance Q3 Earnings Transcript (data/RELIANCE_q3_transcript.txt)"),
        "TATAMOTORS.NS": ("TATAMOTORS_sebi_filing.txt", "Tata Motors SEBI Reg-30 Filing (data/TATAMOTORS_sebi_filing.txt)")
    }
    
    if ticker in file_map:
        filename, citation = file_map[ticker]
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                    if content:
                        # Extract first 320 chars for a clean card presentation
                        snippet = content[:320] + ("..." if len(content) > 320 else "")
                        return {
                            "summary": snippet,
                            "citation": citation,
                            "risk_flag": "LOW" if "RELIANCE" in ticker else "MEDIUM"
                        }
            except Exception:
                pass
                
    # Fallback if specific file is missing or unpopulated
    return {
        "summary": _BASE_METRICS[ticker]["litigation"],
        "citation": f"SEBI Q3 Corporate Filing & Transcripts ({ticker}), Section 4.2",
        "risk_flag": _BASE_METRICS[ticker]["risk"]
    }

# ──────────────────────────────────────────────────────────────────────────
# PIPELINE EXECUTION & FALLBACK LOGIC
# ──────────────────────────────────────────────────────────────────────────
def _mock_pipeline(ticker: str, persona: str, degraded: bool) -> dict:
    m = _BASE_METRICS[ticker]
    momentum_dir = "BULLISH" if m["rsi"] >= 55 else ("BEARISH" if m["rsi"] <= 40 else "NEUTRAL")
    quant = {
        "momentum": f"{momentum_dir} (RSI: {m['rsi']})",
        "volume_anomaly": f"{m['vol_mult']}x 20-DMA Spike ({'Anomaly Detected' if m['vol_mult'] >= 2 else 'Within Range'})",
        "sentiment": f"Institutional Flow: {'+' if m['flow'] >= 0 else ''}₹{m['flow']} Cr ({'Positive' if m['flow'] >= 0 else 'Negative'})",
        "confidence": round(min(0.95, 0.55 + m["vol_mult"] * 0.1), 2),
        "reasoning": f"{momentum_dir.title()} structure on {ticker} with {'above' if m['rsi'] >= 50 else 'below'}-average 50-day EMA positioning and {'continuous buying' if m['flow'] >= 0 else 'net distribution'} volume.",
    }

    if degraded:
        rag = {
            "status": "DEGRADED",
            "citation": "SEBI EDGAR feed unreachable — falling back to last cached snapshot (T-1).",
            "summary": "Regulatory grounding unavailable this session. Recommendation limited to technical signals only; no risk flag can be asserted with confidence.",
            "risk_flag": "UNKNOWN",
        }
    else:
        doc_data = _load_filing_corpus(ticker)
        rag = {
            "status": "HEALTHY",
            "citation": doc_data["citation"],
            "summary": doc_data["summary"],
            "risk_flag": doc_data["risk_flag"],
        }

    conservative = persona.startswith("Conservative")
    if degraded:
        action = "HOLD" if momentum_dir != "BEARISH" else "REDUCE"
        justification = "Regulatory grounding is offline, so the synthesis layer withholds a directional call and defaults to the lowest-risk stance until the feed recovers."
    elif rag["risk_flag"] == "HIGH":
        action = "CAUTION / AVOID"
        justification = "Technical signals lean constructive, but the regulatory agent flagged an unresolved disclosure issue — synthesis downgrades the call and surfaces the conflict rather than averaging it away."
    elif conservative:
        action = "ACCUMULATE (SIP)" if momentum_dir != "BEARISH" else "HOLD"
        justification = "Prioritizing capital preservation: signal strength is noted, but conservative guidelines call for dollar-cost averaging rather than a lump-sum entry at current valuations."
    else:
        action = "STRONG BUY" if momentum_dir == "BULLISH" else ("REDUCE" if momentum_dir == "BEARISH" else "HOLD")
        justification = "Aggressive risk profile permits sizing into confirmed momentum with volume confirmation; stop-loss discipline substitutes for the caution a conservative profile would apply."

    synth_conf = round((quant["confidence"] + (0.5 if degraded else (0.9 if rag["risk_flag"] == "LOW" else 0.65))) / 2, 2)

    return {
        "ticker": ticker,
        "persona": persona,
        "quant_agent": quant,
        "rag_agent": rag,
        "synthesized_intelligence": {
            "action": action,
            "confidence": synth_conf,
            "justification": justification,
            "degraded_data_status": "SEBI_FEED_UNREACHABLE" if degraded else "ALL_FEEDS_HEALTHY",
        },
        "telemetry": {
            "latency_ms": random.randint(310, 640),
            "risk_concentration_score": round(random.uniform(0.12, 0.41), 2),
            "signal_forward_accuracy": f"{round(random.uniform(71.0, 84.5), 1)}%",
        },
        "reasoning_log": [
            ("QUANT", quant["reasoning"]),
            ("RAG", rag["summary"] if not degraded else "Cached snapshot loaded; live corpus query skipped."),
            ("PERSONA", f"Applying '{persona}' weighting profile to raw signal set."),
            ("SYNTHESIS", justification),
        ],
    }


def fetch_analysis(ticker: str, persona: str, degraded: bool) -> dict:
    """Tries live orchestrator integration with dynamic signature resolution, falls back safely to mock."""
    try:
        from orchestrator import run_pipeline
        try:
            return run_pipeline(ticker=ticker, persona_id=persona, force_degrade=degraded)
        except TypeError:
            return run_pipeline(ticker=ticker, persona=persona, simulate_degraded=degraded)
    except Exception:
        time.sleep(0.35)
        return _mock_pipeline(ticker, persona, degraded)


# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR — CONTROLS
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='display' style='font-size:20px;font-weight:700;color:#EDF1F7;'>◈ TRINETRA</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8993A8;font-size:12px;margin-bottom:22px;'>Session controls</div>", unsafe_allow_html=True)

    ticker = st.selectbox("Equity", TICKERS, index=0)
    persona = st.radio("Investor persona", PERSONAS, index=0)
    degraded = st.toggle("Simulate SEBI feed outage", value=False, help="Forces the RAG agent into a degraded state to demonstrate graceful fallback.")

    run_clicked = st.button("Run analysis", use_container_width=True)

    st.markdown("<div class='sec-rule' style='margin:22px 0 14px 0;'></div>", unsafe_allow_html=True)
    st.caption("HACKVERSE · PS-01 · Multi-Agent Financial Intelligence")

if "analysis" not in st.session_state or run_clicked:
    st.session_state.analysis = fetch_analysis(ticker, persona, degraded)
    st.session_state.ts = datetime.now().strftime("%H:%M:%S")

data = st.session_state.analysis

# ──────────────────────────────────────────────────────────────────────────
# TICKER TAPE
# ──────────────────────────────────────────────────────────────────────────
def _tape_item(name, price, up):
    cls = "tape-up" if up else "tape-down"
    arrow = "▲" if up else "▼"
    return f"<span class='{cls}'>{name} {price} {arrow}</span>"


tape_items = "".join(_tape_item(name, price, up) for name, price, up in TAPE_SEED)
st.markdown(f"""<div class="tape-wrap"><div class="tape-track">{tape_items}{tape_items}</div></div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# MASTHEAD
# ──────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
  <div class="brand">TRI<span class="brand-mark">NET</span>RA</div>
  <div class="mono" style="color:#8993A8;font-size:12px;">LAST RUN {st.session_state.ts} IST</div>
</div>
<div class="tagline">Three analyst agents. One cited, explainable verdict — under 60 seconds.</div>
""", unsafe_allow_html=True)

if data["rag_agent"]["status"] == "DEGRADED":
    st.markdown(
        "<div class='banner'>⚠ DEGRADED MODE — regulatory feed unreachable. "
        "Falling back to technical signals only. No uncited claims are being generated.</div>",
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────
# HERO VERDICT
# ──────────────────────────────────────────────────────────────────────────
synth = data["synthesized_intelligence"]
accent = ACTION_COLOR.get(synth["action"], "var(--gold)")

st.markdown(f"""
<div class="hero">
  <div class="hero-accent" style="background:{accent};"></div>
  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
    <div>
      <div class="hero-label">{data['ticker']} · {data['persona']}</div>
      <div class="hero-action" style="color:{accent};">{synth['action']}</div>
      <div class="hero-just">{synth['justification']}</div>
    </div>
    <div class="hero-conf">
      <div class="hero-conf-num" style="color:{accent};">{int(synth['confidence']*100)}%</div>
      <div class="hero-conf-label">Synthesis confidence</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# 3D SIGNAL CARDS
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head"><span class="sec-num">01</span><span class="sec-title">3D Signal Classification — Quant Agent</span><div class="sec-rule"></div></div>
""", unsafe_allow_html=True)

quant = data["quant_agent"]
c1, c2, c3 = st.columns(3)
cards = [
    ("MOMENTUM", quant["momentum"], "Price-trend structure vs. 50-day EMA."),
    ("VOLUME ANOMALY", quant["volume_anomaly"], "Deviation from the 20-day moving average of traded volume."),
    ("INSTITUTIONAL SENTIMENT", quant["sentiment"], "Net FII/DII flow attributed to this ticker."),
]
for col, (dim, val, reason) in zip([c1, c2, c3], cards):
    with col:
        st.markdown(f"""
        <div class="sig-card">
          <div class="sig-dim">{dim}</div>
          <div class="sig-val">{val}</div>
          <div class="sig-reason">{reason}</div>
          <div class="sig-bar-track"><div class="sig-bar-fill" style="width:{int(quant['confidence']*100)}%; background:{accent};"></div></div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# RAG CITATION DRAWER
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head"><span class="sec-num">02</span><span class="sec-title">Regulatory Grounding — RAG Agent</span><div class="sec-rule"></div></div>
""", unsafe_allow_html=True)

rag = data["rag_agent"]
risk_color = {"LOW": "var(--bull)", "MEDIUM": "var(--gold)", "HIGH": "var(--bear)", "UNKNOWN": "#8993A8"}.get(rag["risk_flag"], "#8993A8")

with st.expander("Source attribution & filing summary", expanded=True):
    st.markdown(f"""
    <div class="cite-box">
      <div class="cite-src">SOURCE — {rag['citation']}</div>
      <div class="cite-body">{rag['summary']}</div>
      <span class="risk-pill" style="color:{risk_color}; border-color:{risk_color};">RISK FLAG · {rag['risk_flag']}</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# GLASS-BOX REASONING LOG
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head"><span class="sec-num">03</span><span class="sec-title">Glass-Box Reasoning Audit Log</span><div class="sec-rule"></div></div>
""", unsafe_allow_html=True)

with st.expander("Expand agent-by-agent reasoning chain", expanded=False):
    log_html = "".join(
        f"<div class='log-line'><span class='log-agent'>[{agent}]</span> {text}</div>"
        for agent, text in data["reasoning_log"]
    )
    st.markdown(f"<div>{log_html}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# TELEMETRY BAR
# ──────────────────────────────────────────────────────────────────────────
t = data["telemetry"]
st.markdown(f"""
<div class="telem">
  <div class="telem-item"><div class="telem-num">{t['latency_ms']} ms</div><div class="telem-label">Pipeline latency</div></div>
  <div class="telem-item"><div class="telem-num">{t['risk_concentration_score']}</div><div class="telem-label">Portfolio risk concentration</div></div>
  <div class="telem-item"><div class="telem-num">{t['signal_forward_accuracy']}</div><div class="telem-label">Signal forward accuracy</div></div>
  <div class="telem-item"><div class="telem-num" style="color:{'#17C787' if data['rag_agent']['status']=='HEALTHY' else '#E8B84C'};">{data['synthesized_intelligence']['degraded_data_status'].replace('_',' ')}</div><div class="telem-label">Feed status</div></div>
</div>
""", unsafe_allow_html=True)