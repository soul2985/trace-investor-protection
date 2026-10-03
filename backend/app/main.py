"""
Trace: Scam & Claim Verifier
FastAPI Main Application
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from .config import (
    BASE_DIR, FRONTEND_DIR, BENCHMARK_PATH,
    SEBI_SNAPSHOT_DATE, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
)
from .normalizer import normalize_text, replace_homoglyphs
from .entity_extractor import extract_entities
from .rule_engine import rule_engine
from .sebi_verifier import sebi_verifier
from .link_checker import analyze_links
from .risk_aggregator import aggregate_risk
from .explainer import generate_explanation

# Initialize FastAPI App
app = FastAPI(
    title="Trace - Scam & Claim Verifier",
    description="Investor Safety Infrastructure for the SANGYAN Investor Resilience Hackathon",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request / Response Schemas
class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Message text or OCR transcription")
    language: str = Field(default="en", description="Target language: en, hi, mr")

class SebiDetails(BaseModel):
    reg_no: Optional[str] = None
    registered_name: Optional[str] = None
    type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class SebiCheckResult(BaseModel):
    status: str
    claimed_number: Optional[str] = None
    details: Optional[SebiDetails] = None
    snapshot_date: str
    message: str

class HighlightSpan(BaseModel):
    rule_id: str
    rule_name: str
    start: int
    end: int
    phrase: str

class ReasonItem(BaseModel):
    rule_id: str
    title: str
    description: str

class AnalyzeResponse(BaseModel):
    risk_band: str
    confidence_score: int
    confidence_level: str
    summary: str
    reasons: List[ReasonItem]
    highlights: List[HighlightSpan]
    sebi_check: SebiCheckResult
    link_check: List[Dict[str, Any]]
    entities: Dict[str, Any]
    unverified: List[str]
    next_steps: List[str]
    analogy: str
    check_type: str
    snapshot_date: str
    language: str

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Scam & Claim Verifier",
        "version": "1.0.0",
        "sebi_records_indexed": len(sebi_verifier.by_reg_no),
        "rules_active": len(rule_engine.rules),
        "snapshot_date": SEBI_SNAPSHOT_DATE
    }

@app.get("/api/rules")
def get_rules():
    return {
        "count": len(rule_engine.rules),
        "rules": [
            {
                "id": r["id"],
                "name": r["name"],
                "severity": r.get("severity", "medium"),
                "weight": r.get("weight", 20)
            }
            for r in rule_engine.rules
        ]
    }

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_message(req: AnalyzeRequest):
    """
    Main verification pipeline:
    Input Normalizer -> Entity Extractor -> Parallel Checks -> Risk Aggregator -> Explainer
    """
    raw_text = req.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Message text cannot be empty")

    lang = req.language.lower()
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    # 1. Normalize text
    normalized_text = normalize_text(raw_text)
    eval_text = replace_homoglyphs(normalized_text)

    # 2. Extract Entities
    entities = extract_entities(eval_text)

    # 3. Parallel Fact Verification
    # A. Rule Engine Check
    rule_results = rule_engine.evaluate(eval_text, language=lang)
    
    # B. SEBI Snapshot Lookup
    sebi_results = sebi_verifier.verify(
        sebi_numbers=entities["sebi_reg_numbers"],
        claimed_names=entities["claimed_names"],
        full_text=eval_text
    )

    # C. Link / URL Safety Check
    link_results = analyze_links(entities["urls"])

    # 4. Risk Aggregation
    risk_summary = aggregate_risk(
        text=eval_text,
        rule_results=rule_results,
        sebi_results=sebi_results,
        link_results=link_results,
        entities=entities
    )

    # 5. Explanations (Localized Templates + LLM Analogy if configured)
    explanation = generate_explanation(
        text=raw_text,
        language=lang,
        risk_band=risk_summary["risk_band"],
        sebi_results=sebi_results,
        triggered_rules=rule_results["triggered_rules"]
    )

    return AnalyzeResponse(
        risk_band=risk_summary["risk_band"],
        confidence_score=risk_summary["confidence_score"],
        confidence_level=risk_summary["confidence_level"],
        summary=explanation["summary"],
        reasons=[ReasonItem(**r) for r in explanation["reasons"]],
        highlights=[HighlightSpan(**h) for h in rule_results["highlights"]],
        sebi_check=SebiCheckResult(**sebi_results),
        link_check=link_results,
        entities=entities,
        unverified=risk_summary["unverified"],
        next_steps=explanation["next_steps"],
        analogy=explanation["analogy"],
        check_type=explanation["check_type"],
        snapshot_date=SEBI_SNAPSHOT_DATE,
        language=lang
    )

@app.get("/api/sebi/lookup")
def lookup_sebi(reg_no: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    """
    Direct endpoint to check any SEBI registration number or search by entity name.
    """
    if reg_no:
        clean_reg = reg_no.replace(" ", "").replace("-", "").upper()
        rec = sebi_verifier.by_reg_no.get(clean_reg)
        if rec:
            return {"found": True, "record": rec, "snapshot_date": SEBI_SNAPSHOT_DATE}
        return {"found": False, "reg_no": clean_reg, "snapshot_date": SEBI_SNAPSHOT_DATE}
    
    if q:
        query_str = q.lower().strip()
        matches = []
        for item in sebi_verifier.name_index:
            if query_str in item["name_lower"] or query_str in item["contact_lower"]:
                rec = sebi_verifier.by_reg_no.get(item["reg_no"])
                if rec:
                    matches.append(rec)
            if len(matches) >= 10:
                break
        return {"query": q, "matches": matches, "count": len(matches), "snapshot_date": SEBI_SNAPSHOT_DATE}

    raise HTTPException(status_code=400, detail="Provide 'reg_no' or 'q' parameter")

@app.get("/api/benchmark")
def run_benchmark():
    """
    Executes automated accuracy evaluation against the 100 test cases
    (50 synthetic scams, 25 genuine, 25 ambiguous).
    """
    if not os.path.exists(BENCHMARK_PATH):
        raise HTTPException(status_code=404, detail="Benchmark test file not found")

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total = len(cases)
    scam_total = 0
    scam_correct = 0
    genuine_total = 0
    genuine_correct = 0
    ambiguous_total = 0
    ambiguous_correct = 0

    results = []

    for item in cases:
        text = item["text"]
        cat = item["category"]
        expected = item["expected_risk"]

        # Run analysis
        req = AnalyzeRequest(text=text, language="en")
        analysis = analyze_message(req)
        actual = analysis.risk_band.lower()

        is_match = False
        if cat == "scam":
            scam_total += 1
            if actual in ["high_risk", "medium_risk"]:
                scam_correct += 1
                is_match = True
        elif cat == "genuine":
            genuine_total += 1
            if actual == "low_risk":
                genuine_correct += 1
                is_match = True
        elif cat == "ambiguous":
            ambiguous_total += 1
            if actual in ["cant_tell", "low_risk"]:
                ambiguous_correct += 1
                is_match = True

        results.append({
            "id": item["id"],
            "text": text[:60] + "...",
            "category": cat,
            "expected": expected,
            "actual": actual,
            "pass": is_match
        })

    scam_accuracy = round((scam_correct / scam_total) * 100, 1) if scam_total else 0
    genuine_accuracy = round((genuine_correct / genuine_total) * 100, 1) if genuine_total else 0
    ambiguous_accuracy = round((ambiguous_correct / ambiguous_total) * 100, 1) if ambiguous_total else 0
    overall_accuracy = round(((scam_correct + genuine_correct + ambiguous_correct) / total) * 100, 1)

    return {
        "total_cases": total,
        "overall_accuracy_pct": overall_accuracy,
        "scam_detection_rate_pct": scam_accuracy,
        "false_positive_rate_pct": round(100 - genuine_accuracy, 1),
        "genuine_accuracy_pct": genuine_accuracy,
        "ambiguous_accuracy_pct": ambiguous_accuracy,
        "scam_counts": f"{scam_correct}/{scam_total}",
        "genuine_counts": f"{genuine_correct}/{genuine_total}",
        "ambiguous_counts": f"{ambiguous_correct}/{ambiguous_total}",
        "results": results
    }

# Mount static frontend
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Trace Backend API is running. Frontend index.html not found."}

@app.get("/favicon.ico")
def serve_favicon():
    logo_file = FRONTEND_DIR / "assets" / "logo.png"
    if logo_file.exists():
        return FileResponse(str(logo_file), media_type="image/png")
    return FileResponse(str(FRONTEND_DIR / "index.html"))

