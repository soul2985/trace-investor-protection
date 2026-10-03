"""
Input normalization module.
Removes zero-width characters, homoglyphs, and obfuscations.
"""
import re
import unicodedata

# Common zero-width and invisible unicode characters
ZERO_WIDTH_CHARS = [
    '\u200b',  # zero width space
    '\u200c',  # zero width non-joiner (preserve in Devanagari only if part of word, else clean)
    '\u200d',  # zero width joiner
    '\ufeff',  # byte order mark / zero width no-break space
    '\u200e',  # left-to-right mark
    '\u200f',  # right-to-left mark
    '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',  # directional formatting
    '\u2060',  # word joiner
]

# Basic Cyrillic to Latin homoglyphs often used in phishing
HOMOGLYPH_MAP = {
    'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o', 'р': 'p', 'ѕ': 's',
    'х': 'x', 'у': 'y', 'і': 'i', 'ј': 'j', 'А': 'A', 'В': 'B',
    'С': 'C', 'Е': 'E', 'Н': 'H', 'І': 'I', 'Ј': 'J', 'К': 'K',
    'М': 'M', 'О': 'O', 'Р': 'P', 'Т': 'T', 'Х': 'X'
}

def normalize_text(text: str) -> str:
    """
    Cleans raw user input while preserving Hindi and Marathi Devanagari scripts.
    """
    if not text:
        return ""
    
    # Standardize unicode normalization form
    text = unicodedata.normalize("NFKC", text)
    
    # Strip dangerous zero-width and invisible characters
    for ch in ZERO_WIDTH_CHARS:
        text = text.replace(ch, " ")
        
    # Replace non-breaking spaces with standard spaces
    text = text.replace("\u00a0", " ")
    
    # Collapse multiple spaces while preserving single newlines
    lines = text.splitlines()
    cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in lines]
    cleaned_text = "\n".join([line for line in cleaned_lines if line])
    
    return cleaned_text

def replace_homoglyphs(text: str) -> str:
    """
    Substitutes common phishing homoglyphs for rule evaluation.
    """
    chars = []
    for char in text:
        chars.append(HOMOGLYPH_MAP.get(char, char))
    return "".join(chars)
