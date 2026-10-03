"""
Rule Engine module.
Evaluates normalized text against 11 fraud detection rules with negation handling
and generates character-offset spans for visual phrase highlighting.
"""
import json
import os
import re
from typing import List, Dict, Any, Tuple
from .config import RULES_PATH

class RuleEngine:
    def __init__(self, rules_path: str = str(RULES_PATH)):
        self.rules = []
        self._load_rules(rules_path)

    def _load_rules(self, path: str):
        if not os.path.exists(path):
            print(f"Warning: Rules file not found at {path}")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
        except Exception as e:
            print(f"Error loading rules: {e}")

    def evaluate(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Evaluates input text against rules.
        Returns triggered rules, highlighted phrase spans, and cumulative risk score.
        """
        if not text:
            return {"triggered_rules": [], "highlights": [], "total_score": 0}

        triggered = []
        highlights = []
        total_score = 0

        for rule in self.rules:
            rule_id = rule["id"]
            rule_name = rule["name"]
            weight = rule.get("weight", 20)
            patterns = rule.get("patterns", [])
            negations = rule.get("negations", [])
            explanations = rule.get("explanations", {})

            # 1. Check if negation applies to this rule
            is_negated = False
            for neg_pat in negations:
                if re.search(neg_pat, text, re.IGNORECASE):
                    is_negated = True
                    break

            if is_negated:
                # Rule was negated (e.g. "returns are not guaranteed"), do not flag
                continue

            # 2. Check for positive pattern matches
            matched_spans = []
            for pat in patterns:
                for match in re.finditer(pat, text, re.IGNORECASE):
                    start, end = match.span()
                    phrase = text[start:end]
                    # Check overlap with existing spans for this rule
                    if not any(s <= start and end <= e for s, e, _ in matched_spans):
                        matched_spans.append((start, end, phrase))

            if matched_spans:
                # Add to triggered rules
                explanation = explanations.get(language, explanations.get("en", ""))
                triggered.append({
                    "rule_id": rule_id,
                    "rule_name": rule_name,
                    "weight": weight,
                    "severity": rule.get("severity", "medium"),
                    "matched_count": len(matched_spans),
                    "phrases": [p for _, _, p in matched_spans],
                    "explanation": explanation
                })
                total_score += weight

                for s, e, phrase in matched_spans:
                    highlights.append({
                        "rule_id": rule_id,
                        "rule_name": rule_name,
                        "start": s,
                        "end": e,
                        "phrase": phrase
                    })

        # Deduplicate and sort highlights by character start offset
        sorted_highlights = sorted(highlights, key=lambda x: (x["start"], -x["end"]))
        clean_highlights = []
        last_end = -1
        for h in sorted_highlights:
            if h["start"] >= last_end:
                clean_highlights.append(h)
                last_end = h["end"]

        return {
            "triggered_rules": triggered,
            "highlights": clean_highlights,
            "total_score": min(total_score, 100)
        }

# Global singleton
rule_engine = RuleEngine()
