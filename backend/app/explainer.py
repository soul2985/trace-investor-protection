"""
Explainer module.
Generates localized, plain-language explanations in English, Hindi, and Marathi.
Combines deterministic templates with LLM enhancements when available.
"""
from typing import Dict, Any, List
from .llm_service import llm_service

SUMMARY_TEMPLATES = {
    "HIGH_RISK": {
        "en": "This message shows several serious warning signs commonly seen in investment fraud.",
        "hi": "यह संदेश निवेश धोखाधड़ी (स्कैम) में दिखने वाले कई गंभीर चेतावनी संकेत दिखाता है।",
        "mr": "हा संदेश गुंतवणूक फसवणुकीमध्ये आढळणारे अनेक गंभीर धोक्याचे इशारे दाखवतो."
    },
    "MEDIUM_RISK": {
        "en": "This message has elements that require caution before taking any action.",
        "hi": "इस संदेश में कुछ ऐसे तत्व हैं जिनके प्रति सतर्क रहना बहुत आवश्यक है।",
        "mr": "या संदेशात काही अशा गोष्टी आहेत ज्यांच्याबद्दल सावधगिरी बाळगणे आवश्यक आहे."
    },
    "LOW_RISK": {
        "en": "No major warning signs were found in this communication.",
        "hi": "इस संदेश में कोई बड़ा चेतावनी संकेत नहीं पाया गया।",
        "mr": "या संदेशात कोणताही मोठा धोक्याचा इशारा आढळला नाही."
    },
    "CANT_TELL": {
        "en": "We could not verify enough information from this message to determine risk.",
        "hi": "हम इस संदेश से जोखिम तय करने के लिए पर्याप्त जानकारी सत्यापित नहीं कर सके।",
        "mr": "जोखीम ठरवण्यासाठी या संदेशातून पुरेशी माहिती पडताळता आली नाही."
    }
}

NEXT_STEPS_TEMPLATES = {
    "HIGH_RISK": {
        "en": [
            "Do NOT transfer any money or enter your UPI PIN.",
            "Do NOT download any APK or grant screen-sharing permission.",
            "Check SEBI's official portal (sebi.gov.in) directly to verify any registered adviser.",
            "If pressured or already paid, report immediately at cybercrime.gov.in or call 1930."
        ],
        "hi": [
            "कोई भी पैसा ट्रांसफर न करें और न ही अपना UPI PIN दर्ज करें।",
            "कोई भी APK फ़ाइल डाउनलोड न करें और न ही स्क्रीन-शेयरिंग की अनुमति दें।",
            "सलाहकार की पुष्टि के लिए सेबी की आधिकारिक वेबसाइट (sebi.gov.in) देखें।",
            "यदि दबाव बनाया जा रहा है या पैसे दे दिए हैं, तो तुरंत 1930 पर कॉल करें या cybercrime.gov.in पर रिपोर्ट करें।"
        ],
        "mr": [
            "कोणतेही पैसे पाठवू नका किंवा तुमचा UPI PIN टाकू नका.",
            "कोणतीही APK फाईल डाउनलोड करू नका किंवा स्क्रीन शेअरिंग करू नका.",
            "सल्लागाराची खात्री करण्यासाठी सेबीच्या अधिकृत संकेतस्थळाला (sebi.gov.in) भेट द्या.",
            "दबाव आणला जात असल्यास किंवा पैसे भरले असल्यास, त्वरित 1930 वर संपर्क करा किंवा cybercrime.gov.in वर तक्रार नोंदवा."
        ]
    },
    "MEDIUM_RISK": {
        "en": [
            "Do not rush into any decision or click unfamiliar links.",
            "Ask a trusted family member or certified financial advisor to review the message.",
            "Never share bank details, OTPs, or passwords with unknown contacts."
        ],
        "hi": [
            "जल्दबाजी में कोई निर्णय न लें और अपरिचित लिंक पर क्लिक न करें।",
            "संदेश की समीक्षा के लिए किसी विश्वसनीय पारिवारिक सदस्य या प्रमाणित सलाहकार से बात करें।",
            "अज्ञात संपर्कों के साथ बैंक विवरण, ओटीपी या पासवर्ड कभी साझा न करें।"
        ],
        "mr": [
            "घाईघाईत कोणताही निर्णय घेऊ नका आणि अनोळखी लिंकवर क्लिक करू नका.",
            "कुटुंबातील विश्वासू व्यक्ती किंवा प्रमाणित आर्थिक सल्लागाराशी चर्चा करा.",
            "अनोळखी व्यक्तींशी बँक तपशील, ओटीपी किंवा पासवर्ड कधीही शेअर करू नका."
        ]
    },
    "LOW_RISK": {
        "en": [
            "The message appears consistent with routine official communications.",
            "Always verify investment transactions directly inside your authorized banking or demat app."
        ],
        "hi": [
            "संदेश सामान्य आधिकारिक सूचनाओं के अनुरूप प्रतीत होता है।",
            "हमेशा अपने अधिकृत बैंकिंग या डीमैट ऐप के माध्यम से ही लेन-देन की पुष्टि करें।"
        ],
        "mr": [
            "संदेश सामान्य अधिकृत संभाषणासारखा दिसत आहे.",
            "नेहमी तुमच्या अधिकृत बँकिंग किंवा डिमॅट अ‍ॅपद्वारेच व्यवहारांची खात्री करा."
        ]
    },
    "CANT_TELL": {
        "en": [
            "Verify the sender's identity independently through a phone call or trusted contact.",
            "Never send money or credentials without knowing exactly who is requesting them."
        ],
        "hi": [
            "संदेश भेजने वाले की पहचान फोन कॉल या विश्वसनीय संपर्क के माध्यम से स्वतंत्र रूप से सत्यापित करें।",
            "जब तक आप पूरी तरह सुनिश्चित न हों, पैसे या व्यक्तिगत जानकारी न भेजें।"
        ],
        "mr": [
            "फोन कॉलद्वारे किंवा विश्वासू ओळखीद्वारे पाठवणाऱ्या व्यक्तीची खात्री करा.",
            "पूर्ण खात्री असल्याशिवाय पैसे किंवा वैयक्तिक माहिती पाठवू नका."
        ]
    }
}

DEFAULT_ANALOGIES = {
    "HIGH_RISK": {
        "en": "Think of this like a stranger on the road offering to sell you pure gold for the price of iron, but demanding cash in a side alley. If it sounds too good to be true, it almost always is.",
        "hi": "इसे ऐसे समझें जैसे कोई अनजान व्यक्ति सड़क पर आपको लोहे के भाव में खरा सोना देने का दावा करे और सुनसान गली में नकद मांगे। अगर कोई सौदा जरूरत से ज्यादा अच्छा लगे, तो वह धोखा ही होता है।",
        "mr": "हे रस्त्यावरील अनोळखी व्यक्तीने लोखंडाच्या भावात अस्सल सोने देण्याचा दावा करण्यासारखे आहे. जर एखादी गोष्ट अवास्तव फायद्याची वाटत असेल, तर त्यात नक्कीच फसवणूक असते."
    },
    "MEDIUM_RISK": {
        "en": "Like an unlabelled medicine bottle—it might not be harmful, but you should never consume it without consulting a qualified doctor first.",
        "hi": "बिना लेबल वाली दवा की शीशी की तरह—हो सकता है यह नुकसान न करे, लेकिन डॉक्टर से पूछे बिना इसे लेना जोखिम भरा है।",
        "mr": "नाव नसलेल्या औषधाच्या बाटलीसारखे—ते घातक नसेलही, पण खात्री केल्याशिवाय त्याचा वापर करणे योग्य नाही."
    },
    "LOW_RISK": {
        "en": "Like an official sealed letter from a post office, carrying standard legal notices and warnings.",
        "hi": "पोस्ट ऑफिस से आए आधिकारिक सीलबंद पत्र की तरह, जिसमें मानक कानूनी चेतावनियां और सूचनाएं शामिल हैं।",
        "mr": "पोस्टातून आलेल्या अधिकृत पत्रासारखे, ज्यात नियमानुसार कायदेशीर माहिती आणि सूचना दिलेल्या असतात."
    },
    "CANT_TELL": {
        "en": "Like hearing a single sentence out of context—it is impossible to know what the conversation is really about without asking more questions.",
        "hi": "बिना संदर्भ की कोई एक बात सुनने की तरह—जब तक पूरी बात न पता चले, कोई निष्कर्ष निकालना संभव नहीं है।",
        "mr": "अर्धवट ऐकलेल्या वाक्यासारखे—जोपर्यंत पूर्ण संदर्भ समजत नाही, तोपर्यंत कोणताही अंदाज लावणे शक्य नाही."
    }
}

def generate_explanation(
    text: str,
    language: str,
    risk_band: str,
    sebi_results: Dict[str, Any],
    triggered_rules: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Produces final user-facing text, reasons, safety steps, and analogies.
    Uses LLM if available; otherwise uses deterministic localized templates.
    """
    lang = language if language in ["en", "hi", "mr"] else "en"
    
    # 1. Base template results
    summary = SUMMARY_TEMPLATES.get(risk_band, {}).get(lang, SUMMARY_TEMPLATES[risk_band]["en"])
    next_steps = NEXT_STEPS_TEMPLATES.get(risk_band, {}).get(lang, NEXT_STEPS_TEMPLATES[risk_band]["en"])
    analogy = DEFAULT_ANALOGIES.get(risk_band, {}).get(lang, DEFAULT_ANALOGIES[risk_band]["en"])
    check_type = "basic"

    # Extract reason explanations from triggered rules
    reasons = []
    for r in triggered_rules[:3]: # Show top 3 reasons as required by PRD
        reasons.append({
            "rule_id": r["rule_id"],
            "title": r["rule_name"],
            "description": r.get("explanation") or r["rule_name"]
        })

    # If no rules triggered, provide context reason
    if not reasons:
        if risk_band == "LOW_RISK":
            no_rule_text = {
                "en": "Standard regulatory disclosures and verified wording present.",
                "hi": "मानक विनियामक खुलासे और सामान्य आधिकारिक भाषा मौजूद है।",
                "mr": "मानक नियामक खुलासे आणि अधिकृत भाषा समाविष्ट आहे."
            }
            reasons.append({
                "rule_id": "regulatory_compliance",
                "title": "Clear Disclosures",
                "description": no_rule_text.get(lang, no_rule_text["en"])
            })
        elif risk_band == "CANT_TELL":
            cant_tell_text = {
                "en": "No specific investment offer or fraudulent pattern detected in this message.",
                "hi": "इस संदेश में कोई विशिष्ट निवेश प्रस्ताव या धोखाधड़ी का पैटर्न नहीं मिला।",
                "mr": "या संदेशात कोणतीही स्पष्ट गुंतवणूक योजना किंवा फसवणुकीची लक्षणे आढळली नाहीत."
            }
            reasons.append({
                "rule_id": "insufficient_context",
                "title": "Insufficient Context",
                "description": cant_tell_text.get(lang, cant_tell_text["en"])
            })

    # 2. Try LLM enhancement if key available
    if llm_service.is_available():
        llm_res = llm_service.explain(
            text=text,
            language=lang,
            risk_band=risk_band,
            sebi_status=sebi_results.get("status", "NONE_CLAIMED"),
            triggered_rules=triggered_rules
        )
        if llm_res:
            if llm_res.get("summary"):
                summary = llm_res["summary"]
            if llm_res.get("analogy"):
                analogy = llm_res["analogy"]
            check_type = "enhanced"

    return {
        "summary": summary,
        "reasons": reasons,
        "next_steps": next_steps,
        "analogy": analogy,
        "check_type": check_type, # "basic" or "enhanced"
        "language": lang
    }
