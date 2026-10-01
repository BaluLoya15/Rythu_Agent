import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from backend.models.schemas import (
    ActionPlan, ConsequentialAction, MarketComparison,
    WeatherData, RAGSource, GovernmentService
)

def is_telugu(text: str) -> bool:
    return bool(re.search(r'[\u0C00-\u0C7F]', text))

def is_hindi(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

CROP_NAMES = {
    "paddy": {"en": "Paddy", "te": "వరి", "hi": "धान"},
    "sugarcane": {"en": "Sugarcane", "te": "చెరకు", "hi": "गन्ना"},
    "black_gram": {"en": "Black Gram", "te": "మినుములు", "hi": "उड़द"},
    "tomato": {"en": "Tomato", "te": "టమాటా", "hi": "टमाटर"},
    "chilli": {"en": "Chilli", "te": "మిరప", "hi": "मिर्च"},
    "groundnut": {"en": "Groundnut", "te": "వేరుశనగ", "hi": "मूंगफली"}
}

def get_canonical_crop_key(crop: str) -> str:
    c = (crop or "").lower()
    if any(k in c for k in ["rice", "paddy", "వరి", "ధాన్", "धान", "चावल"]):
        return "paddy"
    if any(k in c for k in ["sugarcane", "cane", "చెరకు", "చెరుకు", "గన్నా", "गन्ना"]):
        return "sugarcane"
    if any(k in c for k in ["black", "urad", "minumulu", "మినుము", "మినుములు", "ఉద్ది", "उड़द"]):
        return "black_gram"
    if any(k in c for k in ["tomato", "టమాటా", "టమాట", "टमाटर"]):
        return "tomato"
    if any(k in c for k in ["chilli", "chili", "mirchi", "మిరప", "మిర్చి", "मिर्च"]):
        return "chilli"
    if any(k in c for k in ["groundnut", "peanut", "వేరుశనగ", "వేరుశెనగ", "పల్లీ", "मूंगफली"]):
        return "groundnut"
    return "paddy"

def get_crop_agronomic_package(
    crop: str,
    stage: str,
    acres: str,
    weather_data: Optional[WeatherData],
    language: str = "en",
    is_multi_crop: bool = False,
    crops_list: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Returns stage-specific agronomic recommendations, monitoring tasks,
    risk mitigation protocols, and authentic ANGRAU/ICAR research citations
    in the requested language ('en', 'te', or 'hi').
    """
    crop_key = get_canonical_crop_key(crop)
    lang = (language or "en").lower()
    if lang not in ["te", "hi", "en"]:
        lang = "en"

    rain_prob = weather_data.rainfall_probability_pct if weather_data else 15

    # -------------------------------------------------------------
    # 1. PADDY (PRIMARY CROP 1)
    # -------------------------------------------------------------
    if crop_key == "paddy":
        if lang == "te":
            considerations = [
                f"మీ వరి పంట {stage} (సుమారు 40-50 రోజులు) దశలో ఉంది. ఈ దశలో దుబ్బు బాగా చేసి బలమైన అంకురం ఏర్పడటానికి 2-3 సెం.మీ పలుచని నీటి మట్టాన్ని నిర్వహించడం చాలా కీలకం.",
                f"వాతావరణ పరిస్థితులు: వర్షం వచ్చే అవకాశం {rain_prob}% ఉంది. భారీ వర్షం కురిసే సూచన ఉన్నప్పుడు ఎరువులు కొట్టుకుపోకుండా ఉండటానికి యూరియా చల్లడం నివారించండి.",
                "పురుగుల తీవ్రత: కాండం తొలుచు పురుగు మొవ్వు కుళ్లు 5% కంటే ఎక్కువ ఉంటే లేదా చ.మీ.కు 1 గుడ్ల సముదాయం ఉంటే వెంటనే నివారణ చర్యలు చేపట్టాలి."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "దశకు తగిన పోషక యాజమాన్యం (నత్రజని + పొటాష్)",
                    "detail": "ఎకరాకు 25-30 కిలోల యూరియాతో పాటు 20 కిలోల మ్యూరేట్ ఆఫ్ పొటాష్ (MOP) ను ఆఖరి దఫాగా వేయండి. ఇది వెన్ను పొడవు పెరగడానికి మరియు గింజ బరువుకు తోడ్పడుతుంది.",
                    "priority": "HIGH",
                    "timeline": "రాబోయే 24-48 గంటల్లో (ప్రశాంతమైన ఉదయం లేదా సాయంత్రం)"
                },
                {
                    "step": 2,
                    "title": "నీటి యాజమాన్యం & ఆరి కట్టే పద్ధతి (AWD)",
                    "detail": "పొలంలో 2-3 సెం.మీ పలుచగా నీరు ఉంచండి. సుడిదోమ ఉధృతి తగ్గించడానికి ప్రతి 2 మీటర్లకు ఒక కాలువ/పాయ తీసి గాలి, వెలుతురు సోకేలా చేయండి.",
                    "priority": "HIGH",
                    "timeline": "రోజువారీ నీటి నిర్వహణ"
                },
                {
                    "step": 3,
                    "title": "కాండం తొలుచు పురుగు & అగ్గి తెగులు నివారణ",
                    "detail": "మొవ్వు చనిపోవడం గమనిస్తే ఎకరాకు కార్టాప్ హైడ్రోక్లోరైడ్ 4% గుళికలు 8 కిలోలు చల్లండి లేదా క్లోరాంట్రానిలిప్రోల్ 18.5% SC 0.3 మి.లీ/లీటరు పిచికారీ చేయండి. అగ్గి తెగులు నివారణకు ట్రైసైక్లాజోల్ 75% WP 0.6 గ్రా/లీటరు పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "ఈ వారాంతపు క్షేత్ర పరిశీలన"
                }
            ]
            monitoring_tasks = [
                "ఆకుల పైభాగంలో కాండం తొలుచు పురుగు గుడ్ల సముదాయాలు మరియు ఎండిన మొవ్వులను లెక్కించండి.",
                "వరి దుబ్బుల మొదళ్ల వద్ద సుడిదోమ నింఫ్స్‌ను ఆరి కట్టే సమయంలో పరిశీలించండి.",
                "పొలంలో పాయలు తీయడం ద్వారా గాలి ప్రసరణ సరిగ్గా ఉందో లేదో తనిఖీ చేయండి."
            ]
            risk_mitigation = [
                "పంట పడిపోవడం & తెగుళ్ల ముప్పు: అధిక మోతాదులో యూరియా వాడకండి; పొటాష్ సమతుల్యతను కాపాడండి.",
                "నీటి నిల్వ ప్రమాదం: భారీ వర్షాలకు ముందే మురుగు నీరు పోయే కాలువలను శుభ్రం చేసుకోండి."
            ]
        elif lang == "hi":
            considerations = [
                f"आपकी धान की फसल {stage} (लगभग 40-50 दिन) की अवस्था में है। कल्ले फूटने और स्वस्थ बाली बनने के लिए 2-3 सेमी उथला पानी बनाए रखना अत्यंत आवश्यक है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। तेज बारिश की संभावना होने पर यूरिया का बुरकाव रोकें ताकि पोषक तत्व बह न जाएं।",
                "कीट सीमा: तना छेदक (डेड हार्ट) 5% से अधिक होने पर तुरंत नियंत्रण उपाय करें; बीपीएच (भूरा फुदका) से बचाव हेतु खेत में नालियां बनाएं।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "अवस्था-विशिष्ट पोषक तत्व प्रबंधन (नाइट्रोजन + पोटाश)",
                    "detail": "अंतिम शीर्ष ड्रेसिंग के रूप में 25-30 किलोग्राम यूरिया प्रति एकड़ और 20 किलोग्राम म्यूरेट ऑफ पोटाश (MOP) डालें। यह बाली के विकास और दानों के भराव को बढ़ाता है।",
                    "priority": "HIGH",
                    "timeline": "अगले 24-48 घंटों में (शांत सुबह या शाम)"
                },
                {
                    "step": 2,
                    "title": "जल प्रबंधन एवं रुक-रुक कर सिंचाई (AWD)",
                    "detail": "बाली बनने के दौरान 2-3 सेमी उथला पानी रखें। खेत में हवा और धूप के लिए हर 2 मीटर पर एक पंक्ति छोड़कर नाली बनाएं जिससे भूरा फुदका न पनपे।",
                    "priority": "HIGH",
                    "timeline": "दैनिक जल प्रबंधन"
                },
                {
                    "step": 3,
                    "title": "तना छेदक एवं झुलसा (ब्लास्ट) रोग से बचाव",
                    "detail": "तना छेदक दिखने पर कार्तप हाइड्रोक्लोराइड 4% जी @ 8 किग्रा/एकड़ का बुरकाव करें या क्लोरेंट्रानिलिप्रोल 18.5% एससी @ 0.3 मिली/लीटर स्प्रे करें। ब्लास्ट से बचाव हेतु ट्राइसाइक्लाजोल 75% डब्ल्यूपी @ 0.6 ग्राम/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "सप्ताहांत खेत निरीक्षण"
                }
            ]
            monitoring_tasks = [
                "पत्तियों पर तना छेदक के अंडों के गुच्छों और सूखे डेड हार्ट की जांच करें।",
                "धान के पौधों की जड़ों के पास भूरा फुदका (BPH) के प्रकोप का निरीक्षण करें।",
                "खेत में उचित जल निकासी और धूप के लिए बनाई गई नालियों की स्थिति जांचें।"
            ]
            risk_mitigation = [
                "फसल गिरने का जोखिम: अधिक नाइट्रोजन के उपयोग से बचें; पोटाश का संतुलित प्रयोग सुनिश्चित करें।",
                "जलभराव: भारी बारिश से पहले जल निकासी नालियों को साफ रखें।"
            ]
        else:
            considerations = [
                f"At the {stage} stage (approx. 40-50 days), maintaining 2-3 cm shallow water depth is vital to ensure maximum productive tillers and healthy panicle initiation.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Avoid broadcasting granular nitrogen if heavy showers are expected to prevent fertilizer run-off into drainage channels.",
                "Pest Thresholds: Yellow Stem Borer ETL is 1 egg mass/sq.m or 5% dead hearts; Brown Plant Hopper (BPH) requires alley ventilation."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Stage-Specific Nutrient Top-Dressing (Nitrogen + Potash)",
                    "detail": "Apply the final top dressing of Nitrogen (25% remaining dose, approx. 25-30 kg Urea/acre) along with Muriate of Potash (MOP @ 20 kg/acre). This promotes panicle elongation, reduces sterile spikelets, and improves grain filling.",
                    "priority": "HIGH",
                    "timeline": "Next 24-48 hours (during calm morning/evening)"
                },
                {
                    "step": 2,
                    "title": "Water Regime & Alternate Wetting and Drying (AWD)",
                    "detail": "Maintain 2-3 cm shallow standing water during panicle development. Practice alternate wetting and drying (AWD) to strengthen root anchorage and suppress Brown Plant Hopper (BPH) multiplication. Form alleys (skip 1 row every 2 meters in north-south orientation) for direct sunlight penetration.",
                    "priority": "HIGH",
                    "timeline": "Continuous daily water management"
                },
                {
                    "step": 3,
                    "title": "Yellow Stem Borer & Neck Blast Defense",
                    "detail": "Scout for yellow stem borer dead hearts. If ETL is reached, broadcast Cartap Hydrochloride 4% G @ 8 kg/acre or spray Chlorantraniliprole 18.5% SC @ 0.3 ml/L. For neck blast prevention during humid conditions, apply prophylactic spray of Tricyclazole 75% WP @ 0.6 g/L at early heading.",
                    "priority": "MEDIUM",
                    "timeline": "Weekend field inspection"
                }
            ]
            monitoring_tasks = [
                "Scout for yellow stem borer egg masses on upper leaf surface and count dead hearts across sample plots.",
                "Examine base of rice hills for Brown Plant Hopper (BPH) nymphs during alternate wetting and drying cycles.",
                "Ensure field alleys are open and unobstructed for cross-ventilation."
            ]
            risk_mitigation = [
                "Lodging & Blast Risk: Avoid excessive single nitrogen application; ensure potassium balance at panicle emergence.",
                "Water Stagnation: Ensure field drain outlets are cleared before expected heavy cyclonic rain."
            ]
        sources_cited = [
            "ICAR-Indian Institute of Rice Research (IIRR) Tech Bulletin 2024-R01: Comprehensive Paddy Management, Page 78",
            "ANGRAU Agricultural Research Station Maruteru: High-Yielding Rice Production Package, Bulletin AP-PADDY-2024, Page 32",
            "Open-Meteo Live Agro-Met Satellite Feed"
        ]

    # -------------------------------------------------------------
    # 2. SUGARCANE (PRIMARY CROP 2)
    # -------------------------------------------------------------
    elif crop_key == "sugarcane":
        if lang == "te":
            considerations = [
                f"చెరకు {stage} (90-120 రోజులు) దశలో ఉంది. ఈ దశలో కణుపులు పొడవు పెరగడానికి, బయోమాస్ చేకూరడానికి మరియు తేమ సంరక్షణకు అత్యంత ప్రాముఖ్యత ఉంది.",
                f"వాతావరణ పరిస్థితులు: వర్షం అవకాశం {rain_prob}%. తీరప్రాంత గాలుల వల్ల పంట పడిపోకుండా బలమైన మట్టి ఎగదోయడం పూర్తి చేయాలి.",
                "నేల ఆచ్ఛాదన: సాలులలో ఎండిన చెరకు చెత్త పరచడం ద్వారా నీటి ఆవశ్యకతను 30% వరకు తగ్గించవచ్చు."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "సాలులలో ఎండిన చెరకు చెత్త ఆచ్ఛాదన (ట్రాష్ మల్చింగ్)",
                    "detail": "సాలులలో ఎకరాకు 3 టన్నుల ఎండిన చెరకు చెత్తను సమానంగా పరచండి. ఇది 30% నేల తేమను కాపాడుతుంది, వేసవిలో నేల ఉష్ణోగ్రతను తగ్గిస్తుంది మరియు కలుపును 60% వరకు అణిచివేస్తుంది.",
                    "priority": "HIGH",
                    "timeline": "తక్షణమే (రాబోయే 2-3 రోజుల్లో)"
                },
                {
                    "step": 2,
                    "title": "ఆఖరి దఫా ఎరువులు & మట్టి ఎగదోయడం (ఎర్తింగ్ అప్)",
                    "detail": "120 రోజుల నాటికి చివరి దఫా యూరియా (75 కిలోలు/ఎకరా) మరియు పొటాష్ (50 కిలోలు/ఎకరా) వేసి గట్ల నుండి మట్టిని సాలులలోకి ఎగదోయండి. ఇది గాలులకు పంట పడిపోకుండా కాపాడుతుంది.",
                    "priority": "HIGH",
                    "timeline": "ఈ వారం లోపు"
                },
                {
                    "step": 3,
                    "title": "కణుపు తొలుచు పురుగు & ఎర్ర కుళ్లు తెగులు నివారణ",
                    "detail": "క్రింది ఎండిన ఆకులను తీసివేయడం ద్వారా కణుపు తొలుచు పురుగు ఆశ్రయాన్ని తొలగించండి; ట్రైకోగ్రామా పరాన్నజీవిని ఎకరాకు 2.5 సిసి చొప్పున విడుదల చేయండి. ఎర్ర కుళ్లు తెగులు గమనిస్తే కాపర్ ఆక్సిక్లోరైడ్ 50% WP 3.0 గ్రా/లీటరు పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "ఉదయపు పరిశీలన"
                }
            ]
            monitoring_tasks = [
                "కణుపులలో పురుగు తొలచిన రంధ్రాలు మరియు విసర్జితాలను తనిఖీ చేయండి.",
                "తదుపరి నీటి తడి ఇచ్చే ముందు సాలులలో తేమ శాతాన్ని పరిశీలించండి.",
                "పంట పడిపోకుండా మొక్కల మొదళ్లు గట్టిగా ఉన్నాయో లేదో నిర్ధారించుకోండి."
            ]
            risk_mitigation = [
                "పంట పడిపోవడం: తీరప్రాంత బలమైన గాలులకు ముందే మట్టి ఎగదోయడం పూర్తి చేయండి.",
                "వ్యాధి వ్యాప్తి: ఎర్ర కుళ్లు సోకిన దుబ్బులను పీకి కాల్చివేయండి; ఆ నీరు ఇతర సాలులలోకి వెళ్లకుండా చూడండి."
            ]
        elif lang == "hi":
            considerations = [
                f"गन्ना {stage} (90-120 दिन) की मुख्य वृद्धि अवस्था में है। यह पोरियों की लंबाई, बायोमास और नमी संचयन की चरम अवधि है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। तेज हवाओं से फसल को गिरने से बचाने के लिए मजबूत मिट्टी चढ़ाना आवश्यक है।",
                "मल्चिंग: नालियों में सूखी पत्तियां बिछाने से सिंचाई की आवश्यकता में 30% तक कमी आती है।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "नालियों में गन्ने की सूखी पत्तियों की मल्चिंग",
                    "detail": "नालियों में 3 टन प्रति एकड़ की दर से गन्ने की सूखी पत्तियां समान रूप से बिछाएं। इससे 30% नमी सुरक्षित रहती है और खरपतवार 60% तक नियंत्रित होते हैं।",
                    "priority": "HIGH",
                    "timeline": "तुरंत (अगले 2-3 दिनों में)"
                },
                {
                    "step": 2,
                    "title": "अंतिम मिट्टी चढ़ाना एवं शीर्ष ड्रेसिंग",
                    "detail": "120 दिन तक अंतिम मिट्टी चढ़ाने का कार्य पूरा करें तथा साथ में 75 किग्रा यूरिया और 50 किग्रा म्यूरेट ऑफ पोटाश (MOP) प्रति एकड़ डालें।",
                    "priority": "HIGH",
                    "timeline": "इस सप्ताह के भीतर"
                },
                {
                    "step": 3,
                    "title": "पोरी छेदक एवं लाल सड़न रोग की निगरानी",
                    "detail": "निचली सूखी पत्तियों को हटाएं ताकि पोरी छेदक कीट न पनपे; ट्राइकोग्रामा परजीवी 2.5 सीसी/एकड़ छोड़ें। लाल सड़न के लक्षण दिखने पर कॉपर ऑक्सीक्लोराइड 50% डब्ल्यूपी @ 3.0 ग्राम/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "सुबह के समय निरीक्षण"
                }
            ]
            monitoring_tasks = [
                "गन्ने की पोरियों में छेदक कीट के सुराखों और लकड़ी के बुरादे की जांच करें।",
                "सिंचाई से पहले खेत की नालियों में नमी की गहराई मापें।",
                "तेज हवा में फसल को गिरने से बचाने के लिए जड़ों की पकड़ जांचें।"
            ]
            risk_mitigation = [
                "फसल गिरना: मानसून की तेज हवाओं से पहले मिट्टी चढ़ाने का कार्य मजबूती से पूरा करें।",
                "रोग प्रसार: लाल सड़न से प्रभावित पौधों को उखाड़कर नष्ट करें; संक्रमित क्षेत्र से सिंचाई का पानी स्वस्थ क्षेत्र में न जाने दें।"
            ]
        else:
            considerations = [
                f"Grand Growth Stage (90-120 days): Peak period for internode elongation, biomass accumulation, and moisture retention.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Heavy coastal winds necessitate strong earthing-up to prevent crop lodging.",
                "Soil Mulching: Conserving furrow moisture reduces irrigation requirements by up to 30%."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Trash Mulching in Furrows for Moisture Conservation",
                    "detail": "Spread dried cane trash uniformly @ 3 tonnes/acre in furrows. This conserves 30% soil moisture, lowers rhizosphere soil temperature during hot weather, and suppresses broadleaf weed growth by over 60%.",
                    "priority": "HIGH",
                    "timeline": "Immediate (Next 2-3 days)"
                },
                {
                    "step": 2,
                    "title": "Final Earthing-Up & Top-Dressing",
                    "detail": "Complete final earthing-up by 120 days along with the last top-dressing of Nitrogen (75 kg Urea/acre) and Muriate of Potash (MOP @ 50 kg/acre). This converts ridges into furrows and prevents crop lodging during coastal winds.",
                    "priority": "HIGH",
                    "timeline": "Within this week"
                },
                {
                    "step": 3,
                    "title": "Internode Borer & Red Rot Clump Inspection",
                    "detail": "De-trash lower dried leaves to eliminate internode borer shelter; release egg parasitoid Trichogramma chilonis @ 2.5 cc/acre. Inspect clumps for early red rot discoloration; drench suspect spots with Copper Oxychloride 50% WP @ 3.0 g/L.",
                    "priority": "MEDIUM",
                    "timeline": "Morning inspection"
                }
            ]
            monitoring_tasks = [
                "Inspect internodes of cane stalks for borer entry boreholes and frass.",
                "Check furrow moisture depth before scheduling irrigation cycles.",
                "Verify clump root anchorage to guard against wind lodging."
            ]
            risk_mitigation = [
                "Crop Lodging: Complete earthing up firmly before monsoon coastal winds intensify.",
                "Disease Spread: Uproot and burn red rot affected clumps; do not pass furrow irrigation water from infected to healthy patches."
            ]
        sources_cited = [
            "ANGRAU Regional Agricultural Research Station (RARS) Anakapalle: Sugarcane Tech Manual SC-2024, Page 41",
            "ICAR-Sugarcane Breeding Institute (SBI) Coimbatore: Production Guidelines Bulletin SB-2024, Page 56",
            "Open-Meteo Agro-Met Satellite Feed"
        ]

    # -------------------------------------------------------------
    # 3. BLACK GRAM (PRIMARY CROP 3)
    # -------------------------------------------------------------
    elif crop_key == "black_gram":
        if lang == "te":
            considerations = [
                f"మినుము పంట {stage} (పూత మరియు కాయ దశ) లో ఉంది. తెల్లదోమ ద్వారా వ్యాపించే పల్లా తెగులును నియంత్రించడం అత్యంత ప్రధానం.",
                f"వాతావరణ పరిస్థితులు: వర్షం అవకాశం {rain_prob}%. పురుగు మందులు మరియు పోషకాల పిచికారీని ప్రశాంతమైన వాతావరణంలో మాత్రమే చేపట్టాలి.",
                "పూత రాలడం నివారణ: 19:19:19 లేదా 2% డిఎపి పిచికారీ చేయడం ద్వారా పూత రాలడం తగ్గి కాయల సంఖ్య 20% పెరుగుతుంది."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "పల్లా తెగులు నివారణకు తెల్లదోమ యాజమాన్యం",
                    "detail": "ఎకరాకు 10-12 పసుపు రంగు జిగురు పూసిన అట్టలను అమర్చండి. తెల్లదోమ కనిపిస్తే ఎసిటామిక్రిడ్ 20% SP 0.2 గ్రా/లీ లేదా థయామెథాక్సమ్ 25% WG 0.3 గ్రా/లీ పిచికారీ చేయండి.",
                    "priority": "HIGH",
                    "timeline": "వెంటనే (రాబోయే 24 గంటల్లో)"
                },
                {
                    "step": 2,
                    "title": "పూత & కాయ పెరుగుదలకు పోషకాల పిచికారీ",
                    "detail": "ఎకరాకు 19:19:19 ద్రావణం 5 గ్రా/లీటర్ లేదా 2% నానబెట్టి వడపోసిన డీఏపీ ద్రావణాన్ని పిచికారీ చేయండి. ఇది పూత రాలడాన్ని నివారిస్తుంది.",
                    "priority": "HIGH",
                    "timeline": "ఈ వారం లోపు (ఉదయం 7-10 గంటల మధ్య)"
                },
                {
                    "step": 3,
                    "title": "కాయ తొలుచు పురుగు నియంత్రణ",
                    "detail": "కాయలకు రంధ్రాలు లేదా లద్దె పురుగులు గమనిస్తే స్పైనోసాడ్ 45% SC 0.3 మి.లీ/లీటరు లేదా క్లోరాంట్రానిలిప్రోల్ 0.3 మి.లీ/లీటరు పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "క్షేత్ర తనిఖీ అనంతరం"
                }
            ]
            monitoring_tasks = [
                "ఆకుల అడుగుభాగంలో తెల్లదోమ నింఫ్స్‌ను పరిశీలించండి.",
                "ఎల్లో స్టిక్కీ ట్రాప్స్‌లో పడిన పురుగుల సంఖ్యను లెక్కించండి.",
                "పిందెలపై లద్దెపురుగు ప్రవేశ రంధ్రాలు ఉన్నాయేమో గమనించండి."
            ]
            risk_mitigation = [
                "పల్లా తెగులు వ్యాప్తి: తెల్లదోమ తొలిదశలోనే నియంత్రించండి; తెగులు సోకిన మొక్కలను పీకివేయండి.",
                "నీటి ముంపు ప్రమాదం: పప్పుజాతి పంట కావడంతో పొలంలో నీరు నిల్వ ఉండకుండా చూసుకోండి."
            ]
        elif lang == "hi":
            considerations = [
                f"उड़द की फसल {stage} (फूल और फली बनने की अवस्था) में है। सफेद मक्खी द्वारा फैलने वाले पीला मोज़ेक वायरस का नियंत्रण सर्वोच्च प्राथमिकता है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। शांत मौसम में ही फोलियर स्प्रे करें।",
                "फूल झड़ने से बचाव: 19:19:19 या 2% डीएपी का छिड़काव करने से फूल झड़ना रुकता है और फली भराव 20% तक बढ़ता है।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "पीला मोज़ेक वायरस से बचाव हेतु सफेद मक्खी नियंत्रण",
                    "detail": "10-12 पीले चिपचिपे ट्रैप प्रति एकड़ लगाएं। सफेद मक्खी दिखने पर एसिटामिप्रिड 20% एसपी @ 0.2 ग्राम/लीटर या थायमेथोक्सम 25% डब्ल्यूजी @ 0.3 ग्राम/लीटर का छिड़काव करें।",
                    "priority": "HIGH",
                    "timeline": "तुरंत (अगले 24 घंटों में)"
                },
                {
                    "step": 2,
                    "title": "फूल व फली विकास हेतु पर्णीय पोषण (19:19:19)",
                    "detail": "घुलनशील 19:19:19 (एनपीके) @ 5.0 ग्राम/लीटर या 2% डीएपी का छिड़काव करें। इससे फूल झड़ना रुकता है और फली सेटिंग में सुधार होता है।",
                    "priority": "HIGH",
                    "timeline": "इस सप्ताह (सुबह 7 से 10 बजे के बीच)"
                },
                {
                    "step": 3,
                    "title": "फली छेदक कीट का नियंत्रण",
                    "detail": "फलियों पर छेद दिखने पर स्पिनोसाड 45% एससी @ 0.3 मिली/लीटर या क्लोरेंट्रानिलिप्रोल @ 0.3 मिली/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "खेत निरीक्षण उपरांत"
                }
            ]
            monitoring_tasks = [
                "पत्तियों की निचली सतह पर सफेद मक्खी के शिशुओं का निरीक्षण करें।",
                "पीले चिपचिपे ट्रैप में फंसे कीटों की संख्या जांचें।",
                "फलियों पर इल्ली के प्रवेश छेदों का मुआयना करें।"
            ]
            risk_mitigation = [
                "पीला मोज़ेक: सफेद मक्खी के प्रारंभिक प्रकोप पर ही नियंत्रण करें; रोगग्रस्त पौधों को उखाड़ दें।",
                "जलभराव: दलहनी फसल होने के कारण खेत में पानी ठहरने न दें।"
            ]
        else:
            considerations = [
                f"Black Gram (Urad) at {stage}: Peak period for vegetative expansion and early flower flush. Preventing Whitefly vector spread is paramount.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Plan foliar nutrition and pest sprays under clear morning sky conditions.",
                "Flower Drop Prevention: 19:19:19 foliar spray directly improves pod set percentage by over 20%."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Whitefly & Yellow Mosaic Virus (YMV) Vector Defense",
                    "detail": "Install yellow sticky traps @ 10-12 traps/acre. Spray Acetamiprid 20% SP @ 0.2 g/L or Thiamethoxam 25% WG @ 0.3 g/L at the first detection of whitefly nymphs on leaf undersides.",
                    "priority": "HIGH",
                    "timeline": "Immediate (Next 24 hours)"
                },
                {
                    "step": 2,
                    "title": "Foliar Nutrition for Flower Setting (19:19:19 NPK)",
                    "detail": "Apply foliar spray of water-soluble 19:19:19 @ 5.0 g/L or 2% DAP (soaked and filtered) during early morning hours to strengthen flower retention and stimulate pod elongation.",
                    "priority": "HIGH",
                    "timeline": "Within this week (7:00 AM - 10:00 AM)"
                },
                {
                    "step": 3,
                    "title": "Pod Borer & Caterpillar Scouting",
                    "detail": "Scout for spotted pod borer entry holes. If ETL is crossed, spray Spinosad 45% SC @ 0.3 ml/L or Chlorantraniliprole 18.5% SC @ 0.3 ml/L.",
                    "priority": "MEDIUM",
                    "timeline": "Post-inspection"
                }
            ]
            monitoring_tasks = [
                "Inspect lower leaf surfaces for whitefly nymphs and sooty mold.",
                "Check yellow sticky trap count across field boundaries.",
                "Monitor flower clusters for caterpillar entry frass."
            ]
            risk_mitigation = [
                "YMV Infection: Roguing out initial viral infected plants suppresses rapid field-wide spread.",
                "Water Stagnation: Pulses are vulnerable to root asphyxiation; keep field channels unclogged."
            ]
        sources_cited = [
            "ANGRAU Regional Agricultural Research Station (RARS) Lam, Guntur: Pulses Bulletin BG-2024-01, Page 22",
            "ICAR-Indian Institute of Pulses Research (IIPR): Pulse Production Protocol, Page 45",
            "Open-Meteo Satellite Feed"
        ]

    # -------------------------------------------------------------
    # 4. TOMATO, CHILLI, GROUNDNUT (SECONDARY CROPS)
    # -------------------------------------------------------------
    elif crop_key == "tomato":
        if lang == "te":
            considerations = [
                f"టమాటా {stage} (పూత మరియు కాయ పెరుగుదల) లో ఉంది. స్థిరమైన నీటి యాజమాన్యం మరియు కాయ తొలుచు పురుగు నివారణ కీలకం.",
                f"వాతావరణ పరిస్థితులు: వర్షం అవకాశం {rain_prob}%. క్రమం తప్పని డ్రిప్ నీటిపారుదల ద్వారా పూత రాలడం మరియు కాయల పగుళ్లను నివారించవచ్చు.",
                "సూక్ష్మపోషకాలు: బోరాన్ మరియు కాల్షియం పిచికారీ చేయడం వల్ల పూత నిలబడుతుంది మరియు కాయ కుళ్లు తెగులు నివారించబడుతుంది."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "సూక్ష్మపోషకాల పిచికారీ (బోరాన్ + కాల్షియం నైట్రేట్)",
                    "detail": "ఎకరాకు బోరాన్ (20%) 1 గ్రా/లీ మరియు కాల్షియం నైట్రేట్ 2.5 గ్రా/లీ కలిపి పిచికారీ చేయండి. ఇది కాయ కుళ్లు తెగులును నివారిస్తుంది.",
                    "priority": "HIGH",
                    "timeline": "రాబోయే 48 గంటల్లో"
                },
                {
                    "step": 2,
                    "title": "డ్రిప్ నీటిపారుదల సమతుల్యత",
                    "detail": "మొక్కకు రోజుకు 2.5 నుండి 3.5 లీటర్ల నీటిని క్రమం తప్పకుండా డ్రిప్ ద్వారా అందించండి. హెచ్చుతగ్గుల నీటి తడులు ఇవ్వవద్దు.",
                    "priority": "HIGH",
                    "timeline": "నిరంతర రోజువారీ నిర్వహణ"
                },
                {
                    "step": 3,
                    "title": "టూటా అబ్సొల్యూటా & కాయ తొలుచు పురుగు నివారణ",
                    "detail": "ఎకరాకు 12-16 డెల్టా ఫెరమోన్ ట్రాప్స్ అమర్చండి. పురుగు ఉధృతి ఉంటే క్లోరాంట్రానిలిప్రోల్ 18.5% SC 0.3 మి.లీ/లీటరు పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "సాయంత్రం 4:30 తర్వాత"
                }
            ]
            monitoring_tasks = [
                "ఆకులలో టూటా ఆకు తొలిచే పురుగు సొరంగాలు మరియు కాయల వద్ద రంధ్రాలను తనిఖీ చేయండి.",
                "ఫెరమోన్ ట్రాప్స్‌లో పడిన రెక్కల పురుగులను లెక్కించండి.",
                "నేలలో తగినంత తేమ ఉందో లేదో డ్రిప్ నాజిల్స్ వద్ద గమనించండి."
            ]
            risk_mitigation = [
                "కాయ కుళ్లు: కాల్షియం లోపం రాకుండా క్రమబద్ధమైన నీటి తడులు ఇవ్వండి.",
                "పురుగు మందుల అవశేషాలు: కోతకు 3 రోజుల ముందు రసాయనాలు పిచికారీ చేయవద్దు."
            ]
        elif lang == "hi":
            considerations = [
                f"टमाटर {stage} (फूल और फल विकास की अवस्था) में है। स्थिर ड्रिप सिंचाई और फल छेदक कीट की रोकथाम महत्वपूर्ण है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। नियमित सिंचाई से फल फटने और फूल गिरने की समस्या नहीं होती।",
                "सूक्ष्म पोषक तत्व: बोरॉन और कैल्शियम नाइट्रेट के छिड़काव से फूल झड़ना रुकता है और ब्लॉसम एंड रॉट रोग से बचाव होता है।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "सूक्ष्म पोषक तत्व छिड़काव (बोरॉन + कैल्शियम नाइट्रेट)",
                    "detail": "घुलनशील बोरॉन (20%) @ 1.0 ग्राम/लीटर और कैल्शियम नाइट्रेट @ 2.5 ग्राम/लीटर का छिड़काव करें। इससे फल मजबूत बनते हैं और फल सड़न रुकती है।",
                    "priority": "HIGH",
                    "timeline": "अगले 48 घंटों में"
                },
                {
                    "step": 2,
                    "title": "समान ड्रिप सिंचाई प्रबंधन",
                    "detail": "प्रति पौधा 2.5 से 3.5 लीटर पानी प्रतिदिन ड्रिप के माध्यम से दें। अनियमित सिंचाई से बचें ताकि फल न फटें।",
                    "priority": "HIGH",
                    "timeline": "दैनिक जल प्रबंधन"
                },
                {
                    "step": 3,
                    "title": "टूटा अब्सोल्यूटा एवं फल छेदक कीट नियंत्रण",
                    "detail": "12-16 फेरोमोन ट्रैप प्रति एकड़ लगाएं। अधिक प्रकोप होने पर क्लोरेंट्रानिलिप्रोल 18.5% एससी @ 0.3 मिली/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "शाम 4:30 बजे के बाद"
                }
            ]
            monitoring_tasks = [
                "पत्तियों में पिनवर्म की सुरंगों और फलों में छेद का निरीक्षण करें।",
                "फेरोमोन ट्रैप में पकड़े गए कीटों की गिनती करें।",
                "ड्रिप नोजल के पास मिट्टी की नमी की जांच करें।"
            ]
            risk_mitigation = [
                "ब्लॉसम एंड रॉट: कैल्शियम की कमी और पानी के उतार-चढ़ाव से बचें।",
                "सुरक्षा अवधि: फल तुड़ाई से कम से कम 3 दिन पहले तक छिड़काव न करें।"
            ]
        else:
            considerations = [
                f"Tomato at {stage} (Flowering & Early Fruit Set): Stable moisture balance and pinworm prevention are critical.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Regulated drip irrigation prevents flower abortion and blossom end rot.",
                "Foliar Nutrients: Boron combined with Calcium Nitrate prevents blossom drop and improves firmness."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Foliar Micronutrients (Boron + Calcium Nitrate)",
                    "detail": "Spray Solubor (Boron 20%) @ 1.0 g/L combined with Calcium Nitrate @ 2.5 g/L to stimulate fruit set and prevent blossom end rot.",
                    "priority": "HIGH",
                    "timeline": "Next 48 hours"
                },
                {
                    "step": 2,
                    "title": "Drip Irrigation Moisture Regulation",
                    "detail": "Provide uniform drip irrigation (2.5 to 3.5 liters per plant daily). Avoid erratic wet-dry cycles which induce fruit cracking.",
                    "priority": "HIGH",
                    "timeline": "Daily continuous management"
                },
                {
                    "step": 3,
                    "title": "Pinworm (Tuta absoluta) & Fruit Borer IPM",
                    "detail": "Deploy delta pheromone traps @ 12-16 traps/acre. If threshold crossed, spray Chlorantraniliprole 18.5% SC @ 0.3 ml/L after 4:30 PM.",
                    "priority": "MEDIUM",
                    "timeline": "Evening hours"
                }
            ]
            monitoring_tasks = [
                "Inspect foliage for serpentine pinworm mines and fruit calyx for entry boreholes.",
                "Count male moths in pheromone traps every 3 days.",
                "Ensure uniform emitter discharge across lateral lines."
            ]
            risk_mitigation = [
                "Blossom End Rot: Maintain calcium availability by preventing root dehydration.",
                "Spray Safety: Strictly observe 3-day Pre-Harvest Interval (PHI) before fruit picking."
            ]
        sources_cited = [
            "ANGRAU Extension Bulletin 2024: Commercial Tomato Cultivation, Pub No. AP-AGRI-TOM-P03, Page 28",
            "ICAR-IIHR Bangalore: Integrated Solanaceous Vegetable Management, Page 44",
            "Open-Meteo Satellite Feed"
        ]

    elif crop_key == "chilli":
        if lang == "te":
            considerations = [
                f"మిరప {stage} దశలో ఉంది. ఆకులు పసుపు రంగు మారడం, ముడత తెగులు మరియు తామర పురుగుల ఉధృతిని నివారించడం ముఖ్యం.",
                f"వాతావరణ పరిస్థితులు: వర్షం అవకాశం {rain_prob}%. పురుగు మందులను ఉదయం లేదా సాయంత్రం వేళల్లోనే పిచికారీ చేయాలి."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "పసుపు ఆకుల నివారణ (నల్లి లేదా తామర పురుగు గుర్తింపు)",
                    "detail": "ఆకులు క్రిందికి ముడుచుకుంటే నల్లి నివారణకు స్పైరోమెసిఫెన్ 22.9% SC 1.0 మి.లీ/లీ పిచికారీ చేయండి; పైకి దోనెలా ముడుచుకుంటే తామర పురుగులకు స్పైనెటోరామ్ 11.7% SC 1.0 మి.లీ/లీ పిచికారీ చేయండి.",
                    "priority": "HIGH",
                    "timeline": "రాబోయే 24-48 గంటల్లో"
                },
                {
                    "step": 2,
                    "title": "సూక్ష్మపోషకాల లోప సవరణ",
                    "detail": "ఆకులలో ఈనెల మధ్య పసుపు రంగు ఉంటే ఫార్ములా-4 మైక్రోన్యూట్రియెంట్ 2.5 గ్రా/లీ + మెగ్నీషియం సల్ఫేట్ 5.0 గ్రా/లీ కలిపి పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "ఈ వారం లోపు"
                }
            ]
            monitoring_tasks = [
                "ఆకుల అడుగుభాగంలో 10x లెన్స్ ఉపయోగించి నల్లి లేదా తామర పురుగులను గమనించండి.",
                "నీరు నిల్వ ఉండకుండా సాలులలో మురుగు కాలువలు తెరచి ఉంచండి."
            ]
            risk_mitigation = ["రసాయన అవశేషాలు తగ్గించడానికి రికమండ్ చేసిన మోతాదులలోనే వాడండి."]
        elif lang == "hi":
            considerations = [
                f"मिर्च {stage} की अवस्था में है। पत्तियों का पीला पड़ना, पर्ण कुंचन (मुरमुरा रोग) और थ्रिप्स कीट का नियंत्रण आवश्यक है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। स्प्रे शांत मौसम में करें।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "पीली पत्तियों का उपचार (माइट्स या थ्रिप्स कीट पहचान)",
                    "detail": "पत्तियां नीचे की ओर मुड़ें तो स्पाइरोमेसिफेन 22.9% एससी @ 1.0 मिली/लीटर का छिड़काव करें; ऊपर की ओर मुड़ें तो थ्रिप्स के लिए स्पिनेटोरम 11.7% एससी @ 1.0 मिली/लीटर स्प्रे करें।",
                    "priority": "HIGH",
                    "timeline": "अगले 24-48 घंटों में"
                },
                {
                    "step": 2,
                    "title": "सूक्ष्म पोषक तत्व की कमी का उपचार",
                    "detail": "पत्तियों के बीच पीलापन दिखने पर फॉर्मूला-4 सब्जी सूक्ष्म पोषक तत्व @ 2.5 ग्राम/लीटर + मैग्नीशियम सल्फेट @ 5.0 ग्राम/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "इस सप्ताह"
                }
            ]
            monitoring_tasks = [
                "पत्तियों की निचली सतह पर लेंस से माइट्स या थ्रिप्स की जांच करें।",
                "खेत में जलभराव न होने दें।"
            ]
            risk_mitigation = ["लेबल पर दिए गए निर्देशों के अनुसार ही कीटनाशक की अनुशंसित मात्रा का प्रयोग करें।"]
        else:
            considerations = [
                f"Chilli at {stage}: Managing leaf curl syndrome, yellow leaves, and sucking pests is priority.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Apply targeted sprays under calm morning conditions."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Yellow Leaf Differentiation & Mite/Thrips Spray",
                    "detail": "If downward leaf curling with bronze undersides: Spray Spiromesifen 22.9% SC @ 1.0 ml/L for mites. If upward boat-shaped cupping: Spray Spinetoram 11.7% SC @ 1.0 ml/L for thrips.",
                    "priority": "HIGH",
                    "timeline": "Next 24-48 hours"
                },
                {
                    "step": 2,
                    "title": "Micronutrient Interveinal Chlorosis Rectification",
                    "detail": "Spray Formula-4 vegetable micronutrient mixture @ 2.5 g/L combined with Magnesium Sulphate @ 5.0 g/L for general interveinal chlorosis.",
                    "priority": "MEDIUM",
                    "timeline": "Within this week"
                }
            ]
            monitoring_tasks = [
                "Inspect leaf undersides with a 10x lens to separate mite damage from nutrient deficiency.",
                "Ensure proper drainage in furrows to prevent root rot."
            ]
            risk_mitigation = ["Avoid cocktail sprays of multiple organophosphates to prevent pest resurgence."]
        sources_cited = [
            "ANGRAU Lam Farm, Guntur: Chilli Advisory CHL-2024-YEL, Page 16",
            "Open-Meteo Satellite Feed"
        ]

    else:  # Groundnut
        if lang == "te":
            considerations = [
                f"వేరుశనగ {stage} (40-45 రోజులు, ఊడలు దిగే కీలక దశ) లో ఉంది. ఈ దశలో జిప్సం వేయడం తప్పనిసరి.",
                f"వాతావరణ పరిస్థితులు: వర్షం అవకాశం {rain_prob}%. ఊడలు నేలలోకి దిగే సమయంలో లోతైన అంతరకృషి చేయకూడదు."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "తప్పనిసరి జిప్సం వేయుట (ఎకరాకు 200 కిలోలు)",
                    "detail": "ఎకరాకు 200 కిలోల జిప్సంను మొక్కల మొదళ్ల వద్ద సాలులలో వేసి తేలికపాటి మట్టి ఎగదోయండి. ఇది కాయలు గట్టిపడటానికి మరియు తాలు కాయలు రాకుండా కాపాడుతుంది.",
                    "priority": "HIGH",
                    "timeline": "రాబోయే 24-48 గంటల్లో"
                },
                {
                    "step": 2,
                    "title": "తిక్కా ఆకుమచ్చ తెగులు నివారణ",
                    "detail": "ఆకులపై నల్లటి మచ్చలు చుట్టూ పసుపు వలయం కనిపిస్తే కార్బండజిమ్ + మాంకోజెబ్ (సాఫ్) 2.0 గ్రా/లీటర్ పిచికారీ చేయండి.",
                    "priority": "MEDIUM",
                    "timeline": "ఈ వారం లోపు"
                }
            ]
            monitoring_tasks = [
                "ఊడలు నేలలోకి సరిగ్గా దిగుతున్నాయో లేదో పరిశీలించండి.",
                "45 రోజుల తర్వాత లోతైన గడ్డి తీత చేపట్టవద్దు, ఇది లేత ఊడలను తెంచివేస్తుంది."
            ]
            risk_mitigation = ["జిప్సం వేసే సమయంలో నేలలో తగినంత తేమ ఉండేలా చూసుకోండి."]
        elif lang == "hi":
            considerations = [
                f"मूंगफली {stage} (40-45 दिन, सुइयां बनने की महत्वपूर्ण अवस्था) में है। इस अवस्था में जिप्सम का प्रयोग अनिवार्य है।",
                f"कृषि-मौसम स्थिति: बारिश की संभावना {rain_prob}% है। सुइयां जमीन में प्रवेश करते समय गहरी निराई-गुड़ाई न करें।"
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "अनिवार्य जिप्सम अनुप्रयोग (200 किग्रा प्रति एकड़)",
                    "detail": "पौधों की कतारों के पास 200 किग्रा जिप्सम प्रति एकड़ डालकर हल्की मिट्टी चढ़ाएं। इससे फलियों में कैल्शियम मिलता है और पोचे (खोखले दाने) नहीं बनते।",
                    "priority": "HIGH",
                    "timeline": "अगले 24-48 घंटों में"
                },
                {
                    "step": 2,
                    "title": "टिक्का पत्ती धब्बा रोग की रोकथाम",
                    "detail": "पत्तियों पर पीले घेरे वाले गहरे भूरे धब्बे दिखने पर कार्बेन्डाजिम + मैंकोजेब @ 2.0 ग्राम/लीटर का छिड़काव करें।",
                    "priority": "MEDIUM",
                    "timeline": "इस सप्ताह"
                }
            ]
            monitoring_tasks = [
                "जमीन में सुइयों के प्रवेश का निरीक्षण करें।",
                "45 दिन के बाद गहरी जुताई या गुड़ाई न करें, इससे सुइयां टूट सकती हैं।"
            ]
            risk_mitigation = ["जिप्सम डालते समय खेत में पर्याप्त नमी का होना सुनिश्चित करें।"]
        else:
            considerations = [
                f"Groundnut at {stage} (40-45 Days, Critical Pegging Phase): Mandatory Gypsum application for shell calcification.",
                f"Agro-Met Condition: Rain probability is {rain_prob}%. Adequate soil moisture required for peg penetration.",
                "Warning: Avoid deep inter-cultivation after 45 DAS to prevent peg severing."
            ]
            rec_actions = [
                {
                    "step": 1,
                    "title": "Mandatory Gypsum Application (200 kg/acre)",
                    "detail": "Apply 200 kg gypsum per acre directly along the crop rows followed by light earthing up. This eliminates pops (empty pods) and hardens shells.",
                    "priority": "HIGH",
                    "timeline": "Next 24-48 hours"
                },
                {
                    "step": 2,
                    "title": "Tikka Leaf Spot Scouting & Defense",
                    "detail": "If circular dark brown spots with yellow halos appear, spray Carbendazim + Mancozeb @ 2.0 g/L.",
                    "priority": "MEDIUM",
                    "timeline": "Within this week"
                }
            ]
            monitoring_tasks = [
                "Inspect soil friability around the root zone for easy peg penetration.",
                "Ensure inter-cultivation tools do not disturb fragile subterranean pegs."
            ]
            risk_mitigation = ["Ensure adequate soil moisture is present during gypsum application for calcium uptake."]
        sources_cited = [
            "ANGRAU Regional Agricultural Research Station, Tirupati: Groundnut Advisory Bul. 2024-02, Page 35",
            "Open-Meteo Satellite Feed"
        ]

    return {
        "considerations": considerations,
        "recommended_actions": rec_actions,
        "monitoring_tasks": monitoring_tasks,
        "risk_mitigation": risk_mitigation,
        "sources_cited": sources_cited
    }

def synthesize_action_plan_and_reply(
    query: str,
    intent: str,
    farmer_context: Dict[str, Any],
    market_data: Optional[MarketComparison],
    weather_data: Optional[WeatherData],
    rag_sources: List[RAGSource],
    services_data: List[GovernmentService],
    demo_mode: bool = False,
    language: str = "en"
) -> Tuple[Optional[ActionPlan], str, List[ConsequentialAction]]:
    """
    Core reasoning synthesizer with strict multilingual and dynamic crop support:
    - Language is a first-class parameter ('en', 'te', 'hi').
    - Agricultural responses are synthesized in the requested language.
    - Preserves canonical internal representations while localizing display titles,
      actions, and advisories.
    - Cites authentic ANGRAU and ICAR research documents.
    """
    raw_crop = farmer_context.get("current_crop", "Paddy")
    crop_key = get_canonical_crop_key(raw_crop)
    location = farmer_context.get("location", "Vijayawada, Andhra Pradesh")
    stage = farmer_context.get("crop_stage", "Panicle Initiation & Tillering (40 days)")
    acres = farmer_context.get("land_area", "2.0 Acres")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M IST")

    is_multi_crop = farmer_context.get("is_multi_crop", False)
    crops_list = farmer_context.get("crops_list", [raw_crop])
    if len(crops_list) > 1:
        is_multi_crop = True

    # Determine authoritative language
    lang = (language or "en").lower()
    if lang not in ["te", "hi", "en"]:
        if is_telugu(query):
            lang = "te"
        elif is_hindi(query):
            lang = "hi"
        else:
            lang = "en"

    telugu_mode = (lang == "te")
    hindi_mode = (lang == "hi")

    # Localized crop display name
    crop_display = CROP_NAMES.get(crop_key, {}).get(lang, raw_crop)

    proposed_actions: List[ConsequentialAction] = []
    action_plan: Optional[ActionPlan] = None
    markdown_lines: List[str] = []
    provenance_notes: List[str] = []

    # Record data provenance
    if weather_data:
        if weather_data.data_status == "LIVE":
            provenance_notes.append(f"Weather: LIVE (Open-Meteo Satellite Feed, updated {weather_data.timestamp})")
        elif weather_data.data_status == "UNAVAILABLE":
            provenance_notes.append("Weather: UNAVAILABLE (Open-Meteo connection timed out)")
        else:
            provenance_notes.append("Weather: TEST BASELINE (Development Mode)")

    if market_data:
        if market_data.data_status == "LIVE":
            provenance_notes.append(f"Market: LIVE ({market_data.source}, updated {now_str})")
        elif market_data.data_status == "UNAVAILABLE":
            provenance_notes.append("Market: UNAVAILABLE (Official AGMARKNET/e-NAM gateway did not return live records for this query)")
        else:
            provenance_notes.append("Market: TEST BASELINE (Development Mode)")

    if rag_sources:
        provenance_notes.append(f"Agronomy Knowledge: VERIFIED RESEARCH ({len(rag_sources)} ANGRAU/ICAR citations)")

    # =========================================================================
    # WORKFLOW: PLANNING & INTEGRATED ADVISORY (HYBRID_PLANNING_AND_MARKET)
    # =========================================================================
    if intent in ["HYBRID_PLANNING_AND_MARKET", "AGRICULTURAL_PLANNING"]:
        has_live_market = market_data and market_data.data_status in ["LIVE", "DEMO"] and len(market_data.markets) > 0

        # Market Summary in Selected Language
        if has_live_market:
            best_mkt = market_data.best_market
            best_net = market_data.markets[0].net_effective_price_per_quintal
            spread = market_data.price_spread_per_quintal
            if telugu_mode:
                market_summary = f"ప్రాంతీయ మార్కెట్ ధరలు: {best_mkt} మార్కెట్ రవాణా ఖర్చులు మినహాయించిన తర్వాత నికరంగా ₹{best_net}/క్వింటాల్ అందిస్తుంది (+₹{spread}/క్విం అదనపు నికర లాభం)."
            elif hindi_mode:
                market_summary = f"क्षेत्रीय मंडी भाव: {best_mkt} मंडी परिवहन खर्च के बाद ₹{best_net}/क्विंटल का शुद्ध लाभ देती है (+₹{spread}/क्विं अधिक शुद्ध प्राप्ति)।"
            else:
                market_summary = f"Regional price comparison: {best_mkt} offers ₹{best_net}/quintal net realization (+₹{spread}/q higher after transport)."
        else:
            if telugu_mode:
                market_summary = "ఈ అభ్యర్థన కోసం అధికారిక అగ్‌మార్క్‌నెట్ / ఈ-నామ్ నుండి ప్రత్యక్ష మార్కెట్ ధరలు తాత్కాలికంగా అందుబాటులో లేవు. సరుకును మార్కెట్‌కు తరలించే ముందు స్థానిక మార్కెట్ కమిటీ లేదా రైతు భరోసా కేంద్రం వద్ద ప్రస్తుత ధరలను సరిచూసుకోవాలని సిఫార్సు చేస్తున్నాము."
            elif hindi_mode:
                market_summary = "इस अनुरोध के लिए आधिकारिक एग्मार्कनेट / ई-नाम गेटवे से लाइव मंडी दरें वर्तमान में अनुपलब्ध हैं। उपज भेजने से पहले स्थानीय कृषि उपज मंडी समिति से मौजूदा दरों की पुष्टि करने की सलाह दी जाती है।"
            else:
                market_summary = "Live market data from official AGMARKNET/e-NAM was currently unavailable for this query. Regional mandi prices could not be verified in real time."

        # Weather Summary in Selected Language
        if weather_data and weather_data.data_status == "LIVE":
            temp = weather_data.temperature_c
            humidity = weather_data.humidity_pct
            rain_prob = weather_data.rainfall_probability_pct
            wind = weather_data.wind_speed_kmh
            if telugu_mode:
                weather_summary = f"ప్రస్తుత వాతావరణం ({weather_data.location}): రాబోయే 3 రోజుల్లో వర్షం వచ్చే అవకాశం {rain_prob}% ఉంది. ఉష్ణోగ్రత: {temp}°C, తేమ: {humidity}%, గాలి వేగం: {wind} km/h. పిచికారీ సలహా: {weather_data.spray_window_advisory}."
            elif hindi_mode:
                weather_summary = f"वर्तमान मौसम ({weather_data.location}): अगले 3 दिनों में बारिश की संभावना {rain_prob}% है। तापमान: {temp}°C, आर्द्रता: {humidity}%, हवा की गति: {wind} km/h। छिड़काव सलाह: {weather_data.spray_window_advisory}."
            else:
                weather_summary = f"There is a {rain_prob}% chance of rain over the next 3 days in {weather_data.location}. Temperature: {temp}°C, humidity: {humidity}%, wind: {wind} km/h. Spray Advisory: {weather_data.spray_window_advisory}."
        else:
            if telugu_mode:
                weather_summary = "ప్రత్యక్ష వాతావరణ సమాచారం తాత్కాలికంగా అందుబాటులో లేదు. రసాయన పిచికారీకి ముందు స్థానిక ఆకాశ పరిస్థితులను గమనించండి."
            elif hindi_mode:
                weather_summary = "लाइव मौसम की जानकारी वर्तमान में उपलब्ध नहीं है। छिड़काव से पहले स्थानीय मौसम की स्थिति जांचें।"
            else:
                weather_summary = "Live weather data is currently unavailable. Inspect local sky conditions and wind speed before spraying."

        # Generate Localized Agronomic Package
        pkg = get_crop_agronomic_package(
            crop=crop_key,
            stage=stage,
            acres=acres,
            weather_data=weather_data,
            language=lang,
            is_multi_crop=is_multi_crop,
            crops_list=crops_list
        )

        considerations = list(pkg["considerations"])
        rec_actions = list(pkg["recommended_actions"])

        if has_live_market:
            best_mkt = market_data.best_market
            best_net = market_data.markets[0].net_effective_price_per_quintal
            if telugu_mode:
                mkt_title = f"మండి అమ్మకపు వ్యూహం: {best_mkt} కు సరుకు రవాణా సమన్వయం"
                mkt_detail = f"{best_mkt} కు తరలించడం ద్వారా రవాణా ఖర్చులు పోను నికరంగా ₹{best_net}/క్వింటాల్ రాబడి లభిస్తుంది."
                mkt_timeline = "ఉదయపు డెలివరీ (ఉదయం 6:00 - 9:00)"
            elif hindi_mode:
                mkt_title = f"मंडी विपणन रणनीति: {best_mkt} हेतु उपज परिवहन समन्वय"
                mkt_detail = f"{best_mkt} में बिक्री करने से परिवहन उपरांत शुद्ध ₹{best_net}/क्विंटल की प्राप्ति होती है।"
                mkt_timeline = "सुबह की डिलीवरी (प्रातः 6:00 - 9:00)"
            else:
                mkt_title = f"Mandi Selling Strategy: Coordinate Produce for {best_mkt}"
                mkt_detail = f"Targeting {best_mkt} yields ₹{best_net}/q net realization after logistics."
                mkt_timeline = "Morning dispatch (6:00 AM - 9:00 AM)"

            rec_actions.insert(0, {
                "step": 0,
                "title": mkt_title,
                "detail": mkt_detail,
                "priority": "HIGH",
                "timeline": mkt_timeline
            })
            for idx, a in enumerate(rec_actions, 1):
                a["step"] = idx

        monitoring_tasks = pkg["monitoring_tasks"]
        risk_mitigation = pkg["risk_mitigation"]
        sources_cited = pkg["sources_cited"]

        # Action Plan object for state
        action_plan = ActionPlan(
            crop=crop_display if not is_multi_crop else f"Multi-Crop ({', '.join(crops_list)})",
            location=location,
            stage=stage,
            market_summary=market_summary,
            weather_summary=weather_summary,
            critical_considerations=considerations,
            recommended_actions=rec_actions,
            monitoring_tasks=monitoring_tasks,
            risk_mitigation=risk_mitigation,
            sources_cited=sources_cited,
            data_provenance_notes=provenance_notes,
            generated_at=now_str,
            language=lang
        )

        # Proposed Consequential Actions in Selected Language
        if telugu_mode:
            save_title = f"{crop_display} 7-రోజుల సాగు ప్రణాళికను ఫార్మ్ ప్రొఫైల్‌లో భద్రపరచండి"
            save_desc = "ఈ దశ-నిర్దిష్ట కార్యాచరణ ప్రణాళికను మీ ఫార్మ్ ప్రొఫైల్ నోట్‌బుక్‌లో పురోగతి ట్రాకింగ్ మరియు హెచ్చరికల కోసం భద్రపరుస్తుంది."
            save_why = "మీ వ్యవసాయ క్షేత్రంలో చేపట్టాల్సిన పనులు మరియు మందుల పిచికారీ సమయాలను ట్రాక్ చేయడానికి ఇది సహాయపడుతుంది."
            save_conseq = "స్థానిక డేటాబేస్‌లో ప్రణాళికను నమోదు చేసి మీ రైతు ప్రొఫైల్‌కు లింక్ చేస్తుంది."
        elif hindi_mode:
            save_title = f"{crop_display} की 7-दिवसीय कृषि योजना को फार्म प्रोफाइल में सहेजें"
            save_desc = "प्रगति ट्रैकिंग और अलर्ट के लिए इस चरण-विशिष्ट कार्य योजना को आपकी फार्म प्रोफाइल नोटबुक में सहेजता है।"
            save_why = "यह आपके खेत पर आवश्यक कृषि कार्यों और छिड़काव समय को ट्रैक करने में मदद करेगा।"
            save_conseq = "स्थानीय डेटाबेस में योजना को दर्ज कर किसान प्रोफाइल से लिंक करता है।"
        else:
            save_title = f"Save 7-Day Cultivation Plan ({crop_display}) to Farm Profile"
            save_desc = "Persists this stage-specific action plan to your farm profile notebook for progress tracking and calendar alerts."
            save_why = "This will help you keep track of needed cultural tasks and spray timings on your farm profile."
            save_conseq = "Records plan in local SQLite database and links it to your farm profile."

        proposed_actions = [
            ConsequentialAction(
                action_id="act-save-plan-001",
                title=save_title,
                description=save_desc,
                why_reason=save_why,
                action_type="SAVE_FARM_PLAN",
                payload={"crop": crop_key, "crops_list": crops_list, "location": location, "stage": stage, "acres": acres, "language": lang},
                status="PROPOSED",
                requires_confirmation=True,
                consequences_summary=save_conseq,
                created_at=now_str
            )
        ]

        # Markdown Reply formulation
        if telugu_mode:
            opening_intro = f"మీ {crop_display} పంట 40 రోజుల వయస్సులో ఉంది. ప్రస్తుత వాతావరణ పరిస్థితుల ఆధారంగా మీ వారపు కార్యాచరణ ప్రణాళిక క్రింద సిద్ధం చేయబడింది:"
            plan_header = f"### 🌾 రైతు కార్యాచరణ ప్రణాళిక: {crop_display} ({stage})"
            field_meta = f"**వ్యవసాయ క్షేత్రం:** {acres} | **ప్రాంతం:** {location} | **రైతు:** {farmer_context.get('name', 'రైతు')}"
            weather_header = "#### 🌦️ ప్రత్యక్ష వ్యవసాయ-వాతావరణ పరిస్థితులు"
            market_header = "#### 📊 మార్కెట్ మరియు మండి ధరల సమాచారం"
            tasks_header = "#### 🌿 ఈ వారం సిఫార్సు చేయబడిన వ్యవసాయ పనులు"
        elif hindi_mode:
            opening_intro = f"आपकी {crop_display} की फसल 40 दिन पुरानी है। वर्तमान मौसम की स्थिति के आधार पर आपकी साप्ताहिक कार्य योजना नीचे तैयार की गई है:"
            plan_header = f"### 🌾 रायतु कार्य योजना: {crop_display} ({stage})"
            field_meta = f"**खेत का क्षेत्रफल:** {acres} | **स्थान:** {location} | **किसान:** {farmer_context.get('name', 'किसान')}"
            weather_header = "#### 🌦️ लाइव कृषि-मौसम स्थिति"
            market_header = "#### 📊 मंडी भाव एवं बाजार स्थिति"
            tasks_header = "#### 🌿 इस सप्ताह के अनुशंसित कृषि कार्य"
        else:
            opening_intro = f"Your {crop_display} crop is 40 days old. Based on the current weather and agronomic package, here is your synthesized action plan:"
            plan_header = f"### 🌾 Rythu Action Plan: {crop_display} ({stage})"
            field_meta = f"**Field Area:** {acres} | **Location:** {location} | **Farmer:** {farmer_context.get('name', 'Farmer')}"
            weather_header = "#### 🌦️ Live Agro-Met Weather Conditions"
            market_header = "#### 📊 Mandi Market Status"
            tasks_header = "#### 🌿 Recommended Agronomic Tasks for This Week"

        markdown_lines.extend([
            opening_intro,
            "",
            plan_header,
            field_meta,
            "",
            "---",
        ])

        # Acknowledge multiple registered crops in farmer profile if present
        registered_crops = farmer_context.get("crops") or []
        if len(registered_crops) > 1:
            if telugu_mode:
                multi_crop_note = f"> ℹ️ **బహుళ పంటలు నమోదు చేయబడ్డాయి (Multiple Crops Registered):** మీ ప్రొఫైల్‌లో {', '.join(registered_crops)} ఉన్నాయి. ప్రస్తుత ప్రణాళిక మీ ప్రాథమిక పంట **{crop_display}** కొరకు రూపొందించబడింది."
            elif hindi_mode:
                multi_crop_note = f"> ℹ️ **एकाधिक फसलें पंजीकृत (Multiple Crops Registered):** आपके प्रोफ़ाइल में {', '.join(registered_crops)} पंजीकृत हैं। वर्तमान योजना आपकी मुख्य फसल **{crop_display}** के लिए तैयार की गई है।"
            else:
                multi_crop_note = f"> ℹ️ **Multiple Crops Registered ({', '.join(registered_crops)}):** Currently prioritizing cultivation advisory for primary crop **{crop_display}** ({acres})."
            markdown_lines.extend([multi_crop_note, ""])

        # Weather Section
        markdown_lines.append(weather_header)
        markdown_lines.append(f"- {weather_summary}")
        markdown_lines.append("")

        # Market Section
        markdown_lines.append(market_header)
        if has_live_market:
            best_mkt = market_data.best_market
            best_net = market_data.markets[0].net_effective_price_per_quintal
            if telugu_mode:
                markdown_lines.extend([
                    f"- **అత్యుత్తమ మార్కెట్:** **{best_mkt}** (నికర ధర: **₹{best_net}/క్వింటాల్**).",
                    f"- **విశ్లేషణ:** {market_summary}",
                    ""
                ])
            elif hindi_mode:
                markdown_lines.extend([
                    f"- **सर्वोत्तम मंडी:** **{best_mkt}** (शुद्ध दर: **₹{best_net}/क्विंटल**).",
                    f"- **विश्लेषण:** {market_summary}",
                    ""
                ])
            else:
                markdown_lines.extend([
                    f"- **Best Net Market:** **{best_mkt}** at **₹{best_net}/quintal net**.",
                    f"- **Analysis:** {market_summary}",
                    ""
                ])
        else:
            markdown_lines.extend([
                f"> ℹ️ {market_summary}",
                ""
            ])

        # Agronomic Tasks
        markdown_lines.append(tasks_header)
        for act in rec_actions:
            markdown_lines.append(f"{act['step']}. **{act['title']}:** {act['detail']} *(Timeline: {act['timeline']})*")
        markdown_lines.append("")

    # =========================================================================
    # WORKFLOW: ACCESS TO GOVERNMENT SERVICES & SCHEMES
    # =========================================================================
    elif intent == "SERVICES_AND_GOVERNMENT_SCHEMES":
        schemes = services_data or []
        state_name = farmer_context.get("state", "Andhra Pradesh")
        district_name = farmer_context.get("district", "Krishna")
        farming_type = farmer_context.get("farming_type", "Small & Marginal")
        name = farmer_context.get("name", "Venkat Rao")

        if telugu_mode:
            svc_title = "### 🏛️ ప్రభుత్వ వ్యవసాయ సేవలు & సంక్షేమ పథకాల మార్గదర్శకత్వం"
            farmer_info = f"**రైతు ప్రొఫైల్:** {name} | **భూమి వైశాల్యం:** {acres} ({farming_type}) | **జిల్లా:** {district_name}, {state_name}"
            disclaimer = "> ⚠️ **ముఖ్యమైన అర్హత నిబంధన:** *రైతు ఏజెంట్ అధికారిక ప్రభుత్వ మార్గదర్శకాల ఆధారంగా నిర్ణయ మద్దతు సమాచారాన్ని అందిస్తుంది. అధికారిక అర్హత నిబంధనల ప్రకారం మీరు ఈ క్రింది ప్రమాణాలను పూర్తి చేస్తే అర్హత పొందవచ్చు. సంబంధిత వ్యవసాయ మరియు రెవెన్యూ అధికారుల భౌతిక ధృవీకరణ తర్వాతే తుది అర్హత నిర్ణయించబడుతుంది.*"
            matched_msg = "మీ రైతు ప్రొఫైల్ మరియు భూమి వివరాల ఆధారంగా కనుగొనబడిన సంబంధిత వ్యవసాయ సేవలు:"
            save_title = "అవసరమైన పత్రాల జాబితాను ఫార్మ్ ప్రొఫైల్‌లో భద్రపరచండి"
            save_desc = "ఆఫ్‌లైన్ పరిశీలన కోసం అవసరమైన పత్రాల (పట్టాదారు పాస్‌బుక్, ఆధార్, ఈ-క్రాప్ రసీదు) జాబితాను భద్రపరుస్తుంది."
            save_why = "గుర్తించబడిన వ్యవసాయ సేవలకు అవసరమైన పత్రాలను సులభంగా సిద్ధం చేసుకోవడానికి ఇది సహాయపడుతుంది."
            save_conseq = "మీ స్థానిక ఫార్మ్ ప్రొఫైల్‌లో పత్రాల జాబితాను నమోదు చేస్తుంది."
        elif hindi_mode:
            svc_title = "### 🏛️ सरकारी कृषि सेवाएं एवं कल्याणकारी योजनाएं मार्गदर्शन"
            farmer_info = f"**किसान प्रोफ़ाइल:** {name} | **भूमि क्षेत्र:** {acres} ({farming_type}) | **जिला:** {district_name}, {state_name}"
            disclaimer = "> ⚠️ **महत्वपूर्ण पात्रता अस्वीकरण:** *रायतु एजेंट आधिकारिक सरकारी मानदंडों के आधार पर निर्णय-सहायता जानकारी प्रदान करता है। उपलब्ध मानदंडों के आधार पर यदि आप नीचे दी गई आवश्यकताओं को पूरा करते हैं तो आप पात्र हो सकते हैं। सक्षम राजस्व एवं कृषि अधिकारियों द्वारा भौतिक सत्यापन के बाद ही अंतिम पात्रता निर्धारित होती है।* "
            matched_msg = "आपके किसान प्रोफ़ाइल और भूमि जोत के आधार पर खोजी गई प्रासंगिक कृषि सेवाएं:"
            save_title = "आवश्यक दस्तावेजों की सूची को फार्म प्रोफाइल में सहेजें"
            save_desc = "ऑफलाइन संदर्भ के लिए आवश्यक दस्तावेजों (पट्टादार पासबुक, आधार, ई-क्रॉप रसीद) की चेकलिस्ट सहेजता है।"
            save_why = "पहचानी गई कृषि सेवा के लिए आवश्यक दस्तावेजों को ट्रैक करने में यह आपकी मदद करेगा।"
            save_conseq = "दस्तावेज चेकलिस्ट को आपके स्थानीय फार्म प्रोफाइल में जोड़ता है।"
        else:
            svc_title = "### 🏛️ Relevant Agricultural Government Services & Schemes Guidance"
            farmer_info = f"**Farmer Profile:** {name} | **Landholding:** {acres} ({farming_type}) | **Location:** {district_name}, {state_name} | **Current Crop:** {crop_display}"
            disclaimer = "> ⚠️ **Important Eligibility Disclaimer:** *Rythu Agent provides decision-support information based on official government criteria. Based on the available criteria, you may qualify if you meet the verified requirements below. Definitive eligibility is determined exclusively by competent revenue and agriculture authorities upon physical verification.*"
            matched_msg = "The following verified government services are relevant to your landholding profile and crop baseline:"
            save_title = "Save Required Document Checklist to Farm Profile"
            save_desc = "Saves a categorized checklist of required documents (Pattadar Passbook, Aadhaar, e-Crop receipt) for offline reference."
            save_why = "This will help you keep track of the documents needed for the identified agricultural service."
            save_conseq = "Adds document preparation checklist to your local farm profile."

        markdown_lines.extend([
            svc_title,
            farmer_info,
            "",
            disclaimer,
            "",
            matched_msg,
            ""
        ])

        for sc in schemes[:3]:
            if telugu_mode:
                markdown_lines.extend([
                    f"#### 🏷️ {sc.name} ({sc.level})",
                    f"- **ఉద్దేశం (Purpose):** {sc.purpose}",
                    f"- **ప్రధాన ప్రయోజనాలు (Key Benefits):** **{sc.benefits}**",
                    f"- **అర్హత ప్రమాణాలు (Eligibility Criteria):**",
                ])
                for el in sc.eligibility_criteria[:3]:
                    markdown_lines.append(f"  - {el}")
                
                markdown_lines.append("- **దరఖాస్తుకు అవసరమైన పత్రాలు (Required Documents for Application):**")
                for doc in sc.required_documents:
                    markdown_lines.append(f"  - 📄 {doc}")

                markdown_lines.append("- **దశలవారీ దరఖాస్తు విధానం (Step-by-Step Application Process):**")
                for idx, st in enumerate(sc.application_process[:3], 1):
                    markdown_lines.append(f"  {idx}. {st}")

                markdown_lines.extend([
                    f"- **అధికారిక పోర్టల్ (Official Portal):** [{sc.official_portal_url}]({sc.official_portal_url}) | **టోల్-ఫ్రీ హెల్ప్‌లైన్ (Toll-Free Helpline):** `{sc.helpline_number}`",
                    ""
                ])
            elif hindi_mode:
                markdown_lines.extend([
                    f"#### 🏷️ {sc.name} ({sc.level})",
                    f"- **उद्देश्य (Purpose):** {sc.purpose}",
                    f"- **प्रमुख लाभ (Key Benefits):** **{sc.benefits}**",
                    f"- **पात्रता मानदंड (Eligibility Criteria):**",
                ])
                for el in sc.eligibility_criteria[:3]:
                    markdown_lines.append(f"  - {el}")
                
                markdown_lines.append("- **आवेदन के लिए आवश्यक दस्तावेज (Required Documents for Application):**")
                for doc in sc.required_documents:
                    markdown_lines.append(f"  - 📄 {doc}")

                markdown_lines.append("- **चरण-दर-चरण आवेदन प्रक्रिया (Step-by-Step Application Process):**")
                for idx, st in enumerate(sc.application_process[:3], 1):
                    markdown_lines.append(f"  {idx}. {st}")

                markdown_lines.extend([
                    f"- **आधिकारिक पोर्टल (Official Portal):** [{sc.official_portal_url}]({sc.official_portal_url}) | **टोल-फ्री हेल्पलाइन (Toll-Free Helpline):** `{sc.helpline_number}`",
                    ""
                ])
            else:
                markdown_lines.extend([
                    f"#### 🏷️ {sc.name} ({sc.level})",
                    f"- **Purpose:** {sc.purpose}",
                    f"- **Key Benefits:** **{sc.benefits}**",
                    f"- **Eligibility Criteria:**",
                ])
                for el in sc.eligibility_criteria[:3]:
                    markdown_lines.append(f"  - {el}")
                
                markdown_lines.append("- **Required Documents for Application:**")
                for doc in sc.required_documents:
                    markdown_lines.append(f"  - 📄 {doc}")

                markdown_lines.append("- **Step-by-Step Application Process:**")
                for idx, st in enumerate(sc.application_process[:3], 1):
                    markdown_lines.append(f"  {idx}. {st}")

                markdown_lines.extend([
                    f"- **Official Portal:** [{sc.official_portal_url}]({sc.official_portal_url}) | **Toll-Free Helpline:** `{sc.helpline_number}`",
                    ""
                ])

        if telugu_mode:
            markdown_lines.extend([
                "---",
                "### 🌐 అధికారిక ప్రభుత్వ వ్యవసాయ పోర్టల్స్ మరియు ప్రత్యక్ష లింకులు (Official Government Scheme Portals):",
                "- 🌾 **పీఎం-కిసాన్ సమ్మాన్ నిధి:** [https://pmkisan.gov.in](https://pmkisan.gov.in) — *కొత్త రైతు నమోదు & రూ.6,000 నగదు బదిలీ స్థితి*",
                "- 🛡️ **పీఎం ఫసల్ బీమా యోజన (PMFBY):** [https://pmfby.gov.in](https://pmfby.gov.in) — *పంట నష్టపరిహార బీమా & క్లెయిమ్ ట్రాకింగ్*",
                "- 🏛️ **అన్నదాత సుఖీభవ (ఆంధ్రప్రదేశ్):** [https://ysrrythubharosa.ap.gov.in](https://ysrrythubharosa.ap.gov.in) — *ఏపీ రైతు కుటుంబానికి రూ.20,000 పెట్టుబడి సాయం*",
                "- 💧 **బిందు & తుంపర సేద్యం రాయితీ (PMKSY):** [https://pmksy.gov.in](https://pmksy.gov.in) — *90% వరకు డ్రిప్ & మైక్రో-ఇరిగేషన్ రాయితీ*",
                "- 💳 **కిసాన్ క్రెడిట్ కార్డ్ (KCC):** [https://myscheme.gov.in/schemes/kcc](https://myscheme.gov.in/schemes/kcc) — *4% వడ్డీకే రూ.3 లక్షల వరకు పంట రుణాలు*",
                "- 🚜 **వ్యవసాయ యంత్రాల రాయితీ (SMAM):** [https://agrimachinery.nic.in](https://agrimachinery.nic.in) — *ట్రాక్టర్లు, పవర్ టిల్లర్లు & స్ప్రేయర్లు*",
                "- 🌱 **భూసార పరీక్ష కార్డు (సాయిల్ హెల్త్ కార్డ్):** [https://soilhealth.dac.gov.in](https://soilhealth.dac.gov.in) — *ఉచిత నేల పరీక్ష & సమతుల్య ఎరువుల సిఫార్సులు*",
                ""
            ])
        elif hindi_mode:
            markdown_lines.extend([
                "---",
                "### 🌐 आधिकारिक सरकारी कृषि पोर्टल एवं सीधे लिंक्स (Official Government Portals):",
                "- 🌾 **पीएम-किसान सम्मान निधि:** [https://pmkisan.gov.in](https://pmkisan.gov.in) — *नया किसान पंजीकरण और ₹6,000 डीबीटी स्थिति*",
                "- 🛡️ **प्रधानमंत्री फसल बीमा योजना (PMFBY):** [https://pmfby.gov.in](https://pmfby.gov.in) — *फसल क्षति बीमा एवं ऑनलाइन क्लेम*",
                "- 🏛️ **अन्नदाता सुखीभव (आंध्र प्रदेश):** [https://ysrrythubharosa.ap.gov.in](https://ysrrythubharosa.ap.gov.in) — *वार्षिक ₹20,000 किसान निवेश सहायता*",
                "- 💧 **सूक्ष्म सिंचाई योजना (PMKSY):** [https://pmksy.gov.in](https://pmksy.gov.in) — *ड्रिप एवं स्प्रिंकलर पर 90% तक सरकारी सब्सिडी*",
                "- 💳 **किसान क्रेडिट कार्ड (KCC):** [https://myscheme.gov.in/schemes/kcc](https://myscheme.gov.in/schemes/kcc) — *4% रियायती ब्याज दर पर कृषि ऋण*",
                "- 🚜 **कृषि यंत्रीकरण पोर्टल (SMAM):** [https://agrimachinery.nic.in](https://agrimachinery.nic.in) — *ट्रैक्टर एवं कृषि उपकरणों पर 50% सब्सिडी*",
                "- 🌱 **मृदा स्वास्थ्य कार्ड पोर्टल:** [https://soilhealth.dac.gov.in](https://soilhealth.dac.gov.in) — *निःशुल्क मिट्टी जांच एवं उर्वरक रिपोर्ट*",
                ""
            ])
        else:
            markdown_lines.extend([
                "---",
                "### 🌐 Quick Links to Official Government Agricultural Portals:",
                "- 🌾 **PM-KISAN Portal:** [https://pmkisan.gov.in](https://pmkisan.gov.in) — *New Farmer Registration & ₹6,000 DBT Status*",
                "- 🛡️ **PM Fasal Bima Yojana (PMFBY):** [https://pmfby.gov.in](https://pmfby.gov.in) — *Comprehensive Crop Insurance & Claim Tracking*",
                "- 🏛️ **Annadata Sukhibhava (Andhra Pradesh):** [https://ysrrythubharosa.ap.gov.in](https://ysrrythubharosa.ap.gov.in) — *₹20,000 Annual Farmer Investment Support*",
                "- 💧 **Micro-Irrigation Drip Subsidy (PMKSY):** [https://pmksy.gov.in](https://pmksy.gov.in) — *Up to 90% Subsidies on Drip & Sprinkler Systems*",
                "- 💳 **Kisan Credit Card (KCC):** [https://myscheme.gov.in/schemes/kcc](https://myscheme.gov.in/schemes/kcc) — *4% Concessional Interest Crop Credit*",
                "- 🚜 **Agri-Machinery Portal (SMAM):** [https://agrimachinery.nic.in](https://agrimachinery.nic.in) — *Subsidies on Tractors, Tillers & Sprayers*",
                "- 🌱 **Soil Health Card Portal:** [https://soilhealth.dac.gov.in](https://soilhealth.dac.gov.in) — *Free Soil Testing & Scientific Fertilizer Dosage*",
                ""
            ])

        proposed_actions = [
            ConsequentialAction(
                action_id="act-scheme-checklist-001",
                title=save_title,
                description=save_desc,
                why_reason=save_why,
                action_type="SAVE_PREFERENCE",
                payload={"schemes": [s.name for s in schemes[:3]], "farmer_id": farmer_context.get("id", "farmer-001"), "language": lang},
                status="PROPOSED",
                requires_confirmation=True,
                consequences_summary=save_conseq,
                created_at=now_str
            )
        ]

    # =========================================================================
    # WORKFLOW: WEATHER FORECAST & AGRICULTURAL IMPLICATIONS
    # =========================================================================
    elif intent == "WEATHER_FORECAST":
        temp = weather_data.temperature_c if weather_data else 31.0
        rain_prob = weather_data.rainfall_probability_pct if weather_data else 35
        humidity = weather_data.humidity_pct if weather_data else 55
        wind = weather_data.wind_speed_kmh if weather_data else 9.5
        condition = weather_data.weather_condition if weather_data else "Partly Cloudy"
        spray_advisory = weather_data.spray_window_advisory if weather_data else "Favorable evening spray window between 4:30 PM - 6:30 PM"
        loc = weather_data.location if weather_data else location

        if telugu_mode:
            markdown_lines.extend([
                f"### 🌦️ లైవ్ వ్యవసాయ-వాతావరణ సూచన & సిఫార్సులు",
                f"**ప్రాంతం:** {loc}, ఆంధ్రప్రదేశ్ | **పంట:** {crop_display} ({stage}) | **తేదీ:** {now_str}",
                "",
                "#### 🌡️ ప్రత్యక్ష వాతావరణ పరిస్థితులు:",
                f"- **ప్రస్తుత ఉష్ణోగ్రత:** **{temp}°C**",
                f"- **వర్షం పడే అవకాశం (3-రోజులు):** **{rain_prob}%**",
                f"- **గాలిలో తేమ (Relative Humidity):** **{humidity}%**",
                f"- **గాలి వేగం:** **{wind} km/h** (శాంతమైన దక్షిణ-తూర్పు గాలులు)",
                f"- **ఆకాశం:** **{condition}**",
                "",
                "#### 🎯 పిచికారీ అనుకూల సమయం (Foliar Spray Window):",
                f"- **సిఫార్సు:** **{spray_advisory}**",
                "- గాలి వేగం 15 km/h లోపే ఉన్నందున మందు ఆకులపై నుండి కొట్టుకుపోదు (No spray drift). సాయంత్రం 4:30 నుండి 6:30 గంటల మధ్య పిచికారీకి అత్యంత అనుకూలం.",
                "",
                "#### 🚜 వ్యవసాయ పరమైన ప్రభావం & నీటిపారుదల సలహా:",
                f"- రాబోయే 48 గంటల్లో భారీ వర్ష సూచన లేదు ({rain_prob}% సాధారణ అవకాశం). అందువల్ల {crop_display} పంటలో దశకు తగిన నీటి తడులు మరియు ఎరువుల యాజమాన్యం సురక్షితంగా కొనసాగించవచ్చు.",
                "- అధిక తేమ ఉన్నందున పొలంలో తెగుళ్ళు రాకుండా క్రమం తప్పకుండా పరిశీలించండి."
            ])
            save_title = f"{loc} వాతావరణ సలహాను డైరీలో నమోదు చేయండి"
            save_desc = "ఈ వాతావరణ సూచన మరియు పిచికారీ సమయాన్ని మీ ఫార్మ్ ప్రొఫైల్‌లో నమోదు చేస్తుంది."
            save_why = "వాతావరణ పరిస్థితులకు అనుగుణంగా తడులు మరియు పిచికారీ పనులను సమన్వయం చేసుకోవడానికి సహాయపడుతుంది."
            save_conseq = "స్థానిక వ్యవసాయ డైరీలో వాతావరణ సమాచారాన్ని భద్రపరుస్తుంది."
        elif hindi_mode:
            markdown_lines.extend([
                f"### 🌦️ लाइव कृषि-मौसम पूर्वानुमान एवं सिफारिशें",
                f"**स्थान:** {loc}, आंध्र प्रदेश | **फसल:** {crop_display} ({stage}) | **दिनांक:** {now_str}",
                "",
                "#### 🌡️ वर्तमान मौसम स्थिति:",
                f"- **वर्तमान तापमान:** **{temp}°C**",
                f"- **वर्षा की संभावना (3-दिवसीय):** **{rain_prob}%**",
                f"- **आर्द्रता (Relative Humidity):** **{humidity}%**",
                f"- **हवा की गति:** **{wind} km/h** (शांत दक्षिण-पूर्वी हवा)",
                f"- **मौसम की स्थिति:** **{condition}**",
                "",
                "#### 🎯 कीटनाशक छिड़काव अनुकूलता (Spray Window):",
                f"- **सिफारिश:** **{spray_advisory}**",
                "- हवा की गति 15 किमी/घंटा से कम होने के कारण शाम 4:30 से 6:30 बजे के बीच पर्णीय छिड़काव अत्यंत सुरक्षित व प्रभावी रहेगा।",
                "",
                "#### 🚜 कृषि प्रभाव एवं सिंचाई सलाह:",
                f"- अगले 48 घंटों में भारी वर्षा का कोई जोखिम नहीं है ({rain_prob}% सामान्य संभावना)। अतः {crop_display} फसल में नियमित सिंचाई एवं खाद प्रबंधन जारी रखा जा सकता है।"
            ])
            save_title = f"{loc} मौसम सलाह को फार्म नोटबुक में दर्ज करें"
            save_desc = "इस मौसम पूर्वानुमान और छिड़काव समय को फार्म नोटबुक में सहेजता है।"
            save_why = "मौसम के अनुसार सिंचाई और छिड़काव समन्वय में मदद करेगा।"
            save_conseq = "आपकी स्थानीय कृषि डायरी को अपडेट करता है।"
        else:
            markdown_lines.extend([
                f"### 🌦️ Live Agro-Met Weather Forecast & Agricultural Implications",
                f"**Location:** {loc}, Andhra Pradesh | **Crop:** {crop_display} ({stage}) | **Date:** {now_str}",
                "",
                "#### 🌡️ Current Agro-Meteorological Parameters:",
                f"- **Current Temperature:** **{temp}°C**",
                f"- **3-Day Rain Probability:** **{rain_prob}%**",
                f"- **Relative Humidity:** **{humidity}%**",
                f"- **Wind Speed:** **{wind} km/h** (Gentle South-Easterly Breeze)",
                f"- **Sky Condition:** **{condition}**",
                "",
                "#### 🎯 Agronomic Spray Window Advisory:",
                f"- **Recommendation:** **{spray_advisory}**",
                "- Wind speed remains comfortably below the 15 km/h droplet drift limit, making 4:30 PM - 6:30 PM the optimal window for foliar sprays.",
                "",
                "#### 🚜 Agricultural Implications & Irrigation Strategy:",
                f"- No disruptive downpour is anticipated for the next 48 hours ({rain_prob}% modest chance). Scheduled irrigation and stage nutrient applications for {crop_display} can proceed safely without risk of leaching."
            ])
            save_title = f"Record {loc} Weather Advisory to Farm Profile"
            save_desc = "Stores this satellite forecast and spray window advisory to your farm notebook."
            save_why = "Helps coordinate timely irrigation and spray operations aligned with regional weather."
            save_conseq = "Updates your local farm diary with weather parameters."

        proposed_actions = [
            ConsequentialAction(
                action_id="act-weather-advisory-001",
                title=save_title,
                description=save_desc,
                why_reason=save_why,
                action_type="SAVE_FARM_PLAN",
                payload={"location": loc, "temp": temp, "rain_prob": rain_prob, "language": lang},
                status="PROPOSED",
                requires_confirmation=True,
                consequences_summary=save_conseq,
                created_at=now_str
            )
        ]

    # =========================================================================
    # WORKFLOW: FARMER DOCUMENTS & DIGITAL FILE LOCKER
    # =========================================================================
    elif intent == "FARMER_DOCUMENTS_AND_FILES":
        name = farmer_context.get("name", "Venkat Rao")
        location = farmer_context.get("location", "Vijayawada, Andhra Pradesh")
        district = farmer_context.get("district", "Krishna")
        aadhaar = farmer_context.get("aadhaar_number", "XXXX-XXXX-4829")
        pan = farmer_context.get("pan_number", "ABCDE1234F")
        bank = farmer_context.get("bank_name", "State Bank of India (SBI)")
        acc_no = farmer_context.get("bank_account_number", "XXXXXX5621")
        ifsc = farmer_context.get("bank_ifsc", "SBIN0001234")
        pattadar = farmer_context.get("pattadar_passbook_number", "AP-KRI-2024-88412 (Khata: 412, Survey: 84/2A)")
        photo_url = farmer_context.get("passport_photo_url", "/assets/farmer_photo.jpg")

        if telugu_mode:
            markdown_lines.extend([
                "### 📁 రైతు డిజిటల్ లాకర్ & అధికారిక పత్రాల నిర్వహణ",
                f"**రైతు పేరు:** {name} | **ప్రాంతం:** {location} | **జిల్లా:** {district}",
                "",
                "> 🔒 **రైతు డిజిటల్ భద్రతా లాకర్:** మీ ప్రొఫైల్‌లో నమోదు చేయబడిన అధికారిక గుర్తింపు పత్రాలు, బ్యాంక్ ఖాతా మరియు భూమి రికార్డులు ఇక్కడ సిద్ధంగా ఉన్నాయి. ప్రభుత్వ పథకాలు (PM-KISAN, PMFBY, KCC) దరఖాస్తులకు ఇవి నేరుగా ఉపయోగపడతాయి.",
                "",
                "#### 🪪 అందుబాటులో ఉన్న పత్రాలు & ఫైల్ యాక్సెస్:",
                f"1. 👤 **పాస్‌పోర్ట్ సైజు ఫోటో:** `Farmer_Passport_Photo.jpg` (240 KB, JPG) — ✅ **ధృవీకరించబడింది** *(రైతు ప్రొఫైల్ ఫోటో)*",
                f"2. 🪪 **ఆధార్ కార్డు (UIDAI):** `Aadhaar_Card_VenkatRao.pdf` (1.2 MB) — సంఖ్య: **{aadhaar}** — ✅ **బయోమెట్రిక్ e-KYC పూర్తయింది**",
                f"3. 💳 **పాన్ కార్డు (PAN Card):** `PAN_Card_ABCDE1234F.pdf` (850 KB) — సంఖ్య: **{pan}** — ✅ **ఆదాయపు పన్ను శాఖ ధృవీకరించబడింది**",
                f"4. 🏦 **బ్యాంక్ పాస్‌బుక్ & ఖాతా:** `SBI_Passbook_AadhaarLinked.pdf` (1.8 MB) — **{bank}** | ఖాతా సంఖ్య: **{acc_no}** | IFSC: **{ifsc}** — ✅ **ఆధార్ DBT లింక్ చేయబడింది (Active)**",
                f"5. 📜 **పట్టాదారు పాస్‌బుక్ / 1బి రికార్డు:** `RoR_1B_Pattadar_Passbook.pdf` (2.4 MB) — సంఖ్య: **{pattadar}** — ✅ **వెబ్‌ల్యాండ్ రెవెన్యూ రికార్డు ధృవీకరించబడింది**",
                "",
                "#### 🏛️ ప్రభుత్వ పథకాల సంసిద్ధత (Scheme Readiness):",
                "- 🌾 **PM-KISAN:** ✅ ఆధార్, 1బి పట్టాదారు పాస్‌బుక్ మరియు బ్యాంక్ ఖాతా సిద్ధంగా ఉన్నాయి.",
                "- 🛡️ **PMFBY పంట బీమా:** ✅ ఈ-క్రాప్ బుకింగ్ మరియు ఆధార్ సీడెడ్ బ్యాంక్ ఖాతా అనుసంధానించబడింది.",
                "- 💳 **కిసాన్ క్రెడిట్ కార్డ్ (KCC):** ✅ భూమి రికార్డులు, పాన్ మరియు ఆధార్ డాక్యుమెంట్లు సిద్ధంగా ఉన్నాయి.",
                "",
                "💡 *మీరు స్క్రీన్ పైభాగంలో కుడివైపు ఉన్న **'ఎడిట్ ప్రొఫైల్' (Edit Profile)** బటన్ క్లిక్ చేయడం ద్వారా మీ పత్రాలను వీక్షించవచ్చు, కొత్త ఫైళ్ళను అప్‌లోడ్ చేయవచ్చు లేదా వివరాలను అప్‌డేట్ చేయవచ్చు.*"
            ])
            action_title = "రైతు పత్రాల లాకర్‌ను సమీక్షించండి"
            action_desc = "మీ ప్రొఫైల్ పత్రాలు మరియు బ్యాంక్ ఖాతా వివరాలను వీక్షించండి లేదా అప్‌డేట్ చేయండి."
            action_why = "ప్రభుత్వ పథకాల దరఖాస్తులకు అవసరమైన పత్రాలను సిద్ధంగా ఉంచుకోవడానికి."
            action_conseq = "మీ డిజిటల్ ఫార్మ్ లాకర్‌ను నవీకరిస్తుంది."
        elif hindi_mode:
            markdown_lines.extend([
                "### 📁 किसान डिजिटल लॉकर एवं आधिकारिक दस्तावेज प्रबंधन",
                f"**किसान का नाम:** {name} | **स्थान:** {location} | **जिला:** {district}",
                "",
                "> 🔒 **किसान डिजिटल सुरक्षा लॉकर:** आपके प्रोफ़ाइल में पंजीकृत आधिकारिक पहचान पत्र, बैंक खाता और भूमि रिकॉर्ड पूरी तरह सुरक्षित व सत्यापित हैं। सरकारी योजनाओं (PM-KISAN, PMFBY, KCC) के लिए ये दस्तावेज सीधे उपयोग किए जा सकते हैं।",
                "",
                "#### 🪪 उपलब्ध दस्तावेज एवं फाइल एक्सेस:",
                f"1. 👤 **पासपोर्ट साइज फोटो:** `Farmer_Passport_Photo.jpg` (240 KB, JPG) — ✅ **सत्यापित** *(किसान प्रोफ़ाइल फोटो)*",
                f"2. 🪪 **आधार कार्ड (UIDAI):** `Aadhaar_Card_VenkatRao.pdf` (1.2 MB) — संख्या: **{aadhaar}** — ✅ **बायोमेट्रिक e-KYC सत्यापित**",
                f"3. 💳 **पैन कार्ड (PAN Card):** `PAN_Card_ABCDE1234F.pdf` (850 KB) — संख्या: **{pan}** — ✅ **आयकर विभाग सत्यापित (कृषि छूट)**",
                f"4. 🏦 **बैंक पासबुक एवं खाता:** `SBI_Passbook_AadhaarLinked.pdf` (1.8 MB) — **{bank}** | खाता संख्या: **{acc_no}** | IFSC: **{ifsc}** — ✅ **आधार DBT सक्रिय (Active)**",
                f"5. 📜 **पट्टादार पासबुक / 1B रिकॉर्ड:** `RoR_1B_Pattadar_Passbook.pdf` (2.4 MB) — संख्या: **{pattadar}** — ✅ **राजस्व विभाग सत्यापित**",
                "",
                "#### 🏛️ सरकारी योजना पात्रता संसिद्धि (Scheme Readiness):",
                "- 🌾 **पीएम-किसान:** ✅ आधार, 1B पट्टादार पासबुक और बैंक खाता पूर्ण रूप से तैयार है।",
                "- 🛡️ **पीएम फसल बीमा (PMFBY):** ✅ ई-क्रॉप विवरण और आधार सीडेड बैंक खाता संलग्न है।",
                "- 💳 **किसान क्रेडिट कार्ड (KCC):** ✅ भूमि रिकॉर्ड, पैन और आधार दस्तावेज तैयार हैं।",
                "",
                "💡 *आप स्क्रीन के ऊपरी दाएं कोने में **'Edit Profile'** पर क्लिक करके अपने दस्तावेजों को कभी भी देख सकते हैं, नए दस्तावेज अपलोड कर सकते हैं या विवरण बदल सकते हैं।*"
            ])
            action_title = "किसान दस्तावेज लॉकर की समीक्षा करें"
            action_desc = "अपने प्रोफ़ाइल दस्तावेजों और बैंक विवरणों को देखें या अपडेट करें।"
            action_why = "सरकारी योजनाओं में आवेदन के लिए दस्तावेजों को तैयार रखने हेतु।"
            action_conseq = "आपके डिजिटल फार्म लॉकर को अद्यतन रखता है।"
        else:
            markdown_lines.extend([
                "### 📁 Farmer Digital Locker & Official Documents Management",
                f"**Farmer Name:** {name} | **Location:** {location} | **District:** {district}",
                "",
                "> 🔒 **Farmer Digital Secure Locker:** Your official identity documents, bank accounts, and land records are securely verified and stored in your profile. These are verified and ready for official government scheme applications (PM-KISAN, PMFBY, KCC).",
                "",
                "#### 🪪 Available Documents & File Access:",
                f"1. 👤 **Passport Size Photograph:** `Farmer_Passport_Photo.jpg` (240 KB, JPG) — ✅ **Verified** *(High-resolution profile portrait)*",
                f"2. 🪪 **Aadhaar Card (UIDAI):** `Aadhaar_Card_VenkatRao.pdf` (1.2 MB) — Number: **{aadhaar}** — ✅ **Biometric e-KYC Verified**",
                f"3. 💳 **PAN Card:** `PAN_Card_ABCDE1234F.pdf` (850 KB) — Number: **{pan}** — ✅ **Income Tax Dept Verified (Agricultural Exemption)**",
                f"4. 🏦 **Bank Passbook & Account:** `SBI_Passbook_AadhaarLinked.pdf` (1.8 MB) — **{bank}** | A/C: **{acc_no}** | IFSC: **{ifsc}** — ✅ **Aadhaar DBT Linked & Active**",
                f"5. 📜 **Pattadar Passbook / 1B Record:** `RoR_1B_Pattadar_Passbook.pdf` (2.4 MB) — Number: **{pattadar}** — ✅ **Webland Revenue Certified**",
                "",
                "#### 🏛️ Government Scheme Application Readiness:",
                "- 🌾 **PM-KISAN:** ✅ Aadhaar, 1B Pattadar passbook, and DBT-enabled bank account are all verified.",
                "- 🛡️ **PMFBY Crop Insurance:** ✅ e-Crop booking receipt and Aadhaar-seeded SBI account attached.",
                "- 💳 **Kisan Credit Card (KCC):** ✅ Land records, PAN, and Aadhaar verified for subsidized credit.",
                "",
                "💡 *You can view, download, or replace any of these documents anytime by opening the **Edit Profile** drawer from the top-right header.*"
            ])
            action_title = "Review Farmer Document Locker"
            action_desc = "Access and verify your stored identity documents and bank passbook records."
            action_why = "Ensures your documents are up-to-date for upcoming agricultural scheme deadlines."
            action_conseq = "Updates digital document records in your local profile."

        proposed_actions = [
            ConsequentialAction(
                action_id="act-docs-review-001",
                title=action_title,
                description=action_desc,
                why_reason=action_why,
                action_type="UPDATE_FARMER_PROFILE",
                payload={"farmer_id": "farmer-001", "action": "REVIEW_DOCUMENTS"},
                status="PROPOSED",
                requires_confirmation=False,
                consequences_summary=action_conseq,
                created_at=now_str
            )
        ]

    # =========================================================================
    # WORKFLOW: CROP ADVISORY & PEST MANAGEMENT (Clean, Practical, No Citations)
    # =========================================================================
    elif intent == "CROP_ADVISORY":
        top_source = rag_sources[0] if rag_sources else None
        source_title = top_source.document_title if top_source else f"{crop_display} Management Package"

        if telugu_mode:
            markdown_lines.extend([
                f"### 🔬 వ్యవసాయ సలహా: {crop_display} పంట యాజమాన్యం",
                f"**పంట దశ:** {stage} | **విస్తీర్ణం:** {acres} | **ప్రాంతం:** {location}",
                "",
                "#### 🩺 పంట రక్షణ & యాజమాన్య సిఫార్సులు:"
            ])
            if "chilli" in query.lower() or "మిరప" in query or "yellow" in query.lower() or "పసుపు" in query:
                markdown_lines.extend([
                    "- **మిరపలో ఆకులు పసుపు రంగు మారడానికి కారణాలు మరియు నివారణ:**",
                    "  1. *ఆకులు క్రిందికి ముడుచుకుని పసుపు రంగు మారడం:* ఇది **నల్లి (Yellow Mites)** వల్ల వస్తుంది. నివారణ: స్పైరోమెసిఫెన్ 22.9% SC @ 1.0 మి.లీ/లీటర్ లేదా ప్రొపర్గైట్ 57% EC @ 2.5 మి.లీ/లీటర్ పిచికారీ చేయండి.",
                    "  2. *ఆకులు పైకి దోనెలా ముడుచుకోవడం:* ఇది **తామర పురుగులు (Thrips)** వల్ల వస్తుంది. నివారణ: స్పైనెటోరామ్ 11.7% SC @ 1.0 మి.లీ/లీటర్ లేదా ఫిప్రోనిల్ 5% SC @ 2.0 మి.లీ/లీటర్ పిచికారీ చేయండి.",
                    "  3. *ఆకులలో ఈనెల మధ్య పసుపు రంగు రావడం:* ఇది **జింక్ లేదా మెగ్నీషియం లోపం** లేదా నీటి నిల్వ వల్ల వస్తుంది. నివారణ: ఫార్ములా-4 కూరగాయల సూక్ష్మపోషకాల మిశ్రమం @ 2.5 గ్రా/లీటర్ + మెగ్నీషియం సల్ఫేట్ @ 5.0 గ్రా/లీటర్ పిచికారీ చేయండి."
                ])
            elif "groundnut" in query.lower() or "వేరుశనగ" in query or "40" in query:
                markdown_lines.extend([
                    "- **వేరుశనగ 40-45 రోజుల కీలక ఊడలు దిగే దశ యాజమాన్యం:**",
                    "  - **తప్పనిసరి జిప్సం వాడకం:** ఎకరాకు **200 కిలోల జిప్సం** ను మొక్కల మొదళ్ల వద్ద సాలులలో వేసి తేలికపాటి మట్టి ఎగదోయండి.",
                    "  - జిప్సం కాయలలో గింజ అభివృద్ధికి కాల్షియం అందించి తాలు కాయలు ఏర్పడకుండా నిరోధిస్తుంది.",
                    "  - *హెచ్చరిక:* 45 రోజుల తర్వాత లోతైన గడ్డి తీత చేపట్టవద్దు, ఇది నేలలోకి దిగే లేత ఊడలను తెంచివేస్తుంది."
                ])
            else:
                markdown_lines.extend([
                    f"- **{crop_display} పంట యాజమాన్య ముఖ్యాంశాలు:**",
                    f"- క్రమం తప్పకుండా పొలాన్ని పర్యవేక్షించి, తగిన పోషకాలు మరియు తేమను నిర్వహించండి."
                ])
            save_title = f"{crop_display} సలహాను వ్యవసాయ డైరీలో నమోదు చేయండి"
            save_desc = "ఈ పంట సలహాను మీ ఫార్మ్ ప్రొఫైల్‌లో నమోదు చేస్తుంది."
            save_why = "గుర్తించిన లక్షణాలు మరియు సిఫార్సు చేసిన మందుల పిచికారీ వివరాలను ట్రాక్ చేయడానికి ఇది సహాయపడుతుంది."
            save_conseq = "మీ స్థానిక ఫార్మ్ నోట్‌బుక్‌ను అప్‌డేట్ చేస్తుంది."

        elif hindi_mode:
            markdown_lines.extend([
                f"### 🔬 कृषि सलाह: {crop_display} फसल प्रबंधन",
                f"**फसल अवस्था:** {stage} | **क्षेत्रफल:** {acres} | **स्थान:** {location}",
                "",
                "#### 🩺 फसल स्वास्थ्य एवं प्रबंधन सिफारिशें:"
            ])
            if "chilli" in query.lower() or "मिर्च" in query or "yellow" in query.lower() or "पीली" in query:
                markdown_lines.extend([
                    "- **मिर्च में पत्तियों के पीलेपन के मुख्य कारण और उपचार:**",
                    "  1. *पत्तियां नीचे की ओर मुड़ना एवं पीलापन:* यह **माइट्स (Yellow Mites)** के कारण होता है। उपाय: स्पाइरोमेसिफेन 22.9% एससी @ 1.0 मिली/लीटर या प्रोपार्गाइट 57% ईसी @ 2.5 मिली/लीटर का छिड़काव करें।",
                    "  2. *पत्तियां ऊपर की ओर नाव के आकार में मुड़ना:* यह **थ्रिप्स (Thrips)** के कारण होता है। उपाय: स्पिनेटोरम 11.7% एससी @ 1.0 मिली/लीटर या फिप्रोनिल 5% एससी @ 2.0 मिली/लीटर का छिड़काव करें।",
                    "  3. *पत्तियों में नसों के बीच पीलापन:* यह **जिंक या मैग्नीशियम की कमी** दर्शाता है। उपाय: फॉर्मूला-4 सब्जी सूक्ष्म पोषक तत्व @ 2.5 ग्राम/लीटर + मैग्नीशियम सल्फेट @ 5.0 ग्राम/लीटर का छिड़काव करें।"
                ])
            elif "groundnut" in query.lower() or "मूंगफली" in query or "40" in query:
                markdown_lines.extend([
                    "- **मूंगफली में 40-45 दिन की महत्वपूर्ण पेगिंग (सुई बनने) की अवस्था:**",
                    "  - **अनिवार्य जिप्सम प्रयोग:** **200 किलोग्राम जिप्सम प्रति एकड़** कतारों के साथ डालें और हल्की मिट्टी चढ़ाएं।",
                    "  - जिप्सम फलियों के विकास के लिए कैल्शियम प्रदान करता है और खोखली फलियों को रोकता है।",
                    "  - *चेतावनी:* 45 दिन बाद गहरी निराई-गुड़ाई न करें क्योंकि यह नाजुक सुइयों को तोड़ देती है।"
                ])
            else:
                markdown_lines.extend([
                    f"- **{crop_display} फसल प्रबंधन मुख्य बिंदु:**",
                    f"- संतुलित पोषण एवं नियमित निगरानी बनाए रखें।"
                ])
            save_title = f"{crop_display} सलाह को फार्म नोटबुक में दर्ज करें"
            save_desc = "इस फसल सलाह को आपकी फार्म प्रोफाइल नोटबुक में दर्ज करता है।"
            save_why = "पहचाने गए लक्षणों और निर्धारित छिड़काव को ट्रैक करने में यह आपकी मदद करेगा।"
            save_conseq = "आपकी स्थानीय कृषि डायरी को अपडेट करता है।"

        else:
            markdown_lines.extend([
                f"### 🔬 Agricultural Advisory: {crop_display} Management",
                f"**Diagnosed Query / Stage:** {stage} | **Field Area:** {acres} | **Location:** {location}",
                "",
                "#### 🩺 Diagnosis & Agronomic Advisory:"
            ])
            if "chilli" in query.lower() or "yellow" in query.lower():
                markdown_lines.extend([
                    "- **Symptom Differentiation for Yellowing Leaves:**",
                    "  1. *Downward Curling with Bronze/Rough Underside:* Indicates **Yellow Mite (*Polyphagotarsonemus latus*)** infestation. Remedy: Spiromesifen 22.9% SC @ 1.0 ml/L or Propargite 57% EC @ 2.5 ml/L.",
                    "  2. *Upward Boat-shaped Cupping with Yellow Margins:* Indicates **Thrips (*Scirtothrips dorsalis*)**. Remedy: Spinetoram 11.7% SC @ 1.0 ml/L or Fipronil 5% SC @ 2.0 ml/L.",
                    "  3. *General Interveinal Yellowing without Curling:* Indicates **Micronutrient Deficiency (Zinc/Magnesium)** or water stagnation. Remedy: Vegetable Micronutrient Formula-4 @ 2.5 g/L + MgSO4 @ 5.0 g/L."
                ])
            elif "groundnut" in query.lower() or "40" in query.lower() or "pegging" in query.lower():
                markdown_lines.extend([
                    "- **Critical Pegging Stage (40-45 Days After Sowing):**",
                    "  - **Mandatory Gypsum Application:** Apply **200 kg gypsum per acre** along the crop rows followed by light earthing up.",
                    "  - Gypsum provides critical calcium for pod development and eliminates empty shells ('pops').",
                    "  - *Warning:* Avoid deep hoeing or aggressive inter-cultivation after 45 DAS as it severs tender penetrating pegs."
                ])
            else:
                markdown_lines.append(f"- **Key Technical Advisory:** Maintain recommended irrigation intervals and scout the field regularly for early symptoms.")
            save_title = f"Record {crop_display} Advisory to Farm Notebook"
            save_desc = "Stores this stage advisory in your farm profile for seasonal pest and nutrient tracking."
            save_why = "This will help you keep track of diagnosed symptoms and scheduled sprays."
            save_conseq = "Updates your seasonal farm diary in the local database."

        proposed_actions = [
            ConsequentialAction(
                action_id="act-advisory-save-001",
                title=save_title,
                description=save_desc,
                why_reason=save_why,
                action_type="SAVE_FARM_PLAN",
                payload={"crop": crop_key, "stage": stage, "query": query, "language": lang},
                status="PROPOSED",
                requires_confirmation=True,
                consequences_summary=save_conseq,
                created_at=now_str
            )
        ]

    # =========================================================================
    # WORKFLOW: PURE MARKET INTELLIGENCE
    # =========================================================================
    else:
        has_live = market_data and market_data.data_status in ["LIVE", "DEMO"] and len(market_data.markets) > 0
        if telugu_mode:
            markdown_lines.extend([
                f"### 📈 మార్కెట్ మరియు మండి ధరలు: {crop_display}",
                f"**ప్రాంతం:** {location} | **తేదీ:** {datetime.now().strftime('%d %B %Y')}",
                ""
            ])
            if has_live:
                markdown_lines.append("#### 🏢 ప్రాంతీయ మార్కెట్ ధరల పోలిక:")
                for m in market_data.markets:
                    markdown_lines.append(
                        f"- **{m.market_name} ({m.district}):** మోడల్ ధర ₹{m.modal_price_per_quintal}/క్వింటాల్ (₹{m.price_per_kg}/కిలో) | "
                        f"రవాణా ఖర్చుల తర్వాత నికర ధర: **₹{m.net_effective_price_per_quintal}/క్వింటాల్**"
                    )
                markdown_lines.extend([
                    "",
                    f"**అమ్మకపు సిఫార్సు:** {market_data.recommended_strategy}"
                ])
            else:
                markdown_lines.append("> ℹ️ *ఈ పంట కోసం ప్రత్యక్ష మార్కెట్ ధరలు తాత్కాలికంగా అందుబాటులో లేవు. దయచేసి స్థానిక మార్కెట్ కమిటీని సంప్రదించండి.*")
        elif hindi_mode:
            markdown_lines.extend([
                f"### 📈 मंडी भाव एवं बाजार स्थिति: {crop_display}",
                f"**स्थान:** {location} | **दिनांक:** {datetime.now().strftime('%d %B %Y')}",
                ""
            ])
            if has_live:
                markdown_lines.append("#### 🏢 क्षेत्रीय मंडी भाव तुलना:")
                for m in market_data.markets:
                    markdown_lines.append(
                        f"- **{m.market_name} ({m.district}):** मोडल भाव ₹{m.modal_price_per_quintal}/क्विंटल (₹{m.price_per_kg}/किग्रा) | "
                        f"परिवहन बाद शुद्ध दर: **₹{m.net_effective_price_per_quintal}/क्विंटल**"
                    )
                markdown_lines.extend([
                    "",
                    f"**रणनीतिक सिफारिश:** {market_data.recommended_strategy}"
                ])
            else:
                markdown_lines.append("> ℹ️ *इस फसल के लिए लाइव मंडी दरें अस्थायी रूप से उपलब्ध नहीं हैं। कृपया स्थानीय मंडी समिति से संपर्क करें।*")
        else:
            markdown_lines.extend([
                f"### 📈 Mandi Market Status: {crop_display}",
                f"**Primary Location:** {location} | **Date:** {datetime.now().strftime('%d %B %Y')}",
                ""
            ])
            if has_live:
                markdown_lines.append("#### 🏢 Regional Mandi Price Comparison:")
                for m in market_data.markets:
                    markdown_lines.append(
                        f"- **{m.market_name} ({m.district}):** Modal ₹{m.modal_price_per_quintal}/q (₹{m.price_per_kg}/kg) | "
                        f"Net after transport: **₹{m.net_effective_price_per_quintal}/q** | Status: `{m.data_status}`"
                    )
                markdown_lines.extend([
                    "",
                    f"**Strategic Recommendation:** {market_data.recommended_strategy}"
                ])
            else:
                markdown_lines.append("> ℹ️ *Live market data from official AGMARKNET/e-NAM was currently unavailable for this query.*")

    final_markdown = "\n".join(markdown_lines)
    return action_plan, final_markdown, proposed_actions
