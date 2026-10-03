"""
Risk Aggregator module.
Synthesizes signals from Rule Engine, SEBI Registry, and Link Checker
into the 4 mandated outcomes: HIGH_RISK, MEDIUM_RISK, LOW_RISK, and CANT_TELL.
"""
from typing import Dict, Any, List

def aggregate_risk(
    text: str,
    rule_results: Dict[str, Any],
    sebi_results: Dict[str, Any],
    link_results: List[Dict[str, Any]],
    entities: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes overall risk band, confidence rating, and unverified elements.
    """
    triggered_rules = rule_results.get("triggered_rules", [])
    rule_score = rule_results.get("total_score", 0)
    sebi_status = sebi_results.get("status", "NONE_CLAIMED")
    
    # Assess unverified factors
    unverified = ["Sender's real-world identity"]
    if entities.get("phone_numbers"):
        unverified.append("Phone number ownership and origin")
    if entities.get("upi_ids"):
        unverified.append("UPI account holder verification")
    if entities.get("urls"):
        unverified.append("External website authenticity")

    # High severity indicators
    has_high_rule = any(r.get("severity") == "high" for r in triggered_rules)
    has_apk = any(l.get("is_apk") for l in link_results)
    has_sebi_mismatch = (sebi_status == "FOUND_NAME_MISMATCH")
    has_fake_sebi = (sebi_status == "NOT_FOUND" and any(r["rule_id"] == "fake_sebi_claim" for r in triggered_rules))
    
    # Decision logic for 4 mandated risk bands
    if has_sebi_mismatch or has_apk or has_fake_sebi or rule_score >= 35 or (has_high_rule and len(triggered_rules) >= 1):
        risk_band = "HIGH_RISK"
        confidence_score = min(75 + len(triggered_rules) * 7 + (10 if has_sebi_mismatch or has_apk else 0), 96)
        confidence_level = "high"
        
    elif rule_score >= 20 or len(triggered_rules) >= 1 or any(l.get("severity") == "medium" for l in link_results):
        risk_band = "MEDIUM_RISK"
        confidence_score = 65 + len(triggered_rules) * 5
        confidence_level = "medium"
        
    else:
        # Zero rules triggered: determine whether it is LOW_RISK or CANT_TELL
        # Low risk applies to formal financial notifications, disclaimers, or verified SEBI entities
        text_lower = text.lower()
        formal_markers = [
            "subject to market risk", "read all scheme related documents",
            "past performance is not", "portfolio statement", "sip", "folio",
            "circular", "advisory", "rbi alert", "demat", "bse", "nse", "dividend",
            "epfo", "sovereign gold bond", "income tax department", "debited from your account",
            "order placed successfully", "order to redeem", "nps contribution", "yono app",
            "sebi cautions", "cdsl", "kyc norms", "disclaimer: investments", "research recommendation disclaimer"
        ]
        is_formal_notice = any(m in text_lower for m in formal_markers)
        is_verified_sebi = (sebi_status == "FOUND_NAME_MATCH")

        if is_formal_notice or is_verified_sebi:
            risk_band = "LOW_RISK"
            confidence_score = 80 if is_verified_sebi else 75
            confidence_level = "high" if is_verified_sebi else "medium"
        else:
            # Casual messages, vague chats, or personal texts cannot be reliably verified
            risk_band = "CANT_TELL"
            confidence_score = 50
            confidence_level = "low"
            unverified.append("Message context is insufficient to determine intent")

    return {
        "risk_band": risk_band,
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "rule_score": rule_score,
        "unverified": unverified
    }
