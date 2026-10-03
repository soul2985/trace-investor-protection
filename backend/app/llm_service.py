"""
LLM Service module.
Uses Gemini Flash to provide empathetic, contextual summaries and analogies
while strictly respecting factual signals verified by code.
"""
import os
import json
from typing import Dict, Any, Optional
from .config import GEMINI_API_KEY, GEMINI_MODEL

class LLMService:
    def __init__(self, api_key: str = GEMINI_API_KEY, model_name: str = GEMINI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Gemini Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def explain(
        self,
        text: str,
        language: str,
        risk_band: str,
        sebi_status: str,
        triggered_rules: list
    ) -> Optional[Dict[str, Any]]:
        """
        Calls Gemini Flash to generate a plain-language summary and analogy in the target language.
        Returns None if unavailable or on error, triggering the basic check fallback.
        """
        if not self.is_available():
            return None

        lang_name = {"en": "English", "hi": "Hindi", "mr": "Marathi"}.get(language, "English")

        prompt = f"""You are an investor protection assistant helping an elderly, first-time investor (persona: Ramesh, 62, retired teacher).
Analyze this message and the verified factual signals provided.
Do NOT contradict the verified facts. Do NOT give investment recommendations or stock advice.
Return ONLY valid JSON.

Verified Signals:
- Original Message: "{text}"
- Assessed Risk Level: {risk_band}
- SEBI Registry Status: {sebi_status}
- Triggered Red Flags: {[r['rule_name'] for r in triggered_rules]}
- Target Language: {lang_name}

JSON format to return:
{{
  "summary": "One clear, calm, non-judgmental sentence explaining the risk in {lang_name}",
  "reasons": ["Short reason 1 in {lang_name}", "Short reason 2 in {lang_name}"],
  "analogy": "A simple everyday analogy (e.g., comparing to a street vendor or locked gate) in {lang_name} that helps an elder understand why this is risky",
  "safety_tip": "One clear action for what the user should do right now in {lang_name}"
}}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            if response and response.text:
                return json.loads(response.text)
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return None

        return None

# Global singleton
llm_service = LLMService()
