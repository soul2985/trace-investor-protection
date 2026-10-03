"""
Benchmark evaluation runner for Scam & Claim Verifier.
Runs 100 benchmark test cases (50 synthetic scams, 25 genuine, 25 ambiguous)
and outputs accuracy, scam detection rate, and false-positive rate.
"""
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from backend.app.main import app, analyze_message, AnalyzeRequest
from backend.app.config import BENCHMARK_PATH

def run_evaluation():
    if not os.path.exists(BENCHMARK_PATH):
        print(f"Benchmark file not found: {BENCHMARK_PATH}")
        return

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total = len(cases)
    scam_total = 0
    scam_detected = 0
    genuine_total = 0
    genuine_correct = 0
    ambiguous_total = 0
    ambiguous_correct = 0

    print("=" * 70)
    print(f"RUNNING BENCHMARK EVALUATION ON {total} TEST CASES")
    print("=" * 70)

    for item in cases:
        req = AnalyzeRequest(text=item["text"], language="en")
        analysis = analyze_message(req)
        actual = analysis.risk_band.lower()
        cat = item["category"]

        if cat == "scam":
            scam_total += 1
            if actual in ["high_risk", "medium_risk"]:
                scam_detected += 1
            else:
                print(f"[MISSED SCAM] ID {item['id']}: '{item['text']}' -> Got {actual}")

        elif cat == "genuine":
            genuine_total += 1
            if actual == "low_risk":
                genuine_correct += 1
            else:
                print(f"[FALSE ALARM] ID {item['id']}: '{item['text']}' -> Got {actual}")

        elif cat == "ambiguous":
            ambiguous_total += 1
            if actual in ["cant_tell", "low_risk"]:
                ambiguous_correct += 1
            else:
                print(f"[AMBIGUOUS MISMATCH] ID {item['id']}: '{item['text']}' -> Got {actual}")

    scam_rate = round((scam_detected / scam_total) * 100, 1)
    genuine_rate = round((genuine_correct / genuine_total) * 100, 1)
    false_alarm_rate = round(100 - genuine_rate, 1)
    ambiguous_rate = round((ambiguous_correct / ambiguous_total) * 100, 1)
    overall = round(((scam_detected + genuine_correct + ambiguous_correct) / total) * 100, 1)

    print("\n" + "=" * 70)
    print("BENCHMARK EVALUATION RESULTS")
    print("=" * 70)
    print(f"Total Test Cases:            {total}")
    print(f"Scam Detection Rate:         {scam_rate}% ({scam_detected}/{scam_total})")
    print(f"Genuine Messages Correct:    {genuine_rate}% ({genuine_correct}/{genuine_total})")
    print(f"False Positive Alarm Rate:   {false_alarm_rate}%")
    print(f"Ambiguous / Can't Tell Rate: {ambiguous_rate}% ({ambiguous_correct}/{ambiguous_total})")
    print(f"Overall Benchmark Accuracy:  {overall}%")
    print("=" * 70)

if __name__ == "__main__":
    run_evaluation()
