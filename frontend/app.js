/**
 * TRACE — Investor Scam & Claim Verifier
 * Frontend Application Core
 */

// Application State
let currentLang = 'en';
let currentScreen = 'input';
let screenHistory = ['input'];
let lastAnalysisResult = null;
let currentMessage = '';
let recognition = null;
let isRecording = false;
let checkHistory = [];

// Multilingual UI Text Dictionary (EN, HI, MR)
const UI_TEXTS = {
  en: {
    input_title: "What did you receive?",
    input_sub: "Paste the message, upload a screenshot or speak it. We'll check for warning signs.",
    placeholder: "Paste message here...",
    action_upload: "Upload",
    action_camera: "Camera",
    action_speak: "Speak",
    action_link: "Link",
    check_now: "Check now",
    privacy_foot: "Your message is not stored.",
    analysing_title: "Analysing your message...",
    analysing_sub: "We're checking for warning signs and verifying key details. This usually takes a few seconds.",
    chk_1: "Reading message",
    chk_2: "Extracting key details",
    chk_3: "Checking SEBI records",
    chk_4: "Scanning for warning signs",
    chk_5: "Analysing with AI",
    chk_6: "Preparing your result",
    tip_title: "Did you know?",
    tip_desc: "Many investment scams use fake or stolen SEBI registration numbers to look genuine.",
    quick_summary_title: "Quick Summary",
    warning_signs_title: "Key Warning Signs",
    btn_see_details: "See full details",
    btn_next_steps: "What should you do now?",
    details_title: "Your message",
    details_sub: "We highlighted the parts that look suspicious.",
    extracted_title: "Extracted details",
    btn_to_action: "What should you do now?",
    action_title: "What should you do now?",
    action_sub: "Follow these steps to stay safe.",
    step1_title: "Do not transfer money",
    step1_desc: "Avoid sending money, paying verification fees, or sharing UPI details.",
    step2_title: "Do not install the app",
    step2_desc: "Do not download or install any unknown APK or grant screen-sharing permission.",
    step3_title: "Verify independently",
    step3_desc: "Check the person or firm on SEBI's official website (sebi.gov.in).",
    step4_title: "Report if needed",
    step4_desc: "Report this message on cybercrime.gov.in or call helpline 1930.",
    step5_title: "Share with family",
    step5_desc: "Let your family know about this message to prevent them from falling for it.",
    btn_open_reporting: "Open reporting guide",
    recovery_title: "Already paid?",
    recovery_sub: "Take action quickly. The golden hour response can freeze recipient accounts."
  },
  hi: {
    input_title: "आपको क्या संदेश मिला?",
    input_sub: "संदेश पेस्ट करें, स्क्रीनशॉट अपलोड करें या बोलकर बताएं। हम चेतावनी संकेतों की जांच करेंगे।",
    placeholder: "संदेश यहां पेस्ट करें...",
    action_upload: "अपलोड",
    action_camera: "कैमरा",
    action_speak: "बोलें",
    action_link: "लिंक",
    check_now: "जांच करें",
    privacy_foot: "आपका संदेश कहीं भी सुरक्षित (स्टोर) नहीं किया जाता।",
    analysing_title: "आपके संदेश का विश्लेषण हो रहा है...",
    analysing_sub: "हम चेतावनी संकेतों और आधिकारिक सेबी रिकॉर्ड की जांच कर रहे हैं।",
    chk_1: "संदेश पढ़ा जा रहा है",
    chk_2: "मुख्य विवरण निकाले जा रहे हैं",
    chk_3: "सेबी रिकॉर्ड की जांच हो रही है",
    chk_4: "चेतावनी संकेत खोजे जा रहे हैं",
    chk_5: "एआई द्वारा विश्लेषण",
    chk_6: "परिणाम तैयार किया जा रहा है",
    tip_title: "क्या आप जानते हैं?",
    tip_desc: "कई वित्तीय घोटालेबाज भरोसा जीतने के लिए नकली या चुराए गए सेबी नंबर का इस्तेमाल करते हैं।",
    quick_summary_title: "त्वरित सारांश",
    warning_signs_title: "मुख्य चेतावनी संकेत",
    btn_see_details: "पूरा विवरण देखें",
    btn_next_steps: "अब आपको क्या करना चाहिए?",
    details_title: "आपका संदेश",
    details_sub: "संदेश में जो हिस्से संदेहास्पद लगे उन्हें हमने हाइलाइट किया है।",
    extracted_title: "प्राप्त विवरण",
    btn_to_action: "अब आपको क्या करना चाहिए?",
    action_title: "अब आपको क्या करना चाहिए?",
    action_sub: "सुरक्षित रहने के लिए इन चरणों का पालन करें।",
    step1_title: "पैसे ट्रांसफर न करें",
    step1_desc: "पैसे भेजने, सत्यापन शुल्क देने या यूपीआई विवरण साझा करने से बचें।",
    step2_title: "ऐप इंस्टॉल न करें",
    step2_desc: "अज्ञात एपीके डाउनलोड न करें और न ही स्क्रीन-शेयरिंग की अनुमति दें।",
    step3_title: "स्वतंत्र रूप से जांचें",
    step3_desc: "सेबी की आधिकारिक वेबसाइट (sebi.gov.in) पर व्यक्ति या फर्म की जांच करें।",
    step4_title: "यदि आवश्यक हो तो शिकायत करें",
    step4_desc: "इस संदेश की सूचना cybercrime.gov.in पर दें या 1930 पर कॉल करें।",
    step5_title: "परिवार के साथ साझा करें",
    step5_desc: "अपने परिवार को इस बारे में बताएं ताकि वे धोखाधड़ी से बच सकें।",
    btn_open_reporting: "शिकायत गाइड खोलें",
    recovery_title: "क्या आप पहले ही पैसे दे चुके हैं?",
    recovery_sub: "तुरंत कदम उठाएं। पहले कुछ घंटों में की गई कार्रवाई से पैसे रोके जा सकते हैं।"
  },
  mr: {
    input_title: "तुम्हाला काय संदेश मिळाला?",
    input_sub: "संदेश पेस्ट करा, स्क्रीनशॉट अपलोड करा किंवा बोलून सांगा. आम्ही धोक्याची लक्षणे तपासू.",
    placeholder: "संदेश येथे पेस्ट करा...",
    action_upload: "अपलोड",
    action_camera: "कॅमेरा",
    action_speak: "बोला",
    action_link: "लिंक",
    check_now: "आता तपासा",
    privacy_foot: "तुमचा संदेश कुठेही साठवला जात नाही.",
    analysing_title: "संदेशाची तपासणी सुरू आहे...",
    analysing_sub: "आम्ही धोक्याचे इशारे आणि सेबीचे अधिकृत रेकॉर्ड पडताळत आहोत.",
    chk_1: "संदेश वाचत आहे",
    chk_2: "महत्त्वाचे तपशील काढत आहे",
    chk_3: "सेबी रेकॉर्ड तपासत आहे",
    chk_4: "धोक्याची लक्षणे शोधत आहे",
    chk_5: "एआय विश्‍लेषण सुरू आहे",
    chk_6: "निकाल तयार करत आहे",
    tip_title: "तुम्हाला माहित आहे का?",
    tip_desc: "अनेक गुंतवणूक भामटे विश्वास मिळवण्यासाठी खोटे किंवा चोरलेले सेबी नंबर वापरतात.",
    quick_summary_title: "थोडक्यात सारांश",
    warning_signs_title: "मुख्य धोक्याची लक्षणे",
    btn_see_details: "सविस्तर तपशील पहा",
    btn_next_steps: "आता काय करावे?",
    details_title: "तुमचा मूळ संदेश",
    details_sub: "संदेशातील संशयास्पद भाग आम्ही हायलाइट केले आहेत.",
    extracted_title: "मिळालेले तपशील",
    btn_to_action: "आता काय करावे?",
    action_title: "आता काय करावे?",
    action_sub: "सुरक्षित राहण्यासाठी खालील पायऱ्यांचे पालन करा.",
    step1_title: "पैसे ट्रान्सफर करू नका",
    step1_desc: "पैसे पाठवणे, व्हेरिफिकेशन फी भरणे किंवा यूपीआय माहिती देणे टाळा.",
    step2_title: "अ‍ॅप इन्स्टॉल करू नका",
    step2_desc: "कोणतेही अनोळखी एपीके डाऊनलोड करू नका किंवा स्क्रीन शेअर करू नका.",
    step3_title: "अधिकृत खात्री करा",
    step3_desc: "सेबीच्या अधिकृत वेबसाइटवर (sebi.gov.in) व्यक्ती किंवा कंपनी तपासा.",
    step4_title: "तक्रार नोंदवा",
    step4_desc: "या संदेशाबद्दल cybercrime.gov.in वर किंवा 1930 वर तक्रार करा.",
    step5_title: "कुटुंबाला सावध करा",
    step5_desc: "घरातील लोकांना याबद्दल सांगा जेणेकरून ते फसणार नाहीत.",
    btn_open_reporting: "तक्रार मार्गदर्शन उघडा",
    recovery_title: "आधीच पैसे भरले आहेत का?",
    recovery_sub: "त्वरित पाऊल उचला. सुरुवातीच्या काही तासांत कारवाई केल्यास पैसे वाचू शकतात."
  }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  applyLanguage(currentLang);
  initSpeechRecognition();
});

// Navigation Controller
function navigateTo(screenId) {
  const screens = ['input', 'analysing', 'result', 'details', 'action', 'recovery'];
  screens.forEach(s => {
    const el = document.getElementById(`screen-${s}`);
    if (el) {
      if (s === screenId) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    }
  });

  if (screenId !== currentScreen) {
    screenHistory.push(screenId);
    currentScreen = screenId;
  }

  // Back button visibility in navbar
  const backBtn = document.getElementById('nav-back-btn');
  const shareBtn = document.getElementById('nav-share-btn');
  if (screenId === 'input') {
    backBtn.classList.add('hidden');
    shareBtn.classList.add('hidden');
    updateBottomNav('check');
  } else {
    backBtn.classList.remove('hidden');
    if (screenId === 'result' || screenId === 'details' || screenId === 'action') {
      shareBtn.classList.remove('hidden');
    } else {
      shareBtn.classList.add('hidden');
    }
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
  lucide.createIcons();
}

function handleBackNavigation() {
  if (screenHistory.length > 1) {
    screenHistory.pop(); // Remove current screen
    const previous = screenHistory.pop(); // Get previous
    navigateTo(previous);
  } else {
    navigateTo('input');
  }
}

function updateBottomNav(activeTab) {
  ['check', 'history', 'help', 'settings'].forEach(tab => {
    const btn = document.getElementById(`bnav-${tab}`);
    if (btn) {
      if (tab === activeTab) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    }
  });
}

// Character Counter
function updateCharCount() {
  const input = document.getElementById('message-input');
  const counter = document.getElementById('char-counter');
  counter.innerText = `${input.value.length}/5000`;
}

function clearInput() {
  const input = document.getElementById('message-input');
  input.value = '';
  updateCharCount();
  input.focus();
}

// Language Dropdown Handler
function changeLanguage(lang) {
  currentLang = lang;
  applyLanguage(lang);
  document.getElementById('settings-lang-label').innerText = lang === 'hi' ? 'हिन्दी' : (lang === 'mr' ? 'मराठी' : 'English');

  // If already analyzed, re-run analysis in target language
  if (lastAnalysisResult && currentMessage) {
    submitAnalysis(true);
  }
}

function applyLanguage(lang) {
  const t = UI_TEXTS[lang] || UI_TEXTS.en;
  setText('txt-input-title', t.input_title);
  setText('txt-input-sub', t.input_sub);
  setText('txt-action-upload', t.action_upload);
  setText('txt-action-camera', t.action_camera);
  setText('txt-action-speak', t.action_speak);
  setText('txt-action-link', t.action_link);
  setText('txt-check-now', t.check_now);
  setText('txt-privacy-foot', t.privacy_foot);
  setText('txt-analysing-title', t.analysing_title);
  setText('txt-analysing-sub', t.analysing_sub);
  setText('txt-chk-1', t.chk_1);
  setText('txt-chk-2', t.chk_2);
  setText('txt-chk-3', t.chk_3);
  setText('txt-chk-4', t.chk_4);
  setText('txt-chk-5', t.chk_5);
  setText('txt-chk-6', t.chk_6);
  setText('txt-tip-title', t.tip_title);
  setText('txt-tip-desc', t.tip_desc);
  setText('txt-quick-summary-title', t.quick_summary_title);
  setText('txt-warning-signs-title', t.warning_signs_title);
  setText('txt-btn-see-details', t.btn_see_details);
  setText('txt-btn-next-steps', t.btn_next_steps);
  setText('txt-details-title', t.details_title);
  setText('txt-details-sub', t.details_sub);
  setText('txt-extracted-details-title', t.extracted_title);
  setText('txt-btn-to-action', t.btn_to_action);
  setText('txt-action-title', t.action_title);
  setText('txt-action-sub', t.action_sub);
  setText('txt-step1-title', t.step1_title);
  setText('txt-step1-desc', t.step1_desc);
  setText('txt-step2-title', t.step2_title);
  setText('txt-step2-desc', t.step2_desc);
  setText('txt-step3-title', t.step3_title);
  setText('txt-step3-desc', t.step3_desc);
  setText('txt-step4-title', t.step4_title);
  setText('txt-step4-desc', t.step4_desc);
  setText('txt-step5-title', t.step5_title);
  setText('txt-step5-desc', t.step5_desc);
  setText('txt-btn-open-reporting', t.btn_open_reporting);
  setText('txt-recovery-title', t.recovery_title);
  setText('txt-recovery-sub', t.recovery_sub);

  const inputEl = document.getElementById('message-input');
  if (inputEl) inputEl.placeholder = t.placeholder;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.innerText = text;
}

// 4 Compact Actions: Upload, Camera, Speak, Link
function triggerFilePicker() {
  document.getElementById('file-picker').click();
}

function triggerCameraPicker() {
  document.getElementById('camera-picker').click();
}

async function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  const banner = document.getElementById('status-banner');
  const bannerText = document.getElementById('status-banner-text');
  banner.classList.remove('hidden');
  bannerText.innerText = "Extracting text in-browser...";

  try {
    const ocrLang = currentLang === 'mr' || currentLang === 'hi' ? 'hin+eng' : 'eng';
    const result = await Tesseract.recognize(file, ocrLang);
    const text = result.data.text.trim();
    if (text) {
      document.getElementById('message-input').value = text;
      updateCharCount();
      showToast("Text extracted from image!");
    } else {
      showToast("No readable text detected in image.");
    }
  } catch (err) {
    console.error("OCR Error:", err);
    showToast("Could not extract text. Please paste manually.");
  } finally {
    banner.classList.add('hidden');
    event.target.value = ''; // Reset input
  }
}

function initSpeechRecognition() {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const input = document.getElementById('message-input');
      input.value = (input.value ? input.value + ' ' : '') + transcript;
      updateCharCount();
      showToast("Voice captured!");
      stopSpeech();
    };

    recognition.onerror = (e) => {
      console.warn("Speech recognition error:", e);
      showToast("Voice error. Please speak clearly.");
      stopSpeech();
    };

    recognition.onend = () => {
      stopSpeech();
    };
  }
}

function toggleSpeechInput() {
  if (!recognition) {
    showToast("Speech recognition not supported in this browser.");
    return;
  }
  if (isRecording) {
    recognition.stop();
    stopSpeech();
  } else {
    const code = currentLang === 'mr' ? 'mr-IN' : (currentLang === 'hi' ? 'hi-IN' : 'en-IN');
    recognition.lang = code;
    recognition.start();
    isRecording = true;
    document.getElementById('icon-mic').classList.add('text-[#D97762]', 'animate-pulse');
    showToast("Listening... Speak now");
  }
}

function stopSpeech() {
  isRecording = false;
  const icon = document.getElementById('icon-mic');
  if (icon) icon.classList.remove('text-[#D97762]', 'animate-pulse');
}

function promptLinkInput() {
  const url = prompt("Enter the website, Telegram or WhatsApp link to check:");
  if (url && url.trim()) {
    const input = document.getElementById('message-input');
    input.value = (input.value ? input.value + '\n' : '') + url.trim();
    updateCharCount();
  }
}

// Core Verification Pipeline (Fixing Bug #6: Instant and Guaranteed Response)
async function submitAnalysis(isLanguageRerun = false) {
  const input = document.getElementById('message-input');
  const text = input.value.trim();

  if (!text) {
    showToast("Please enter or paste a message to check.");
    input.focus();
    return;
  }

  currentMessage = text;

  // Immediately navigate to analysing screen
  navigateTo('analysing');

  // Fast reassuring progress ticks
  const resetChecklist = () => {
    for (let i = 1; i <= 6; i++) {
      const el = document.getElementById(`chk-step-${i}`);
      if (el) {
        el.className = "flex items-center gap-3 text-xs font-medium text-[#66716B]";
        el.innerHTML = `<i data-lucide="circle" class="w-4 h-4 text-[#AFC3B4]"></i> <span id="txt-chk-${i}">${el.innerText}</span>`;
      }
    }
  };
  resetChecklist();
  lucide.createIcons();

  let step = 1;
  const timer = setInterval(() => {
    if (step <= 6) {
      const el = document.getElementById(`chk-step-${step}`);
      if (el) {
        el.className = "flex items-center gap-3 text-xs font-semibold text-[#17201C]";
        el.innerHTML = `<i data-lucide="check-circle-2" class="w-4 h-4 text-[#4F806B]"></i> <span>${el.innerText}</span>`;
        lucide.createIcons();
      }
      step++;
    }
  }, 140);

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, language: currentLang })
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    lastAnalysisResult = data;

    // Save to local history
    addToHistory(text, data.risk_band);

    // Wait until checklist ticks finish (~840ms total), then immediately render
    setTimeout(() => {
      clearInterval(timer);
      renderAllScreens(data);
      navigateTo('result');
    }, 850);

  } catch (err) {
    clearInterval(timer);
    console.error("Verification failed:", err);
    showToast("Could not connect to verification server. Please ensure backend is running.");
    navigateTo('input');
  }
}

// Render All Screens
function renderAllScreens(data) {
  renderScreen03Result(data);
  renderScreen04Details(data);
  renderScreen08Recovery(data);
  renderShareModalPreview(data);
}

// Screen 03 — Result Rendering
function renderScreen03Result(data) {
  const card = document.getElementById('risk-result-card');
  const iconCircle = document.getElementById('risk-icon-circle');
  const title = document.getElementById('result-risk-title');
  const sub = document.getElementById('result-risk-sub');
  const confPill = document.getElementById('result-confidence-pill');
  const summaryText = document.getElementById('result-quick-summary-text');
  const warningList = document.getElementById('result-warning-list');
  const countBadge = document.getElementById('result-warning-count');

  // Format Risk State
  if (data.risk_band === 'HIGH_RISK') {
    card.className = "card-lg p-5 border border-[#D97762]/40 bg-[#FBE4DE] space-y-3";
    iconCircle.className = "w-10 h-10 rounded-full flex items-center justify-center font-bold bg-[#D97762] text-white shadow-sm";
    iconCircle.innerHTML = '<i data-lucide="alert-triangle" class="w-5 h-5"></i>';
    confPill.className = "text-xs font-bold px-3 py-1 rounded-full bg-white text-[#D97762] shadow-xs";
    title.className = "text-2xl font-bold leading-tight text-[#D97762]";
    title.innerText = currentLang === 'mr' ? 'अति धोकादायक' : (currentLang === 'hi' ? 'उच्च जोखिम' : 'High Risk');
    sub.innerText = data.summary;
  } else if (data.risk_band === 'MEDIUM_RISK') {
    card.className = "card-lg p-5 border border-[#D4A34A]/40 bg-[#F8EBCF] space-y-3";
    iconCircle.className = "w-10 h-10 rounded-full flex items-center justify-center font-bold bg-[#D4A34A] text-white shadow-sm";
    iconCircle.innerHTML = '<i data-lucide="alert-circle" class="w-5 h-5"></i>';
    confPill.className = "text-xs font-bold px-3 py-1 rounded-full bg-white text-[#D4A34A] shadow-xs";
    title.className = "text-2xl font-bold leading-tight text-[#D4A34A]";
    title.innerText = currentLang === 'mr' ? 'सावधगिरी आवश्यक' : (currentLang === 'hi' ? 'मध्यम जोखिम' : 'Medium Risk');
    sub.innerText = data.summary;
  } else if (data.risk_band === 'LOW_RISK') {
    card.className = "card-lg p-5 border border-[#4F806B]/40 bg-[#E4EFE9] space-y-3";
    iconCircle.className = "w-10 h-10 rounded-full flex items-center justify-center font-bold bg-[#4F806B] text-white shadow-sm";
    iconCircle.innerHTML = '<i data-lucide="check-circle" class="w-5 h-5"></i>';
    confPill.className = "text-xs font-bold px-3 py-1 rounded-full bg-white text-[#4F806B] shadow-xs";
    title.className = "text-2xl font-bold leading-tight text-[#4F806B]";
    title.innerText = currentLang === 'mr' ? 'कमी जोखीम' : (currentLang === 'hi' ? 'कम जोखिम' : 'Low Risk');
    sub.innerText = data.summary;
  } else {
    // CAN'T TELL
    card.className = "card-lg p-5 border border-[#E4E2DA] bg-[#E7F0F7] space-y-3";
    iconCircle.className = "w-10 h-10 rounded-full flex items-center justify-center font-bold bg-[#5B8FB9] text-white shadow-sm";
    iconCircle.innerHTML = '<i data-lucide="help-circle" class="w-5 h-5"></i>';
    confPill.className = "text-xs font-bold px-3 py-1 rounded-full bg-white text-[#5B8FB9] shadow-xs";
    title.className = "text-2xl font-bold leading-tight text-[#5B8FB9]";
    title.innerText = currentLang === 'mr' ? 'सांगता येत नाही' : (currentLang === 'hi' ? 'कहा नहीं जा सकता' : "Can't Tell");
    sub.innerText = data.summary;
  }

  confPill.innerText = `${data.confidence_score}% Confidence`;
  summaryText.innerText = data.summary;

  // Warning signs list
  warningList.innerHTML = '';
  countBadge.innerText = `${data.reasons.length} found`;
  if (data.reasons.length === 0) {
    warningList.innerHTML = `<div class="text-xs text-[#929A95] italic">No major red flags detected.</div>`;
  } else {
    data.reasons.forEach((r, idx) => {
      const item = document.createElement('div');
      item.className = "flex items-start gap-2.5 text-xs text-[#17201C] py-1 border-b border-[#F2EEE5] last:border-none";
      item.innerHTML = `
        <div class="w-5 h-5 rounded-full bg-[#FBE4DE] text-[#D97762] flex items-center justify-center flex-shrink-0 font-bold text-[10px] mt-0.5">
          ${idx + 1}
        </div>
        <div>
          <span class="font-semibold text-[#0F1F1A]">${r.title}</span>
          <p class="text-[11px] text-[#66716B] mt-0.5">${r.description}</p>
        </div>
      `;
      warningList.appendChild(item);
    });
  }

  lucide.createIcons();
}

// Screen 04 — Details Screen Rendering
function renderScreen04Details(data) {
  // 1. Highlighted Original Message
  const box = document.getElementById('details-highlighted-box');
  renderHighlightedText(box, currentMessage, data.highlights);

  // 2. Extracted Details
  const extractedList = document.getElementById('extracted-details-list');
  extractedList.innerHTML = '';

  const addDetailRow = (icon, label, value, statusBadge = null) => {
    const row = document.createElement('div');
    row.className = "flex items-center justify-between py-1.5 border-b border-[#F2EEE5] last:border-none";
    let badgeHtml = '';
    if (statusBadge) {
      const color = statusBadge.color === 'red' ? 'bg-[#FBE4DE] text-[#D97762]' : (statusBadge.color === 'green' ? 'bg-[#E4EFE9] text-[#4F806B]' : 'bg-gray-100 text-gray-700');
      badgeHtml = `<span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${color}">${statusBadge.text}</span>`;
    }
    row.innerHTML = `
      <div class="flex items-center gap-2 text-[#66716B]">
        <i data-lucide="${icon}" class="w-3.5 h-3.5 text-[#929A95]"></i>
        <span>${label}</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="font-medium text-[#0F1F1A]">${value}</span>
        ${badgeHtml}
      </div>
    `;
    extractedList.appendChild(row);
  };

  const firmName = data.entities.claimed_names[0] || (data.sebi_check.details ? data.sebi_check.details.registered_name : 'Not verified');
  addDetailRow('user', 'Person / Firm name', firmName);

  if (data.sebi_check.claimed_number) {
    const isFound = data.sebi_check.status === 'FOUND_NAME_MATCH';
    const isMismatch = data.sebi_check.status === 'FOUND_NAME_MISMATCH';
    const badge = isFound ? { text: 'Found', color: 'green' } : (isMismatch ? { text: 'Mismatch', color: 'red' } : { text: 'Not found', color: 'red' });
    addDetailRow('landmark', 'SEBI Registration No.', data.sebi_check.claimed_number, badge);
  } else {
    addDetailRow('landmark', 'SEBI Registration No.', 'None claimed');
  }

  if (data.entities.urls && data.entities.urls.length > 0) {
    const isApk = data.link_check.some(l => l.is_apk);
    addDetailRow('link', 'Link', data.entities.urls[0].slice(0, 24) + '...', isApk ? { text: 'Suspicious!', color: 'red' } : null);
  }

  if (data.entities.phone_numbers && data.entities.phone_numbers.length > 0) {
    addDetailRow('phone', 'Phone number', data.entities.phone_numbers[0]);
  }

  if (data.entities.upi_ids && data.entities.upi_ids.length > 0) {
    addDetailRow('credit-card', 'UPI ID', data.entities.upi_ids[0], { text: 'Personal UPI', color: 'red' });
  }

  // 3. SEBI Verification Card
  const sebiBadge = document.getElementById('details-sebi-badge');
  const sebiInfo = document.getElementById('details-sebi-info');
  const sc = data.sebi_check;

  if (sc.status === 'FOUND_NAME_MATCH') {
    sebiBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E4EFE9] text-[#4F806B]";
    sebiBadge.innerText = "FOUND";
    sebiInfo.innerHTML = `
      <p class="font-bold text-[#0F1F1A]">${sc.details.registered_name}</p>
      <p>Registration: <span class="font-mono">${sc.claimed_number}</span> (${sc.details.type})</p>
      <p class="text-[11px] text-[#929A95]">Verified against official SEBI snapshot (${sc.snapshot_date}).</p>
    `;
  } else if (sc.status === 'FOUND_NAME_MISMATCH') {
    sebiBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#FBE4DE] text-[#D97762]";
    sebiBadge.innerText = "NAME MISMATCH";
    sebiInfo.innerHTML = `
      <p class="font-bold text-[#D97762]">Impersonation Warning!</p>
      <p>Number ${sc.claimed_number} is officially registered to <strong>"${sc.details.registered_name}"</strong>, not the sender.</p>
    `;
  } else if (sc.status === 'NOT_FOUND') {
    sebiBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#FBE4DE] text-[#D97762]";
    sebiBadge.innerText = "NOT FOUND";
    sebiInfo.innerHTML = `<p>${sc.message}</p>`;
  } else {
    sebiBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-700";
    sebiBadge.innerText = "NO CLAIM";
    sebiInfo.innerHTML = `<p>No SEBI registration number was claimed in this message to verify.</p>`;
  }

  lucide.createIcons();
}

function renderHighlightedText(container, text, highlights) {
  if (!highlights || highlights.length === 0) {
    container.innerText = text;
    return;
  }

  let html = '';
  let cursor = 0;

  highlights.forEach(h => {
    const start = Math.max(0, h.start);
    const end = Math.min(text.length, h.end);
    if (start > cursor) {
      html += escapeHtml(text.slice(cursor, start));
    }
    const phrase = text.slice(start, end);
    html += `<mark class="highlight-phrase" title="${escapeHtml(h.rule_name)}">${escapeHtml(phrase)}</mark>`;
    cursor = end;
  });

  if (cursor < text.length) {
    html += escapeHtml(text.slice(cursor));
  }

  container.innerHTML = html;
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function copyOriginalMessage() {
  navigator.clipboard.writeText(currentMessage).then(() => {
    showToast("Message copied!");
  });
}

// Screen 08 — Recovery Guide Rendering
function renderScreen08Recovery(data) {
  const upi = data.entities.upi_ids.join(', ') || 'N/A';
  const phone = data.entities.phone_numbers.join(', ') || 'N/A';
  const amount = data.entities.amounts.join(', ') || 'N/A';
  const date = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

  const draft = `To: The Cyber Crime Cell / Bank Fraud Grievance Officer
Subject: Urgent Complaint Regarding Financial Extortion & Account Freeze Request

Sir/Madam,
I am submitting an urgent report regarding fraudulent investment solicitations via messaging platforms.

Incident Particulars:
- Incident Date: ${date}
- Fraudulent UPI/Account Provided: ${upi}
- Contact/Phone Number: ${phone}
- Disputed Transaction Amount: ${amount}
- Scam Modus: ${data.summary}

Please immediately issue an account freeze notice to the beneficiary institution under 1930 Cybercrime SOP and initiate transaction recall procedures.

Sincerely,
[Your Name]
[Your Phone Number]`;

  document.getElementById('recovery-complaint-draft').value = draft;
}

function copyComplaintText() {
  const el = document.getElementById('recovery-complaint-draft');
  navigator.clipboard.writeText(el.value).then(() => {
    showToast("Complaint draft copied!");
  });
}

// Screen 09 — Share Modal
function openShareModal() {
  if (!lastAnalysisResult) return;
  const modal = document.getElementById('modal-share');
  modal.classList.remove('hidden');
  renderShareModalPreview(lastAnalysisResult);
}

function closeShareModal() {
  document.getElementById('modal-share').classList.add('hidden');
}

function renderShareModalPreview(data) {
  const preview = document.getElementById('share-card-preview');
  const riskTitle = data.risk_band === 'HIGH_RISK' ? 'High Risk' : (data.risk_band === 'MEDIUM_RISK' ? 'Medium Risk' : (data.risk_band === 'LOW_RISK' ? 'Low Risk' : "Can't Tell"));
  const reasons = data.reasons.slice(0, 3).map(r => `• ${r.title}`).join('<br>');

  preview.innerHTML = `
    <div class="flex items-center gap-1.5 font-bold text-xs text-[#0F1F1A]">
      <img src="/static/assets/logo.png" class="w-4 h-4 object-contain">
      <span>TRACE Verification Summary</span>
    </div>
    <div class="font-bold text-sm ${data.risk_band === 'HIGH_RISK' ? 'text-[#D97762]' : 'text-[#1F3A32]'}">${riskTitle} (${data.confidence_score}% confidence)</div>
    <p class="text-xs text-[#66716B] italic">"${data.summary}"</p>
    <div class="pt-1 text-[11px] text-[#17201C]">${reasons}</div>
  `;
}

function getShareText() {
  if (!lastAnalysisResult) return '';
  const reasons = lastAnalysisResult.reasons.slice(0, 3).map(r => `• ${r.title}`).join('\n');
  return `TRACE Investor Safety Alert:\nRisk Level: ${lastAnalysisResult.risk_band}\n${lastAnalysisResult.summary}\n\nKey Signs:\n${reasons}\n\nAdvice: Do not send money or install unknown APKs. Verify advisors on sebi.gov.in.`;
}

function shareViaWhatsApp() {
  const text = encodeURIComponent(getShareText());
  window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
}

function copyShareText() {
  navigator.clipboard.writeText(getShareText()).then(() => {
    showToast("Summary copied to clipboard!");
    closeShareModal();
  });
}

// Local Session History
function addToHistory(text, riskBand) {
  checkHistory.unshift({
    text: text.slice(0, 70) + (text.length > 70 ? '...' : ''),
    risk_band: riskBand,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });
  if (checkHistory.length > 20) checkHistory.pop();
}

function openHistoryModal() {
  const modal = document.getElementById('modal-history');
  const container = document.getElementById('history-items-container');
  container.innerHTML = '';

  if (checkHistory.length === 0) {
    container.innerHTML = `<div class="text-center py-6 text-[#929A95]">No checks yet in this session.</div>`;
  } else {
    checkHistory.forEach(item => {
      const row = document.createElement('div');
      const badge = item.risk_band === 'HIGH_RISK' ? 'bg-[#FBE4DE] text-[#D97762]' : (item.risk_band === 'LOW_RISK' ? 'bg-[#E4EFE9] text-[#4F806B]' : 'bg-[#F8EBCF] text-[#D4A34A]');
      row.className = "p-2.5 rounded-xl border border-[#E4E2DA] bg-[#F7F2E9]/50 flex items-center justify-between";
      row.innerHTML = `
        <div class="overflow-hidden pr-2">
          <p class="font-medium text-xs text-[#0F1F1A] truncate">${item.text}</p>
          <span class="text-[10px] text-[#929A95]">${item.timestamp}</span>
        </div>
        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${badge} flex-shrink-0">${item.risk_band.replace('_', ' ')}</span>
      `;
      container.appendChild(row);
    });
  }

  modal.classList.remove('hidden');
  updateBottomNav('history');
}

function closeHistoryModal() {
  document.getElementById('modal-history').classList.add('hidden');
  updateBottomNav('check');
}

function clearHistory() {
  checkHistory = [];
  openHistoryModal();
}

// Help & Settings Modals
function openHelpModal() {
  document.getElementById('modal-help').classList.remove('hidden');
  updateBottomNav('help');
}

function closeHelpModal() {
  document.getElementById('modal-help').classList.add('hidden');
  updateBottomNav('check');
}

function openSettingsModal() {
  document.getElementById('modal-settings').classList.remove('hidden');
  updateBottomNav('settings');
}

function closeSettingsModal() {
  document.getElementById('modal-settings').classList.add('hidden');
  updateBottomNav('check');
}

// Toast
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.classList.remove('opacity-0', 'pointer-events-none');
  setTimeout(() => {
    toast.classList.add('opacity-0', 'pointer-events-none');
  }, 2500);
}
