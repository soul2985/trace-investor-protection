"""
Entity extraction module.
Extracts SEBI registration numbers, URLs, UPI IDs, phone numbers, and monetary figures.
"""
import re
from typing import Dict, List, Any

# SEBI Registration regex (Investment Adviser INA, Research Analyst INH, etc.)
SEBI_REG_REGEX = re.compile(
    r"\b(IN[A-Z]\s*[-]?\s*\d{9})\b",
    re.IGNORECASE
)

# Common Indian UPI ID pattern
UPI_REGEX = re.compile(
    r"\b([a-zA-Z0-9.\-_]{2,256}@(okhdfcbank|oksbi|okaxis|okicici|paytm|ybl|axl|upi|apl|ibl|barodampay|federal|allbank|cnrb|postbank|idfcbank))\b",
    re.IGNORECASE
)

# Indian Phone numbers
PHONE_REGEX = re.compile(
    r"(?:\+91[\-\s]?)?[6-9]\d{9}\b"
)

# URLs and Links
URL_REGEX = re.compile(
    r"(?:https?:\/\/|www\.)[^\s/$.?#].[^\s]*",
    re.IGNORECASE
)

# Telegram / WhatsApp links specifically
MESSAGING_LINK_REGEX = re.compile(
    r"(?:https?:\/\/)?(?:t\.me\/[a-zA-Z0-9_+]+|chat\.whatsapp\.com\/[a-zA-Z0-9]+)",
    re.IGNORECASE
)

# Monetary figures and percentages
AMOUNT_REGEX = re.compile(
    r"(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d{1,2})?|\b\d+\s*(?:lakh|crore|k)\b",
    re.IGNORECASE
)

PERCENTAGE_REGEX = re.compile(
    r"\b\d{1,3}(?:\.\d{1,2})?\s*%",
    re.IGNORECASE
)

# Name extraction patterns ("I am <Name>", "Analyst <Name>", "Regards, <Name>", "Contact: <Name>")
NAME_PREFIX_REGEX = re.compile(
    r"(?i:I am|My name is|Analyst:?|Advisor:?|Research Analyst:?|Mr\.?|Mrs\.?|Ms\.?|Regards|Thanks|Best|Contact:?|From:?|Advice from|Advise by)[,\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})"
)

def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extracts structured entities from input text.
    """
    # 1. SEBI Registration numbers
    raw_sebi = SEBI_REG_REGEX.findall(text)
    cleaned_sebi = [re.sub(r"[\s\-]", "", r).upper() for r in raw_sebi]
    cleaned_sebi = list(dict.fromkeys(cleaned_sebi)) # Unique
    
    # 2. UPI IDs
    upi_matches = [m[0] for m in UPI_REGEX.findall(text)]
    upi_matches = list(dict.fromkeys(upi_matches))
    
    # 3. Phone numbers
    phone_matches = PHONE_REGEX.findall(text)
    phone_matches = list(dict.fromkeys(phone_matches))
    
    # 4. URLs
    urls = URL_REGEX.findall(text)
    messaging_links = MESSAGING_LINK_REGEX.findall(text)
    all_urls = list(dict.fromkeys(urls + messaging_links))
    
    # 5. Amounts & Percentages
    amounts = AMOUNT_REGEX.findall(text)
    percentages = PERCENTAGE_REGEX.findall(text)
    
    # 6. Potential names mentioned
    name_matches = NAME_PREFIX_REGEX.findall(text)
    claimed_names = list(dict.fromkeys(name_matches))

    return {
        "sebi_reg_numbers": cleaned_sebi,
        "upi_ids": upi_matches,
        "phone_numbers": phone_matches,
        "urls": all_urls,
        "amounts": amounts,
        "percentages": percentages,
        "claimed_names": claimed_names
    }
