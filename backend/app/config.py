"""
Configuration module for Scam & Claim Verifier.
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

SEBI_REGISTRY_PATH = DATA_DIR / "sebi_registry.json"
RULES_PATH = DATA_DIR / "rules.json"
BENCHMARK_PATH = DATA_DIR / "test_benchmark.json"

# SEBI Snapshot details
SEBI_SNAPSHOT_DATE = "October 03, 2026"

# Supported languages
SUPPORTED_LANGUAGES = ["en", "hi", "mr"]
DEFAULT_LANGUAGE = "en"

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
