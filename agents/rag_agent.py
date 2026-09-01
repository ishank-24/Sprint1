import os
import re
from pathlib import Path
from typing import List, Dict, Any

# ---------- Config ----------
# Reads from 'data' directory where your .txt files live
CORPUS_DIR = Path(os.getenv("RAG_CORPUS_DIR", "data"))
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "500"))

# Check if heavy ML dependencies exist; fall back gracefully if missing
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    HEAVY_RAG_AVAILABLE = True
except ImportError:
    HEAVY_RAG_AVAILABLE = False

# ---------- Global state ----------
embedding_model = None
chunks: List[Dict[str, Any]] = []
index = None


def _normalize_ticker(raw_ticker: str) -> str:
    """Standardize tickers: 'tata_motors' -> 'TATAMOTORS', 'RELIANCE.NS' -> 'RELIANCE'."""
    clean = re.sub(r'[^a-zA-Z0-9]', '', raw_ticker.upper())
    return clean.replace("NS", "").replace("BSE", "")


def _load_text_from_corpus() -> List[Dict[str, Any]]:
    """Load text files from data/ directory and attach normalized ticker metadata."""
    docs = []
    if not CORPUS_DIR.exists():
        print(f"[RAG WARNING] Directory '{CORPUS_DIR}' not found.")
        return docs

    for fname in CORPUS_DIR.glob("*.txt"):
        name = fname.stem  # e.g., RELIANCE_q3_transcript
        raw_ticker = name.split("_")[0]
        ticker = _normalize_ticker(raw_ticker)

        text = fname.read_text(encoding="utf-8")
        docs.append({
            "doc_id": name,
            "ticker": ticker,
            "text": text,
        })
    return docs


def _chunk_documents(docs: List[Dict[str, Any]], chunk_size: int = CHUNK_SIZE) -> List[Dict[str, Any]]:
    """Split documents into smaller chunks for retrieval."""
    section_interval = 1000
    chunks_list = []

    for doc in docs:
        text = doc["text"]
        for i in range(0, max(1, len(text)), chunk_size):
            chunk_text = text[i:i + chunk_size]
            section_id = (i // section_interval) + 1
            chunks_list.append({
                "text": chunk_text,
                "ticker": doc["ticker"],
                "doc_id": doc["doc_id"],
                "section": f"Section {section_id}",
            })
    return chunks_list


def initialize_rag():
    """Call once at app startup to build embeddings and FAISS index."""
    global embedding_model, chunks, index

    docs = _load_text_from_corpus()
    if not docs:
        chunks = []
        index = None
        return

    chunks = _chunk_documents(docs)

    # Use FAISS vector index if packages are installed
    if HEAVY_RAG_AVAILABLE:
        try:
            EMBEDDING_MODEL_NAME = os.getenv("RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            texts = [c["text"] for c in chunks]
            embeddings = embedding_model.encode(texts, convert_to_numpy=True)
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            print(f"[RAG SUCCESS] Loaded {len(chunks)} chunks into FAISS vector index.")
        except Exception as e:
            print(f"[RAG WARNING] FAISS loading failed ({e}). Falling back to Keyword Matching.")
            index = None
    else:
        print("[RAG INFO] Heavy dependencies missing. Running in Lightweight Keyword RAG mode.")


def query_regulatory_rag(ticker: str, question: str = "", top_k: int = 3) -> Dict[str, Any]:
    """Retrieves top matching section for a ticker and evaluates risk levels."""
    global embedding_model, chunks, index

    clean_target_ticker = _normalize_ticker(ticker)

    if not chunks:
        return {
            "citation": "N/A",
            "risk_flag": "UNKNOWN",
            "excerpt": f"No corpus text files loaded from '{CORPUS_DIR}'.",
        }

    # Filter chunks matching the target ticker
    ticker_chunks = [c for c in chunks if c["ticker"] in clean_target_ticker or clean_target_ticker in c["ticker"]]

    if not ticker_chunks:
        return {
            "citation": "N/A",
            "risk_flag": "UNKNOWN",
            "excerpt": f"No regulatory filings found for ticker {ticker.upper()} in corpus.",
        }

    best_chunk = None

    # Option A: Semantic FAISS Search
    if index is not None and embedding_model is not None:
        try:
            q_embed = embedding_model.encode([question], convert_to_numpy=True)
            distances, indices = index.search(q_embed, top_k * 5)
            for idx in indices[0]:
                if idx < len(chunks) and chunks[idx]["ticker"] in clean_target_ticker:
                    best_chunk = chunks[idx]
                    break
        except Exception:
            best_chunk = None

    # Option B: Fast Keyword Fallback
    if best_chunk is None:
        keywords = set(re.findall(r'\w+', question.lower()))
        best_score = -1
        best_chunk = ticker_chunks[0]

        for c in ticker_chunks:
            score = sum(1 for kw in keywords if kw in c["text"].lower())
            if score > best_score:
                best_score = score
                best_chunk = c

    # Risk Flag Heuristic
    excerpt = best_chunk["text"]
    excerpt_lower = excerpt.lower()
    if any(k in excerpt_lower for k in ["risk", "warning", "adverse", "litigation", "penalty", "dispute", "uncertainty"]):
        risk_flag = "HIGH"
    elif any(k in excerpt_lower for k in ["growth", "positive", "profit", "expansion", "stable", "decreased debt"]):
        risk_flag = "LOW"
    else:
        risk_flag = "MEDIUM"

    citation = f"Doc: {best_chunk['doc_id']} | {best_chunk['section']}"

    return {
        "citation": citation,
        "risk_flag": risk_flag,
        "excerpt": excerpt,
    }


def get_regulatory_intel(ticker: str, force_degrade: bool = False) -> Dict[str, Any]:
    """
    MASTER CONTRACT FOR MEMBER 1 (ORCHESTRATOR).
    """
    if force_degrade:
        return {
            "status": "DEGRADED",
            "citation": "N/A",
            "summary": "SEBI/Regulatory document feed offline. Operating in degraded mode.",
            "risk_flag": "UNKNOWN",
            "excerpt": "No data retrieved due to simulated pipeline degradation."
        }
    
    result = query_regulatory_rag(ticker=ticker, question="risk debt regulatory audit litigation growth capex")
    
    return {
        "status": "HEALTHY",
        "citation": result["citation"],
        "summary": result["excerpt"][:180].replace("\n", " ") + "...",
        "risk_flag": result["risk_flag"],
        "excerpt": result["excerpt"]
    }
