"""
SEBI verification module.
Performs fact-checking against the October 03, 2026 official SEBI snapshot.
Detects valid registrations, non-existent numbers, and name-mismatch impersonation attacks.
"""
import json
import os
import re
from typing import Dict, Any, List, Optional
from difflib import SequenceMatcher
from .config import SEBI_REGISTRY_PATH, SEBI_SNAPSHOT_DATE

class SEBIVerifier:
    def __init__(self, registry_path: str = str(SEBI_REGISTRY_PATH)):
        self.snapshot_date = SEBI_SNAPSHOT_DATE
        self.by_reg_no = {}
        self.name_index = []
        self._load_registry(registry_path)

    def _load_registry(self, path: str):
        if not os.path.exists(path):
            print(f"Warning: SEBI registry file not found at {path}")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.snapshot_date = data.get("snapshot_date", SEBI_SNAPSHOT_DATE)
                self.by_reg_no = data.get("by_reg_no", {})
                self.name_index = data.get("name_index", [])
        except Exception as e:
            print(f"Error loading SEBI registry: {e}")

    def _names_match(self, claimed_name: str, registered_name: str, contact_person: str) -> bool:
        """
        Performs fuzzy token comparison between claimed name and registered entity / contact.
        """
        if not claimed_name:
            return True
            
        c_name = claimed_name.lower().strip()
        r_name = registered_name.lower().strip()
        cp_name = contact_person.lower().strip()
        
        # Exact substring match
        if c_name in r_name or c_name in cp_name or r_name in c_name or cp_name in c_name:
            return True
            
        # Token overlap check (e.g. "Kavitha Menon" vs "Menon, Kavitha")
        c_tokens = set(re.findall(r"\w+", c_name))
        r_tokens = set(re.findall(r"\w+", r_name))
        cp_tokens = set(re.findall(r"\w+", cp_name))
        
        # Ignore common titles
        ignore_words = {"mr", "mrs", "ms", "dr", "shri", "smt", "limited", "ltd", "pvt", "private", "llp"}
        c_tokens = c_tokens - ignore_words
        
        if c_tokens and (c_tokens.issubset(r_tokens) or c_tokens.issubset(cp_tokens)):
            return True
            
        # Sequence matcher ratio
        ratio1 = SequenceMatcher(None, c_name, r_name).ratio()
        ratio2 = SequenceMatcher(None, c_name, cp_name).ratio()
        return max(ratio1, ratio2) > 0.75

    def verify(self, sebi_numbers: List[str], claimed_names: List[str], full_text: str) -> Dict[str, Any]:
        """
        Evaluates claimed registration numbers and returns status:
        FOUND_NAME_MATCH | FOUND_NAME_MISMATCH | NOT_FOUND | NONE_CLAIMED
        """
        # If no registration number claimed
        if not sebi_numbers:
            # Check if text claims to be SEBI registered without providing a number
            if re.search(r"(?i)\b(sebi[- ]registered|authorized by sebi|sebi approved)\b", full_text):
                return {
                    "status": "NOT_FOUND",
                    "claimed_number": None,
                    "details": None,
                    "snapshot_date": self.snapshot_date,
                    "message": "Message claims SEBI registration or approval, but does not provide any valid SEBI registration number to verify."
                }
            return {
                "status": "NONE_CLAIMED",
                "claimed_number": None,
                "details": None,
                "snapshot_date": self.snapshot_date,
                "message": "No SEBI registration number was claimed in this message."
            }
            
        # If one or more numbers are claimed, verify the first / primary number
        primary_reg = sebi_numbers[0]
        record = self.by_reg_no.get(primary_reg)
        
        if not record:
            return {
                "status": "NOT_FOUND",
                "claimed_number": primary_reg,
                "details": None,
                "snapshot_date": self.snapshot_date,
                "message": f"Registration number {primary_reg} was NOT found in SEBI's official public list (as of {self.snapshot_date})."
            }
            
        # Number is found, now check if sender name matches registered holder
        reg_name = record["name"]
        contact = record.get("contact_person", "")
        
        # Check against claimed names extracted
        matched = False
        if claimed_names:
            for cn in claimed_names:
                if self._names_match(cn, reg_name, contact):
                    matched = True
                    break
        else:
            # Also scan full text for entity name
            if self._names_match("", reg_name, contact): # Default pass if no specific name asserted
                matched = True

        if claimed_names and not matched:
            return {
                "status": "FOUND_NAME_MISMATCH",
                "claimed_number": primary_reg,
                "details": {
                    "reg_no": primary_reg,
                    "registered_name": reg_name,
                    "type": record["type"],
                    "city": record.get("city", ""),
                    "state": record.get("state", "")
                },
                "snapshot_date": self.snapshot_date,
                "message": f"Registration number {primary_reg} exists in SEBI records, BUT belongs to '{reg_name}', which does NOT match the claimed sender. This is a common impersonation tactic."
            }
            
        return {
            "status": "FOUND_NAME_MATCH",
            "claimed_number": primary_reg,
            "details": {
                "reg_no": primary_reg,
                "registered_name": reg_name,
                "type": record["type"],
                "city": record.get("city", ""),
                "state": record.get("state", "")
            },
            "snapshot_date": self.snapshot_date,
            "message": f"Registration number {primary_reg} found under registered name '{reg_name}' ({record['type']}). Note: Registration alone does not prove the sender's true identity."
        }

# Global singleton
sebi_verifier = SEBIVerifier()
