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
                "mr": "हा संदेश गुंतवणूक फसवणुकीमध्ये आढळणारे अनेक गंभीर धोक्याचे इशारे दाखवतो.",
        "ta": "இந்த செய்தியில் முதலீட்டு மோசடிகளில் பொதுவாக காணப்படும் பல தீவிர எச்சரிக்கை அறிகுறிகள் உள்ளன.",
        "te": "ఈ సందేశంలో పెట్టుబడి మోసాల్లో సాధారణంగా కనిపించే అనేక తీవ్రమైన హెచ్చరిక సంకేతాలు ఉన్నాయి.",
        "bn": "এই বার্তাটি বিনিয়োগ জালিয়াতিতে দেখা যায় এমন বেশ কয়েকটি গুরুতর সতর্কতা সংকেত দেখায়।"
    },
    "MEDIUM_RISK": {
        "en": "This message has elements that require caution before taking any action.",
        "hi": "इस संदेश में कुछ ऐसे तत्व हैं जिनके प्रति सतर्क रहना बहुत आवश्यक है।",
                "mr": "या संदेशात काही अशा गोष्टी आहेत ज्यांच्याबद्दल सावधगिरी बाळगणे आवश्यक आहे.",
        "ta": "எந்த நடவடிக்கையும் எடுப்பதற்கு முன் இந்த செய்தியில் எச்சரிக்கையாக இருக்க வேண்டிய விஷயங்கள் உள்ளன.",
        "te": "ఏదైనా చర్య తీసుకునే ముందు ఈ సందేశంలో జాగ్రత్త వహించాల్సిన విషయాలు ఉన్నాయి.",
        "bn": "কোনো পদক্ষেপ নেওয়ার আগে এই বার্তাটির বিষয়ে সতর্ক থাকা প্রয়োজন।"
    },
    "LOW_RISK": {
        "en": "No major warning signs were found in this communication.",
        "hi": "इस संदेश में कोई बड़ा चेतावनी संकेत नहीं पाया गया।",
                "mr": "या संदेशात कोणताही मोठा धोक्याचा इशारा आढळला नाही.",
        "ta": "இந்த செய்தியில் எந்த பெரிய எச்சரிக்கை அறிகுறிகளும் கண்டறியப்படவில்லை.",
        "te": "ఈ సందేశంలో ఏ పెద్ద హెచ్చరిక సంకేతాలు కనుగొనబడలేదు.",
        "bn": "এই বার্তায় কোনো বড় সতর্কবার্তা পাওয়া যায়নি।"
    },
    "CANT_TELL": {
        "en": "We could not verify enough information from this message to determine risk.",
        "hi": "हम इस संदेश से जोखिम तय करने के लिए पर्याप्त जानकारी सत्यापित नहीं कर सके।",
                "mr": "जोखीम ठरवण्यासाठी या संदेशातून पुरेशी माहिती पडताळता आली नाही.",
        "ta": "அபாயத்தை தீர்மானிக்க இந்த செய்தியிலிருந்து போதிய தகவல்களை சரிபார்க்க முடியவில்லை.",
        "te": "ప్రమాదాన్ని నిర్ధారించడానికి ఈ సందేశం నుండి తగినంత సమాచారాన్ని ధృవీకరించలేకపోయాము.",
        "bn": "ঝুঁকি নির্ধারণের জন্য এই বার্তা থেকে পর্যাপ্ত তথ্য যাচাই করা যায়নি।"
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
        ],
        "ta": [
            "எந்த பணத்தையும் அனுப்ப வேண்டாம் மற்றும் உங்கள் UPI PIN ஐ உள்ளிட வேண்டாம்.",
            "எந்த APK கோப்பையும் பதிவிறக்க வேண்டாம் மற்றும் ஸ்கிரீன் ஷேரிங் செய்ய வேண்டாம்.",
            "அங்கீகரிக்கப்பட்ட ஆலோசகரை சரிபார்க்க செபியின் அதிகாரப்பூர்வ தளத்தை (sebi.gov.in) பார்க்கவும்.",
            "பணம் செலுத்தியிருந்தால் அல்லது வற்புறுத்தப்பட்டால் உடனடியாக 1930 ஐ அழைக்கவும் அல்லது cybercrime.gov.in இல் புகார் செய்யவும்."
        ],
        "te": [
            "ఎటువంటి డబ్బును బదిలీ చేయవద్దు మరియు మీ UPI PIN ని నమోదు చేయవద్దు.",
            "ఏదైనా APK ఫైల్‌ను డౌన్‌లోడ్ చేయవద్దు మరియు స్క్రీన్ షేరింగ్ అనుమతించవద్దు.",
            "నమోదిత సలహాదారుని ధృవీకరించడానికి సెబీ అధికారిక పోర్టల్ (sebi.gov.in) ను చూడండి.",
            "ఒత్తిడి తెచ్చినా లేదా ఇప్పటికే చెల్లించినా వెంటనే 1930 కి కాల్ చేయండి లేదా cybercrime.gov.in లో నివేదించండి."
        ],
        "bn": [
            "কোনো টাকা পাঠাবেন না বা আপনার UPI PIN লিখবেন না।",
            "কোনো APK ফাইল ডাউনলোড করবেন না বা স্ক্রিন শেয়ার করবেন না।",
            "নিবন্ধিত উপদেষ্টাকে যাচাই করতে সরাসরি সেবির অফিসিয়াল পোর্টাল (sebi.gov.in) দেখুন।",
            "টাকা দিয়ে থাকলে বা চাপ দিলে অবিলম্বে ১৯৩০ নম্বরে কল করুন বা cybercrime.gov.in-এ অভিযোগ জানান।"
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
        ],
        "ta": [
            "அவசரப்பட்டு எந்த முடிவும் எடுக்க வேண்டாம் அல்லது தெரியாத இணைப்புகளை கிளிக் செய்ய வேண்டாம்.",
            "செய்தியை மதிப்பாய்வு செய்ய குடும்ப உறுப்பினர் அல்லது நிதி ஆலோசகரிடம் பேசுங்கள்.",
            "தெரியாத நபர்களிடம் வங்கி விவரங்கள், OTP அல்லது கடவுச்சொற்களை பகிர வேண்டாம்."
        ],
        "te": [
            "హడావుడిగా ఎటువంటి నిర్ణయం తీసుకోవద్దు లేదా తెలియని లింక్‌లను క్లిక్ చేయవద్దు.",
            "సందేశాన్ని సమీక్షించడానికి నమ్మకమైన కుటుంబ సభ్యుడు లేదా ఆర్థిక సలహాదారుతో మాట్లాడండి.",
            "తెలియని వ్యక్తులతో బ్యాంక్ వివరాలు, OTPలు లేదా పాస్‌వర్డ్‌లను ఎప్పుడూ పంచుకోవద్దు."
        ],
        "bn": [
            "তাড়াহুড়ো করে কোনো সিদ্ধান্ত নেবেন না বা অচেনা লিঙ্কে ক্লিক করবেন না।",
            "বার্তাটি পর্যালোচনা করার জন্য কোনো বিশ্বস্ত পরিবারের সদস্য বা উপদেষ্টার সাথে কথা বলুন।",
            "অপরিচিত ব্যক্তিদের সাথে ব্যাংকের বিবরণ, OTP বা পাসওয়ার্ড কখনই শেয়ার করবেন না।"
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
        ],
        "ta": [
            "செய்தி சாதாரண அதிகாரப்பூர்வ தகவல்களுடன் ஒத்துப்போகிறது.",
            "உங்கள் அதிகாரப்பூர்வ வங்கி பயன்பாட்டிற்குள் நேரடியாக பரிவர்த்தனைகளை சரிபார்க்கவும்."
        ],
        "te": [
            "సందేశం సాధారణ అధికారిక సమాచారానికి అనుగుణంగా ఉంది.",
            "మీ అధికారిక బ్యాంకింగ్ లేదా డీమ్యాట్ యాప్ ద్వారా నేరుగా లావాదేవీలను ధృవీకరించండి."
        ],
        "bn": [
            "বার্তাটি সাধারণ অফিসিয়াল বার্তার মতো দেখাচ্ছে।",
            "সর্বদা আপনার অনুমোদিত ব্যাংকিং অ্যাপের মাধ্যমে লেনদেন নিশ্চিত করুন।"
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
        ],
        "ta": [
            "போன் கால் அல்லது நம்பகமான நபர் மூலம் அனுப்புனரின் அடையாளத்தை சரிபார்க்கவும்.",
            "யார் கேட்கிறார்கள் என்று தெரியாமல் பணத்தையோ தகவலையோ அனுப்ப வேண்டாம்."
        ],
        "te": [
            "ఫోన్ కాల్ లేదా నమ్మకమైన పరిచయం ద్వారా పంపినవారి గురింపును స్వతంత్రంగా ధృవీకరించండి.",
            "ఎవరు అడుగుతున్నారో తెలియకుండా ఎప్పుడూ డబ్బు లేదా ఆధారాలను పంపవద్దు."
        ],
        "bn": [
            "ফোন কল বা বিশ্বস্ত পরিচিতির মাধ্যমে প্রেরকের পরিচয় যাচাই করুন।",
            "কে অনুরোধ করছে তা না জেনে কখনই টাকা বা তথ্য পাঠাবেন না।"
        ]
    }
}

DEFAULT_ANALOGIES = {
    "HIGH_RISK": {
        "en": "Think of this like a stranger on the road offering to sell you pure gold for the price of iron, but demanding cash in a side alley. If it sounds too good to be true, it almost always is.",
        "hi": "इसे ऐसे समझें जैसे कोई अनजान व्यक्ति सड़क पर आपको लोहे के भाव में खरा सोना देने का दावा करे और सुनसान गली में नकद मांगे। अगर कोई सौदा जरूरत से ज्यादा अच्छा लगे, तो वह धोखा ही होता है।",
                "mr": "हे रस्त्यावरील अनोळखी व्यक्तीने लोखंडाच्या भावात अस्सल सोने देण्याचा दावा करण्यासारखे आहे. जर एखादी गोष्ट अवास्तव फायद्याची वाटत असेल, तर त्यात नक्कीच फसवणूक असते.",
        "ta": "சாலையில் செல்லும் தெரியாத நபர் இரும்பு விலைக்கு தங்கம் தருவதாக கூறி சந்துக்குள் வர சொல்வது போன்றது இது. அளவுக்கு அதிகமாக ஆசை காட்டினால் அது மோசடியே.",
        "te": "రోడ్డుపై వెళ్తున్న తెలియని వ్యక్తి ఇనుము ధరకు స్వచ్ఛమైన బంగారాన్ని ఇస్తానని సందులోకి రమ్మని అడగడం లాంటిది ఇది. అతిగా అనిపిస్తే అది మోసమే.",
        "bn": "এটি রাস্তায় কোনো অচেনা লোকের লোহার দামে খাঁটি সোনা বেচার অফারের মতো, যা গলির ভেতরে নগদ চায়। অতিরিক্ত সুবিধাজনক মনে হলে তা প্রতারণাই।"
    },
    "MEDIUM_RISK": {
        "en": "Like an unlabelled medicine bottle—it might not be harmful, but you should never consume it without consulting a qualified doctor first.",
        "hi": "बिना लेबल वाली दवा की शीशी की तरह—हो सकता है यह नुकसान न करे, लेकिन डॉक्टर से पूछे बिना इसे लेना जोखिम भरा है।",
                "mr": "नाव नसलेल्या औषधाच्या बाटलीसारखे—ते घातक नसेलही, पण खात्री केल्याशिवाय त्याचा वापर करणे योग्य नाही.",
        "ta": "லேபிள் இல்லாத மருந்து பாட்டில் போன்றது—இது தீங்கற்றதாக இருக்கலாம், ஆனால் மருத்துவரை கலந்தாலோசிக்காமல் சாப்பிடக்கூடாது.",
        "te": "లేబుల్ లేని మందు బాటిల్ లాంటిది—ఇది హానికరం కాకపోవచ్చు, కానీ డాక్టర్‌ని సంప్రదించకుండా వాడకూడదు.",
        "bn": "লেবেল ছাড়া ওষুধের বোতলের মতো—এটি ক্ষতিকারক না-ও হতে পারে, তবে ডাক্তারের পরামর্শ ছাড়া খাওয়া উচিত নয়।"
    },
    "LOW_RISK": {
        "en": "Like an official sealed letter from a post office, carrying standard legal notices and warnings.",
        "hi": "पोस्ट ऑफिस से आए आधिकारिक सीलबंद पत्र की तरह, जिसमें मानक कानूनी चेतावनियां और सूचनाएं शामिल हैं।",
                "mr": "पोस्टातून आलेल्या अधिकृत पत्रासारखे, ज्यात नियमानुसार कायदेशीर माहिती आणि सूचना दिलेल्या असतात.",
        "ta": "தபால் நிலையத்திலிருந்து வந்த அதிகாரப்பூர்வ முத்திரையிடப்பட்ட கடிதம் போன்றது.",
        "te": "తపాల కార్యాలయం నుండి వచ్చిన అధికారిక సీలు వేసిన ఉత్తరం లాంటిది.",
        "bn": "ডাকঘর থেকে আসা অফিসিয়াল সিল করা চিঠির মতো।"
    },
    "CANT_TELL": {
        "en": "Like hearing a single sentence out of context—it is impossible to know what the conversation is really about without asking more questions.",
        "hi": "बिना संदर्भ की कोई एक बात सुनने की तरह—जब तक पूरी बात न पता चले, कोई निष्कर्ष निकालना संभव नहीं है।",
                "mr": "अर्धवट ऐकलेल्या वाक्यासारखे—जोपर्यंत पूर्ण संदर्भ समजत नाही, तोपर्यंत कोणताही अंदाज लावणे शक्य नाही.",
        "ta": "சூழல் தெரியாமல் அரைகுறையாக கேட்ட ஒரு வாக்கியம் போன்றது.",
        "te": "సందర్భం లేకుండా విన్న ఒకే వాక్యం లాంటిది.",
        "bn": "প্রসঙ্গ ছাড়া শোনা একটি বাক্যের মতো—সম্পূর্ণ তথ্য ছাড়া কিছু বলা সম্ভব নয়।"
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
    lang = language if language in ["en", "hi", "ta", "te", "bn", "mr"] else "en"
    
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
                                "mr": "मानक नियामक खुलासे आणि अधिकृत भाषा समाविष्ट आहे.",
                "ta": "சாதாரண அதிகாரப்பூர்வ விதிமுறைகள் மற்றும் சரிபார்க்கப்பட்ட வார்த்தைகள் உள்ளன.",
                "te": "సాధారణ నియంత్రణ వెల్లడిలు మరియు ధృవీకరించబడిన పదాలు ఉన్నాయి.",
                "bn": "মানক নিয়ন্ত্রক প্রকাশ এবং যাচাইকৃত শব্দ উপস্থিত রয়েছে।"
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
                                "mr": "या संदेशात कोणतीही स्पष्ट गुंतवणूक योजना किंवा फसवणुकीची लक्षणे आढळली नाहीत.",
                "ta": "இந்த செய்தியில் குறிப்பிட்ட முதலீட்டு சலுகையோ அல்லது மோசடி அமைப்போ கண்டறியப்படவில்லை.",
                "te": "ఈ సందేశంలో ఎటువంటి నిర్దిష్ట పెట్టుబడి ఆఫర్ లేదా మోసపూరిత నమూనా కనుగొనబడలేదు.",
                "bn": "এই বার্তায় কোনো নির্দিষ্ট বিনিয়োগ অফার বা প্রতারণামূলক প্যাটার্ন পাওয়া যায়নি।"
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
