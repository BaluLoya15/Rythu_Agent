import re
from typing import Optional

CROP_TRANSLATIONS = {
    "Paddy": {"en": "Paddy", "te": "వరి పంట", "hi": "धान"},
    "Sugarcane": {"en": "Sugarcane", "te": "చెరకు", "hi": "गन्ना"},
    "Black Gram": {"en": "Black Gram", "te": "మినుము", "hi": "उड़द"},
    "Tomato": {"en": "Tomato", "te": "టమాటా", "hi": "टमाटर"},
    "Chilli": {"en": "Chilli", "te": "మిరప", "hi": "मिर्च"},
    "Groundnut": {"en": "Groundnut", "te": "వేరుశనగ", "hi": "मूंगफली"}
}

def generate_conversation_title(query: str, crop: Optional[str] = "Paddy", language: Optional[str] = "en") -> str:
    """
    Generates a concise title (maximum ~40 characters) from the farmer's actual message.
    Supports Telugu, Hindi, and English.
    """
    q_clean = query.strip()
    q_lower = q_clean.lower()
    norm_crop = crop or "Paddy"

    # Detect language if not explicitly provided
    is_te = bool(re.search(r'[\u0C00-\u0C7F]', q_clean)) or language == "te"
    is_hi = bool(re.search(r'[\u0900-\u097F]', q_clean)) or language == "hi"

    c_meta = CROP_TRANSLATIONS.get(norm_crop, {"en": norm_crop, "te": norm_crop, "hi": norm_crop})
    c_name = c_meta["te"] if is_te else (c_meta["hi"] if is_hi else c_meta["en"])

    # 1. Government Schemes / Services
    if any(w in q_lower for w in ["scheme", "government", "service", "subsidy", "సేవలు", "పథకం", "పథకాలు", "ప్రభుత్వ", "योजना", "सेवाएं", "सरकारी"]):
        if is_te:
            return "వ్యవసాయ పథకాలు & సేవలు"
        if is_hi:
            return "कृषि सेवाएं एवं योजनाएं"
        return "Agricultural Services & Schemes"

    # 2. Symptoms: Yellow Leaves / Pests
    if any(w in q_lower for w in ["yellow", "పసుపు", "पीला", "పీలా"]):
        if is_te:
            return f"{c_name} ఆకుల పసుపు సమస్య"[:40]
        if is_hi:
            return f"{c_name} पत्ती पीलापन समस्या"[:40]
        return f"{c_name} Yellow Leaves Advisory"[:40]

    # 3. Market / Prices
    if any(w in q_lower for w in ["market", "price", "mandi", "ధర", "మార్కెట్", "మండి", "बाजार", "मंडी", "भाव", "దర"]):
        if is_te:
            return f"{c_name} మార్కెట్ ధరలు"[:40]
        if is_hi:
            return f"{c_name} मंडी भाव"[:40]
        return f"{c_name} Market Prices"[:40]

    # 4. Weather / Rain
    if any(w in q_lower for w in ["weather", "rain", "వర్షం", "వాతావరణం", "मौसम", "बारिश"]):
        if is_te:
            return f"{c_name} వాతావరణం & వర్షం"[:40]
        if is_hi:
            return f"{c_name} मौसम एवं बारिश"[:40]
        return f"{c_name} Weather Forecast"[:40]

    # 5. Planning / Weekly Tasks / Stages
    if any(w in q_lower for w in ["plan", "week", "do", "stage", "days", "చేయాలి", "పనులు", "ప్రణాళిక", "వారపు", "సాగు", "योजना", "साप्ताहिक", "करना"]):
        if is_te:
            return f"{c_name} వారపు ప్రణాళిక"[:40]
        if is_hi:
            return f"{c_name} की साप्ताहिक योजना"[:40]
        return f"{c_name} Weekly Plan"[:40]

    # Fallback: clean snippet of query up to 38 characters
    words = q_clean.split()
    snippet = " ".join(words[:5])
    if len(snippet) > 38:
        snippet = snippet[:35] + "..."
    return snippet
