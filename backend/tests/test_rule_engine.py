"""
Unit tests for Scam & Claim Verifier.
Tests Rule Engine, Negation Handling, Multilingual regex, and SEBI Verifier.
"""
import unittest
from backend.app.rule_engine import rule_engine
from backend.app.sebi_verifier import sebi_verifier
from backend.app.entity_extractor import extract_entities
from backend.app.risk_aggregator import aggregate_risk

class TestRuleEngine(unittest.TestCase):
    def test_guaranteed_returns_flagged(self):
        res = rule_engine.evaluate("Get guaranteed 40% monthly returns with our program.")
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertIn("guaranteed_returns", rule_ids)
        self.assertIn("unrealistic_returns", rule_ids)

    def test_negation_handling(self):
        # When negation phrase "returns are not guaranteed" is used, guaranteed_returns should NOT trigger
        text = "Investments are subject to market risks, returns are not guaranteed."
        res = rule_engine.evaluate(text)
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertNotIn("guaranteed_returns", rule_ids)

    def test_hindi_fraud_message(self):
        text = "40% गारंटीड मासिक मुनाफा पाएं। अभी हमारे वीआईपी टेलीग्राम ग्रुप में जुड़ें।"
        res = rule_engine.evaluate(text, language="hi")
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertIn("guaranteed_returns", rule_ids)
        self.assertIn("private_group", rule_ids)

    def test_marathi_fraud_message(self):
        text = "दरमहा 40% खात्रीशीर परतावा मिळवा. लगेच पैसे पाठवा आणि हे अ‍ॅप इन्स्टॉल करा."
        res = rule_engine.evaluate(text, language="mr")
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertIn("guaranteed_returns", rule_ids)
        self.assertIn("app_install", rule_ids)

    def test_apk_and_remote_access(self):
        text = "Install this APK and give remote access so our expert can complete verification."
        res = rule_engine.evaluate(text)
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertIn("app_install", rule_ids)
        self.assertIn("remote_access", rule_ids)

    def test_personal_upi_flag(self):
        text = "Send ₹50,000 directly to manager@okhdfcbank for quick activation."
        res = rule_engine.evaluate(text)
        rule_ids = [r["rule_id"] for r in res["triggered_rules"]]
        self.assertIn("personal_upi", rule_ids)

class TestSEBIVerifier(unittest.TestCase):
    def test_found_name_match(self):
        # Real advisor Kavitha Menon INA000000037
        res = sebi_verifier.verify(
            sebi_numbers=["INA000000037"],
            claimed_names=["Kavitha Menon"],
            full_text="Advice from Kavitha Menon, SEBI reg INA000000037"
        )
        self.assertEqual(res["status"], "FOUND_NAME_MATCH")
        self.assertIsNotNone(res["details"])
        self.assertEqual(res["details"]["reg_no"], "INA000000037")

    def test_found_name_mismatch_impersonation(self):
        # Real registration number INH000000016 belongs to STAKEHOLDERS EMPOWERMENT SERVICES
        # But sender claims to be "Ravi Kumar"
        res = sebi_verifier.verify(
            sebi_numbers=["INH000000016"],
            claimed_names=["Ravi Kumar"],
            full_text="I am Ravi Kumar, registered analyst INH000000016"
        )
        self.assertEqual(res["status"], "FOUND_NAME_MISMATCH")
        self.assertIn("impersonation", res["message"].lower())

    def test_not_found_number(self):
        res = sebi_verifier.verify(
            sebi_numbers=["INA999999999"],
            claimed_names=[],
            full_text="Check my reg INA999999999"
        )
        self.assertEqual(res["status"], "NOT_FOUND")

    def test_none_claimed(self):
        res = sebi_verifier.verify(
            sebi_numbers=[],
            claimed_names=[],
            full_text="Hey let's meet for lunch tomorrow."
        )
        self.assertEqual(res["status"], "NONE_CLAIMED")

class TestEntityExtractor(unittest.TestCase):
    def test_extract_all_entities(self):
        text = "I am Suresh Patil, SEBI reg INA000000037. Pay ₹25,000 to suresh@oksbi or visit https://t.me/vip_signals"
        entities = extract_entities(text)
        self.assertIn("INA000000037", entities["sebi_reg_numbers"])
        self.assertIn("suresh@oksbi", entities["upi_ids"])
        self.assertTrue(any("t.me" in u for u in entities["urls"]))
        self.assertTrue(any("25,000" in a for a in entities["amounts"]))

if __name__ == "__main__":
    unittest.main()
