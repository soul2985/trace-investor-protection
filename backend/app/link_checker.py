"""
Link and URL reputation checker.
Detects APK download links, deceptive URL shorteners, and suspicious TLDs.
"""
import re
from urllib.parse import urlparse
from typing import List, Dict, Any

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".work",
    ".click", ".buzz", ".cfd", ".vip", ".loan", ".icu", ".monster"
}

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy",
    "shorturl.at", "ow.ly", "buff.ly", "goo.gl"
}

PHISHING_KEYWORDS = [
    "sebi", "rbi", "zerodha", "groww", "angelone", "upstox", "bonus",
    "guarantee", "free-profit", "vip-trade", "secure-invest"
]

def check_url(url: str) -> Dict[str, Any]:
    """
    Analyzes a single URL for security red flags.
    """
    issues = []
    severity = "low"
    
    parsed = urlparse(url if "://" in url else "http://" + url)
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # Check 1: Direct APK download
    if path.endswith(".apk") or ".apk?" in url.lower():
        issues.append("Direct APK file download detected. Scammers use APKs to bypass Play Store security.")
        severity = "high"
        
    # Check 2: Known URL shortener hiding target
    for shortener in URL_SHORTENERS:
        if netloc == shortener or netloc.endswith("." + shortener):
            issues.append(f"Shortened URL ({shortener}) used to conceal actual destination.")
            if severity != "high":
                severity = "medium"
            break
            
    # Check 3: Private Telegram or WhatsApp group link
    if "t.me" in netloc or "chat.whatsapp.com" in (netloc + path):
        issues.append("Direct invite link to private messaging group.")
        if severity != "high":
            severity = "medium"
            
    # Check 4: Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if netloc.endswith(tld):
            issues.append(f"Uses suspicious low-cost top-level domain ({tld}) commonly associated with disposable scam pages.")
            severity = "high"
            break
            
    # Check 5: Lookalike / Brand impersonation in domain
    for kw in PHISHING_KEYWORDS:
        if kw in netloc and not netloc.endswith(f"{kw}.gov.in") and not netloc.endswith(f"{kw}.com") and not netloc.endswith(f"{kw}.in"):
            issues.append(f"Domain contains financial keyword '{kw}', likely mimicking a legitimate institution.")
            severity = "high"
            break

    return {
        "url": url,
        "domain": netloc,
        "severity": severity,
        "is_apk": path.endswith(".apk") or ".apk?" in url.lower(),
        "is_shortened": any(s in netloc for s in URL_SHORTENERS),
        "issues": issues
    }

def analyze_links(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Analyzes a list of URLs and returns findings.
    """
    return [check_url(u) for u in urls]
