"""
Trace — Scam & Claim Verifier
Single-command runner to boot the application.
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Ensure SEBI database is built
sebi_db_path = BASE_DIR / "backend" / "data" / "sebi_registry.json"
if not sebi_db_path.exists():
    print("Building SEBI database from official snapshot...")
    from backend.scripts.build_sebi_db import build_database
    build_database()

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("  TRACE — Scam & Claim Verifier")
    print("  Investor Safety Infrastructure (SANGYAN Hackathon)")
    print("=" * 60)
    print("  Application running at: http://localhost:8000")
    print("  API Docs available at:  http://localhost:8000/docs")
    print("  SEBI Snapshot Date:     October 03, 2026")
    print("=" * 60 + "\n")
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
