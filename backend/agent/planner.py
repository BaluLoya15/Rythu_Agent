import re
import json
from typing import Dict, Any, List, Tuple
from backend.models.schemas import TaskPlanStep

def extract_entities_from_query(query: str, default_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts crop, location, acreage, and specific problem keywords from query,
    falling back to farmer profile defaults when not explicitly mentioned.
    Supports primary crops (Paddy, Sugarcane, Black Gram) and secondary crops (Tomato, Chilli, Groundnut)
    with English, Telugu, and Hindi keyword recognition.
    """
    q_lower = query.lower()
    
    # Check for multi-crop list in farmer context
    crops_list = default_context.get("crops", [])
    if isinstance(crops_list, str):
        try:
            crops_list = json.loads(crops_list)
        except Exception:
            crops_list = [crops_list]
    if not crops_list and default_context.get("current_crop"):
        if "," in default_context["current_crop"]:
            crops_list = [c.strip() for c in default_context["current_crop"].split(",") if c.strip()]
        else:
            crops_list = [default_context["current_crop"].strip()]

    # 1. Crop extraction across English, Telugu, and Hindi with whole-word boundary matching
    crop = None
    if re.search(r'\b(?:sugarcane|cane)\b', q_lower) or any(w in q_lower for w in ["చెరకు", "చెరుకు", "गन्ना"]):
        crop = "Sugarcane"
    elif re.search(r'\b(?:black\s*gram|urad|blackgram|minumulu|minumu)\b', q_lower) or any(w in q_lower for w in ["మినుములు", "మినుము", "ఉద్ది", "उड़द", "काली उड़द"]):
        crop = "Black Gram"
    elif re.search(r'\b(?:tomato|tomatoes)\b', q_lower) or any(w in q_lower for w in ["టమాట", "టమోటా", "टमाटर"]):
        crop = "Tomato"
    elif re.search(r'\b(?:chilli|chili|mirchi|chillies)\b', q_lower) or any(w in q_lower for w in ["మిర్చి", "మిరప", "मिर्च"]):
        crop = "Chilli"
    elif re.search(r'\b(?:groundnut|groundnuts|peanut|peanuts)\b', q_lower) or any(w in q_lower for w in ["వేరుశనగ", "వేరుశెనగ", "పల్లీ", "मूंगफली"]):
        crop = "Groundnut"
    elif re.search(r'\b(?:paddy|rice)\b', q_lower) or any(w in q_lower for w in ["వరి", "వరి పంట", "ధాన్", "धान", "चावल"]):
        crop = "Paddy"

    is_multi_crop = False
    if crop is None:
        # Check if farmer has multiple registered crops and query did not pick one
        if len(crops_list) > 1:
            is_multi_crop = True
            crop = crops_list[0]  # Representative primary
        else:
            crop = default_context.get("current_crop", "Paddy")

    # 2. Location extraction
    location = default_context.get("location", "Vijayawada, Andhra Pradesh")
    for loc_candidate in ["vijayawada", "guntur", "tenali", "warangal", "kurnool", "anantapur", "anakapalle", "maruteru", "విజయవాడ", "గుంటూరు", "తేనాలి", "विजयवाड़ा", "गुंटूर"]:
        if loc_candidate in q_lower:
            location = loc_candidate.capitalize()
            break

    # 3. Land area extraction
    land_area = default_context.get("land_area", "2.0 Acres")
    match_acres = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|ఎకరాలు|ఎకరం|एकड़)', q_lower)
    if match_acres:
        land_area = f"{match_acres.group(1)} Acres"

    # 4. Crop age extraction (e.g. 40 days, 40 రోజులు, 40 दिन)
    crop_age_days = default_context.get("crop_age_days")
    match_days = re.search(r'(\d+)\s*(?:రోజులు|రోజుల|రోజు|days|day|din|दिन)', q_lower)
    if match_days:
        crop_age_days = int(match_days.group(1))

    # Stage derivation if days known
    stage = default_context.get("crop_stage")
    if crop_age_days:
        if crop == "Paddy":
            if crop_age_days <= 30:
                stage = f"Active Tillering Phase ({crop_age_days} days)"
            elif crop_age_days <= 65:
                stage = f"Panicle Initiation & Tillering ({crop_age_days} days)"
            else:
                stage = f"Booting & Grain Formation ({crop_age_days} days)"
        elif crop == "Sugarcane":
            if crop_age_days <= 60:
                stage = f"Germination & Tillering ({crop_age_days} days)"
            elif crop_age_days <= 150:
                stage = f"Grand Growth Stage ({crop_age_days} days)"
            else:
                stage = f"Maturation Phase ({crop_age_days} days)"
        elif crop == "Black Gram":
            if crop_age_days <= 25:
                stage = f"Vegetative Phase ({crop_age_days} days)"
            elif crop_age_days <= 45:
                stage = f"Flowering & Pod Setting ({crop_age_days} days)"
            else:
                stage = f"Pod Maturation ({crop_age_days} days)"

    return {
        "crop": crop,
        "is_multi_crop": is_multi_crop,
        "crops_list": crops_list,
        "location": location,
        "land_area": land_area,
        "crop_age_days": crop_age_days,
        "crop_stage": stage,
        "raw_query": query
    }

def classify_intent_and_create_plan(query: str, farmer_context: Dict[str, Any]) -> Tuple[str, str, List[TaskPlanStep]]:
    """
    Determines farmer intent and generates an explicit, multi-step task execution plan.
    Supports English, Telugu, and Hindi phrasing.
    """
    q_lower = query.lower()
    
    # Multilingual Keyword Detection
    has_market = any(w in q_lower for w in [
        "price", "market", "mandi", "sell", "selling", "rate", "cost", "gollapudi", "guntur",
        "ధర", "మార్కెట్", "మండి", "అమ్మకం",
        "बाजार", "मंडी", "दाम", "भाव", "बिक्री"
    ])
    has_scheme = any(w in q_lower for w in [
        "scheme", "government", "subsidy", "service", "services", "welfare", "pm-kisan", "pmfby", "drip subsidy", "apply", "eligibility", "criteria",
        "సేవలు", "సేవల", "సేవలను", "పథకం", "పథకాలు", "ప్రభుత్వ", "అర్హత", "దరఖాస్తు",
        "सेवाएं", "सरकारी", "योजना", "सब्सिडी", "कल्याण", "पात्रता", "आवेदन"
    ])
    has_planning = any(w in q_lower for w in [
        "plan", "cultivation", "week", "weekly", "schedule", "acres", "prepare", "activities", "what should i do",
        "వారం", "వారపు", "ప్రణాళిక", "సాగు", "కార్యాచరణ", "ఏమి చేయాలి", "ఏం చేయాలి", "పనులు",
        "योजना", "सप्ताह", "साप्ताहिक", "कृषि योजना", "तैयारी", "क्या करना चाहिए"
    ])
    has_advisory = any(w in q_lower for w in [
        "yellow", "leaves", "pest", "disease", "borer", "spray", "check", "stage",
        "పురుగు", "తెగులు", "పసుపు", "ఆకులు", "మందు",
        "रोग", "कीट", "पीला", "छिड़काव", "पत्तियां"
    ])
    has_weather = any(w in q_lower for w in [
        "weather", "forecast", "rain", "rainfall", "temperature", "humidity", "wind", "spray window",
        "వాతావరణం", "వర్షం", "వర్షపాతం", "ఎండ", "పిచికారీ సమయం", "గాలి",
        "मौसम", "पूर्वानुमान", "वर्षा", "बारिश", "तापमान", "हवा", "छिड़काव समय"
    ])
    has_documents = any(w in q_lower for w in [
        "passport", "photo", "aadhar", "aadhaar", "pan card", "bank account", "bank passbook", "passbook", "file access", "pattadar", "locker", "id card", "ifsc", "my documents", "farmer documents",
        "ఆధార్", "పాన్ కార్డు", "పాన్ కార్డ్", "బ్యాంక్ ఖాతా", "పాస్పోర్ట్", "ఫోటో", "పాస్‌బుక్", "లాకర్", "నా పత్రాలు", "నా ఫైళ్లు",
        "दस्तावेज", "आधार कार्ड", "पैन कार्ड", "बैंक खाता", "पासपोर्ट", "फोटो", "पासबुक", "लॉकर", "कागजात", "मेरे दस्तावेज"
    ])

    # Determine Intent
    if (has_market or has_planning) and (has_planning or "what should i do" in q_lower or "market price is changing" in q_lower):
        intent = "HYBRID_PLANNING_AND_MARKET"
        user_goal = "Formulate a comprehensive weekly farm action plan integrating farmer profile, crop stage, weather forecast, agronomic RAG, and market intelligence."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Load Farmer Profile & Field Context",
                tool="farmer_tool",
                goal="Retrieve registered acreage, current crop variety, stage, and irrigation constraints."
            ),
            TaskPlanStep(
                step_number=2,
                title="Check Agro-Met Weather Forecast & Spray Window",
                tool="weather_tool",
                goal="Analyze temperature, rainfall probability, and wind speed to establish safe harvest & spraying windows."
            ),
            TaskPlanStep(
                step_number=3,
                title="Retrieve Authoritative Agricultural RAG Guidance",
                tool="rag_tool",
                goal="Retrieve stage-specific nutrient management, cultural operations, and pest defense."
            ),
            TaskPlanStep(
                step_number=4,
                title="Fetch Regional Mandi Market Intelligence",
                tool="market_tool",
                goal="Compare local vs regional mandi prices, arrival trends, and net margins."
            ),
            TaskPlanStep(
                step_number=5,
                title="Reason Across Data & Formulate Farm Action Plan",
                tool="reasoning_engine",
                goal="Synthesize weather safety, research knowledge, and market dynamics into prioritized action cards."
            )
        ]

    elif has_scheme:
        intent = "SERVICES_AND_GOVERNMENT_SCHEMES"
        user_goal = "Identify applicable government services, subsidies, eligibility rules, and application documents."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Inspect Farmer Profile for Eligibility Factors",
                tool="farmer_tool",
                goal="Assess landholding scale (small/marginal), existing scheme enrollments, and district jurisdiction."
            ),
            TaskPlanStep(
                step_number=2,
                title="Query Curated Agricultural Schemes Knowledge Base",
                tool="services_tool",
                goal="Search Central & Andhra Pradesh state schemes (PM-KISAN, PMFBY Free Crop Insurance, PMKSY Drip Subsidy, SMAM Mechanization)."
            ),
            TaskPlanStep(
                step_number=3,
                title="Synthesize Eligibility & Application Requirements",
                tool="reasoning_engine",
                goal="Structure criteria, required verification documents, official portal links, and clear non-guaranteed disclaimers."
            )
        ]

    elif has_documents and not has_planning:
        intent = "FARMER_DOCUMENTS_AND_FILES"
        user_goal = "Access farmer digital locker, retrieve identity credentials (Aadhaar, PAN, Bank Passbook, Passport Photo), and check document verification readiness."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Load Farmer Digital Locker & Credentials",
                tool="farmer_tool",
                goal="Retrieve farmer identification files, Aadhaar number, PAN, bank passbook, and land ownership records."
            ),
            TaskPlanStep(
                step_number=2,
                title="Verify Scheme & Subsidy Readiness",
                tool="services_tool",
                goal="Cross-check available credentials against mandatory government scheme requirements (PM-KISAN, PMFBY, KCC)."
            ),
            TaskPlanStep(
                step_number=3,
                title="Synthesize File Access & Digital Locker Report",
                tool="reasoning_engine",
                goal="Provide direct file access, status overview, masked credentials, and actionable next steps."
            )
        ]

    elif has_weather and not has_market and not has_planning:
        intent = "WEATHER_FORECAST"
        user_goal = "Analyze live agro-meteorological satellite data, precipitation forecast, wind velocity, and spray window suitability."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Load Farmer Location & Crop Details",
                tool="farmer_tool",
                goal="Confirm farmer location, district, and current crop growth stage."
            ),
            TaskPlanStep(
                step_number=2,
                title="Retrieve Live Agro-Met Satellite Feed",
                tool="weather_tool",
                goal="Fetch real-time Open-Meteo satellite feed: temperature, rainfall probability, relative humidity, and wind speed."
            ),
            TaskPlanStep(
                step_number=3,
                title="Verify Agronomic Implications & Spray Safety",
                tool="rag_tool",
                goal="Cross-reference weather conditions against university extension thresholds for foliar application and irrigation."
            ),
            TaskPlanStep(
                step_number=4,
                title="Synthesize Weather Advisory & Irrigation Guidance",
                tool="reasoning_engine",
                goal="Structure temperature metrics, 3-day precipitation risks, optimal spray window, and actionable farm guidance."
            )
        ]

    elif has_market:
        intent = "MARKET_INTELLIGENCE"
        user_goal = "Analyze current mandi prices, compare regional wholesale yards, and evaluate transportation economics."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Load Farmer Location & Crop Details",
                tool="farmer_tool",
                goal="Identify target crop and transit hub proximity."
            ),
            TaskPlanStep(
                step_number=2,
                title="Retrieve Multi-Market Mandi Data",
                tool="market_tool",
                goal="Fetch modal prices, arrivals, price trends, and calculate net effective realization after transport."
            ),
            TaskPlanStep(
                step_number=3,
                title="Formulate Market Decision Support",
                tool="reasoning_engine",
                goal="Produce strategic selling recommendations, grading tips, and mandi comparison tables."
            )
        ]

    else:
        # Default to Crop Advisory / Stage Management
        intent = "CROP_ADVISORY"
        user_goal = "Diagnose crop symptoms, provide grounded package-of-practices, and recommend safe cultural practices."
        plan = [
            TaskPlanStep(
                step_number=1,
                title="Load Crop Profile & Field Parameters",
                tool="farmer_tool",
                goal="Confirm crop type, current growth stage, and soil/irrigation baseline."
            ),
            TaskPlanStep(
                step_number=2,
                title="Retrieve Sourced Extension Research Documents",
                tool="rag_tool",
                goal="Perform semantic RAG search across ANGRAU/ICAR manuals for symptom diagnosis and cultural practices."
            ),
            TaskPlanStep(
                step_number=3,
                title="Check Agro-Met Advisory Conditions",
                tool="weather_tool",
                goal="Verify current humidity and rain conditions affecting disease spread and spray timing."
            ),
            TaskPlanStep(
                step_number=4,
                title="Synthesize Grounded Advisory & Safety Notes",
                tool="reasoning_engine",
                goal="Generate step-by-step diagnostic checklist, bio-rational remedies, and authoritative citations."
            )
        ]

    return intent, user_goal, plan
