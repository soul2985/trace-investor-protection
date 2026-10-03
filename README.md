# TRACE — Scam & Claim Verifier
### Investor Safety Infrastructure
**SANGYAN Investor Resilience Hackathon • Track A (Digital Fraud & Scam Resilience) + Track E Elements**

[![Accuracy](https://img.shields.io/badge/Benchmark_Accuracy-100%25-brightgreen.svg)]()
[![SEBI Snapshot](https://img.shields.io/badge/SEBI_Snapshot-Oct_03,_2026-blue.svg)]()
[![Privacy](https://img.shields.io/badge/Privacy-No_Data_Stored-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

---

## 1. Product Identity & Purpose

**Trace** is a modern, minimal, trustworthy investor-protection application (PWA) built to protect first-time investors, senior citizens, and families in Tier-2/3 cities across India.

### What Trace Is:
* **Investor Safety Infrastructure**: Helps users verify suspicious investment messages, screenshots, voice notes, and links **before** money moves or an unknown APK is installed.
* **Deterministic Fact-Verification Engine**: Code rigorously verifies facts against an authentic dated snapshot of **3,321 official SEBI registered entities** (as of October 03, 2026) and 11 fraud rule categories with negation handling.
* **Empathetic Regional Translation**: Localized explanations, summaries, and audio readout in **English, Hindi (हिन्दी), and Marathi (मराठी)**.

### What Trace Is NOT:
* NOT a trading app or investment platform.
* NOT a stock-picking or financial advisory tool.
* NOT a fintech monetization product.
* Stores **NO** user messages, images, SMS, or OTPs.

---

## 2. Primary Demo Persona

* **Persona**: Ramesh, 62, retired school teacher residing in a Tier-2 city (Solapur/Nagpur/Nashik).
* **Language Comfort**: Marathi and Hindi.
* **Scenario**: Receives an urgent WhatsApp message claiming to be from a *"SEBI-registered analyst"* promising a *"guaranteed 40% monthly return"* with a link to *"download a private APK app not on Play Store"*.
* **Trace's Response**:
  1. Instant **High Risk** verdict with icon, color, and plain-language Marathi explanation.
  2. Audio readout reads the warning aloud in Marathi.
  3. Visual highlights on the exact suspicious phrases.
  4. Cross-checks claimed SEBI registration against official records.
  5. One-tap **Family Guardian Share** to inform his children.
  6. **"I Already Paid" (Recovery Mode)** with immediate 1930 helpline guidance and pre-filled cybercrime complaint drafting.

---

## 3. Four Conceptual Risk Outcomes

In strict adherence to the project rules, Trace never forces messages into binary "Scam" or "Safe" absolutes. It assesses risk honestly across 4 bands:

| Risk Outcome | Visual Representation | Meaning | Example |
| :--- | :--- | :--- | :--- |
| **HIGH RISK** | 🔴 Shield Alert (Red) | Multiple severe warning signs found | Guaranteed returns, APK downloads, personal UPI requests |
| **MEDIUM RISK** | 🟡 Warning Triangle (Amber) | Elements require caution before acting | VIP Telegram groups, unverified urgency |
| **LOW RISK** | 🟢 Shield Check (Green) | Standard official notice or verified SEBI entity | Authentic advisor disclosures, SIP debit notices |
| **CAN'T TELL** | ⚪ Help Circle (Slate/Amber) | Insufficient evidence to establish risk | Casual personal chat, ambiguous query |

---

## 4. Architecture & Pipeline

```mermaid
flowchart TD
    User([User: Ramesh / Family]) --> Input[Input: Paste Text / Screenshot OCR / Voice / Link]
    Input --> Frontend[Mobile-First PWA: React/Modern ESM + Tailwind]
    
    subgraph Backend_Pipeline ["FastAPI Fact-Verification Pipeline"]
        Frontend --> API["POST /api/analyze"]
        API --> Norm[1. Input Normalizer: Unicode / Homoglyphs]
        Norm --> Extractor[2. Entity Extractor: SEBI Reg, Phone, UPI, URLs, Names]
        
        Extractor --> ParallelChecks{"3. Parallel Verification"}
        ParallelChecks -->|11 Fraud Rules & Negations| Rules[Rule Engine: 11 Categories]
        ParallelChecks -->|Name & Number Match| SEBI[SEBI Snapshot Verifier: 3,321 Records]
        ParallelChecks -->|TLD & APK Checks| Link[Link & Reputation Checker]
        
        Rules --> Aggregator[4. Risk Aggregator]
        SEBI --> Aggregator
        Link --> Aggregator
        
        Aggregator --> Bands["Risk Outcome: HIGH / MEDIUM / LOW / CAN'T TELL"]
        
        Bands --> Explainer["5. Explainer & Localizer"]
        Explainer -.->|If GEMINI_API_KEY set| Gemini["Gemini Flash (Empathetic Analogy)"]
        Explainer -->|Offline Default| Templates["Localized Rule Templates (EN / HI / MR)"]
    end
    
    Explainer --> ResultScreen[Result Screen]
    ResultScreen --> Highlights[Message with Highlighted Phrases]
    ResultScreen --> SEBICard[SEBI Verification Status Card]
    ResultScreen --> AudioTTS[Audio Listen Button: Web Speech]
    ResultScreen --> Actions[Next Steps / Family Share / Recovery Mode]
```

---

## 5. Detection Rule Engine (11 Categories from `Fraud.docx`)

1. **`guaranteed_returns`**: Guaranteed, assured, or risk-free return promises.
2. **`unrealistic_returns`**: Unrealistic profit percentages (e.g. 40% monthly, doubling in 45 days).
3. **`fake_sebi_claim`**: Misuse of SEBI approval or registration to manufacture false credibility.
4. **`urgency_pressure`**: Artificial urgency (e.g. "15 minutes left", "only 10 slots remaining").
5. **`private_group`**: Exclusive Telegram or VIP WhatsApp group invitations.
6. **`insider_tip`**: Claims of insider calls or privileged market knowledge.
7. **`app_install`**: Pressure to install unknown APKs or apps outside Google Play Store.
8. **`remote_access`**: Requests for screen-sharing or remote device access (AnyDesk, TeamViewer).
9. **`personal_upi`**: Direct transfer requests to personal UPI accounts.
10. **`bank_transfer`**: Requests for private bank transfers bypassing official gateways.
11. **`withdrawal_fee`**: Demanding advance "fees" or "taxes" before releasing profits.

### Negation Handling Example:
* *"Get guaranteed 40% returns"* $\rightarrow$ **FLAGGED** (`guaranteed_returns`, `unrealistic_returns`).
* *"Mutual funds are subject to market risks, returns are NOT guaranteed"* $\rightarrow$ **NOT FLAGGED** (Negation detected).

---

## 6. Official SEBI Registry Snapshot

* **Snapshot Date**: October 03, 2026
* **Parsed Records**:
  * 1,050 Registered Investment Advisers (IA)
  * 2,271 Registered Research Analysts (RA)
  * Total: **3,321 Official SEBI Entities**
* **Impersonation Attack Detection**:
  * If a scammer quotes a real registration number (e.g., `INH000000016`) but gives a false sender name (e.g., *"Rajesh Sharma"*), Trace detects the discrepancy and flags:
    `FOUND_NAME_MISMATCH: Impersonation Alert! Registration belongs to STAKEHOLDERS EMPOWERMENT SERVICES, not the claimed sender.`

---

## 7. Benchmark Evaluation (100 Test Cases)

Trace includes an automated evaluation benchmark tested across all 50 synthetic scam messages from `Fraud.docx`, plus 25 genuine messages and 25 ambiguous messages:

```text
======================================================================
BENCHMARK EVALUATION RESULTS
======================================================================
Total Test Cases:            100
Scam Detection Rate:         100.0% (50/50)
Genuine Messages Correct:    100.0% (25/25)
False Positive Alarm Rate:   0.0%
Ambiguous / Can't Tell Rate: 100.0% (25/25)
Overall Benchmark Accuracy:  100.0%
======================================================================
```

---

## 8. Quick Start & Execution

### Prerequisites
* Python 3.10+
* Dependencies: `pip install -r requirements.txt`

### Start the Application (Single Command)
```bash
python run.py
```
Open **`http://localhost:8000`** in your browser.

### Run Unit Tests
```bash
python -m unittest backend/tests/test_rule_engine.py
```

### Run Accuracy Benchmark
```bash
python backend/tests/run_benchmark.py
```

---

## 9. Key Hackathon Deliverables & Features

* **Mobile-First PWA**: Installable on Android, iOS, and Desktop.
* **In-Browser OCR (Tesseract.js)**: Screenshot text extraction occurs entirely on the user's phone for privacy.
* **Audio Accessibility (Web Speech API)**: Speaks the verdict aloud in Hindi, Marathi, or English for low-literacy users.
* **Family Guardian Share**: Generates a clean, privacy-scrubbed summary card ready for 1-tap WhatsApp sharing.
* **Emergency Recovery Mode**: Golden Hour checklist, direct 1930 dialing, and pre-filled cybercrime complaint letters.
* **Judge Test Bench**: Built-in interactive drawer in the web UI allowing evaluators to run 1-click tests across all 100 benchmark scenarios.
