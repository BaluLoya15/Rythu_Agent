"""
Authoritative Agricultural Knowledge Documents for Rythu Agent.
Source: ANGRAU (Acharya N.G. Ranga Agricultural University), ICAR, and Krishi Vigyan Kendra (KVK).
Grounding: Andhra Pradesh & South India agro-climatic zones.
Crops Supported:
- Primary: Paddy, Sugarcane, Black Gram
- Secondary: Tomato, Chilli, Groundnut
"""

from typing import List, Dict, Any

AGRICULTURAL_DOCUMENTS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # PRIMARY CROP 1: PADDY / RICE
    # -------------------------------------------------------------
    {
        "doc_id": "doc-ric-001",
        "crop": "Paddy",
        "title": "ICAR-Indian Institute of Rice Research: Comprehensive Paddy Management",
        "organization": "ICAR-IIRR Hyderabad / ANGRAU Maruteru",
        "section": "Panicle Initiation & Stem Borer / Blast Integrated Protocol",
        "page": 78,
        "reference": "IIRR Rice Tech Bulletin 2024-R01",
        "keywords": ["paddy", "rice", "vari", "వరి", "వరి పంట", "ధాన్", "धान", "चावल", "panicle initiation", "stem borer", "కాండం తొలుచు పురుగు", "dead heart", "white earhead", "blast", "అగ్గి తెగులు", "water management"],
        "content": (
            "At Panicle Initiation (PI) stage (50-65 days after transplanting in medium-duration varieties like BPT-5204): "
            "Apply the last top dressing of Nitrogen (25% of total N) along with Potassium (MOP @ 20 kg/acre). "
            "Maintain 2-3 cm standing water; avoid drying the field during panicle development. "
            "For yellow stem borer monitoring: If dead hearts or egg masses exceed ETL (1 egg mass/sq.m), "
            "broadcast Cartap Hydrochloride 4% G @ 8 kg/acre or spray Chlorantraniliprole 18.5% SC @ 0.3 ml/liter. "
            "For neck blast prevention: Prophylactic spray of Tricyclazole 75% WP @ 0.6 g/liter at 5% panicle emergence."
        )
    },
    {
        "doc_id": "doc-ric-002",
        "crop": "Paddy",
        "title": "ANGRAU Package of Practices: High-Yielding Rice Production (Coastal & Delta Zones)",
        "organization": "ANGRAU Agricultural Research Station, Maruteru",
        "section": "Water Management & Brown Plant Hopper (BPH) Alley Formation",
        "page": 32,
        "reference": "ANGRAU Rice Bulletin AP-PADDY-2024",
        "keywords": ["paddy", "rice", "వరి", "వరి పంట", "ధాన్", "धान", "चावल", "bph", "brown plant hopper", "సుడిదోమ", "alley formation", "పాయలు తీయడం", "water draining", "sheath blight", "పాము పొడ తెగులు"],
        "content": (
            "Water management and pest control at active tillering to booting stage: "
            "Practice alternate wetting and drying (AWD) to strengthen root anchorage and suppress Brown Plant Hopper (BPH). "
            "Form 'alleys' (skipping one row every 2 meters in north-south orientation) to facilitate aeration and direct sunlight penetration. "
            "For BPH management: Avoid synthetic pyrethroids. Drain excess standing water for 48 hours and spray Pymetrozine 50% WDG @ 0.6 g/liter "
            "or Triflumezopyrim 10% SC @ 0.4 ml/liter directing the spray nozzle strictly at the base of the rice hills."
        )
    },

    # -------------------------------------------------------------
    # PRIMARY CROP 2: SUGARCANE
    # -------------------------------------------------------------
    {
        "doc_id": "doc-sug-001",
        "crop": "Sugarcane",
        "title": "ANGRAU Sugarcane Production Guide (Coastal Andhra & Krishna Delta)",
        "organization": "ANGRAU Regional Agricultural Research Station (RARS), Anakapalle",
        "section": "Grand Growth Stage (90-120 Days): Earthing-up, Trash Mulching & Moisture Management",
        "page": 41,
        "reference": "RARS Anakapalle Sugarcane Tech Manual SC-2024",
        "keywords": ["sugarcane", "cheruku", "చెరకు", "చెరుకు", "గన్నా", "गन्ना", "grand growth", "trash mulching", "చెరకు చెత్త ఆచ్ఛాదన", "earthing up", "మట్టి ఎగదోయడం", "internode borer", "కణుపు తొలుచు పురుగు", "anakapalle"],
        "content": (
            "Sugarcane during the grand growth stage (90-120 days after planting) requires mandatory cultural operations: "
            "1. Trash Mulching: Spread dried cane trash uniformly @ 3 tonnes/acre in furrows. This reduces weed growth by 60%, "
            "conserves soil moisture by 30%, and lowers soil temperature during hot weather. "
            "2. Final Earthing-Up: Complete final earthing-up by 120 days along with the last top-dressing of Nitrogen (75 kg Urea/acre) "
            "and Muriate of Potash (MOP @ 50 kg/acre). This converts ridges into furrows and prevents crop lodging during coastal winds. "
            "3. Borer Defense: For internode borer, de-trash lower dry leaves and release egg parasitoid Trichogramma chilonis @ 2.5 cc/acre."
        )
    },
    {
        "doc_id": "doc-sug-002",
        "crop": "Sugarcane",
        "title": "ICAR-Sugarcane Breeding Institute: Disease & Nutrient Management",
        "organization": "ICAR-SBI Coimbatore / RARS Anakapalle",
        "section": "Red Rot & Smut Prevention Protocols and Drip Fertigation",
        "page": 56,
        "reference": "ICAR-SBI Production Bulletin SB-2024",
        "keywords": ["sugarcane", "చెరకు", "గన్నా", "गन्ना", "red rot", "ఎర్ర కుళ్లు తెగులు", "लाल सड़न", "smut", "కాటుక తెగులు", "drip fertigation", "బిందు సేద్యం", "micronutrient", "iron chlorosis"],
        "content": (
            "Disease management and fertigation in standing sugarcane: "
            "Inspect clumps for early red rot symptoms (discoloration of 3rd and 4th leaves from top with central white spots on red lesions). "
            "Uproot and burn diseased clumps immediately; drench the spot with Copper Oxychloride 50% WP @ 3.0 g/liter. "
            "For drip fertigated cane: Inject water-soluble fertilizers in 10-day cycles (equal parts N and K) up to 180 days. "
            "If iron chlorosis occurs in calcareous black soils, apply Ferrous Sulphate @ 5.0 g/liter + Citric Acid @ 1.0 g/liter foliar spray twice."
        )
    },

    # -------------------------------------------------------------
    # PRIMARY CROP 3: BLACK GRAM (MINUMULU / URAD)
    # -------------------------------------------------------------
    {
        "doc_id": "doc-bgr-001",
        "crop": "Black Gram",
        "title": "ANGRAU Pulses Production Manual: Black Gram (Urad) in Rice Fallows & Kharif",
        "organization": "ANGRAU Regional Agricultural Research Station, Lam, Guntur",
        "section": "Vegetative to Flowering Stage: Yellow Mosaic Virus & Foliar Nutrition",
        "page": 22,
        "reference": "RARS Lam Pulses Bulletin BG-2024-01",
        "keywords": ["black gram", "urad", "minumulu", "మినుములు", "మినుము", "ఉద్ది", "उड़द", "काली उड़द", "pulses", "yellow mosaic virus", "పల్లా తెగులు", "పీला मोज़ेक", "whitefly", "తెల్లదోమ", "19-19-19", "pod borer", "కాయ తొలుచు పురుగు", "guntur", "krishna"],
        "content": (
            "Black Gram (Urad) management at 25-45 days stage (vegetative to early flowering): "
            "1. Yellow Mosaic Virus (YMV) Watch: YMV causes irregular bright yellow patches on leaves and is transmitted by whiteflies. "
            "Install yellow sticky traps @ 10-12 traps/acre. Spray Acetamiprid 20% SP @ 0.2 g/liter or Thiamethoxam 25% WG @ 0.3 g/liter "
            "at the first sign of whitefly nymphs on leaf undersides. "
            "2. Foliar Nutrition for Pod Setting: Spray water-soluble 19:19:19 (NPK) @ 5.0 g/liter or 2% DAP (dissolved and filtered) "
            "at peak flowering (30-35 DAS) and pod initiation (45 DAS). This prevents flower drop and enhances pod filling by 20-25%. "
            "3. Pod Borer: Spray Spinosad 45% SC @ 0.3 ml/liter if Maruca or Helicoverpa caterpillar entry holes are noticed on pods."
        )
    },

    # -------------------------------------------------------------
    # SECONDARY CROP 1: TOMATO
    # -------------------------------------------------------------
    {
        "doc_id": "doc-tom-001",
        "crop": "Tomato",
        "title": "ANGRAU Package of Practices: Commercial Tomato Cultivation (Krishna & Guntur Districts)",
        "organization": "ANGRAU / ICAR-IIHR Bangalore",
        "section": "Stage 3: Flowering and Early Fruit Set Management (40-60 Days)",
        "page": 28,
        "reference": "ANGRAU Extension Bulletin 2024, Pub No. AP-AGRI-TOM-P03",
        "keywords": ["tomato", "tamata", "టమాటా", "టమాట", "टमाटर", "flowering", "పూత దశ", "fruit set", "boron", "calcium", "blossom end rot", "మాడు తెగులు", "irrigation", "నీటి యాజమాన్యం", "vijayawada", "guntur"],
        "content": (
            "During the flowering and early fruit development stage (40-55 days after transplanting), "
            "tomato crops require stable soil moisture. Fluctuating water stress followed by heavy watering "
            "causes severe flower drop and blossom end rot. Recommended practice: Maintain uniform drip irrigation "
            "(2.5 to 3.5 liters per plant daily in semi-arid zones like Vijayawada/Guntur). "
            "Foliar spray of Solubor (Boron 20%) @ 1.0 g/liter combined with Calcium Nitrate @ 2.5 g/liter "
            "at 10-day intervals enhances fruit setting by 22% and prevents blossom end rot. "
            "Avoid excessive nitrogenous fertilizer application during peak bloom as it triggers vegetative flush "
            "at the expense of fruit initiation."
        )
    },
    {
        "doc_id": "doc-tom-002",
        "crop": "Tomato",
        "title": "ICAR-IIHR Integrated Pest and Disease Management in Solanaceous Vegetables",
        "organization": "ICAR-National Bureau of Agricultural Insect Resources",
        "section": "Tomato Pinworm (Tuta absoluta) and Fruit Borer (Helicoverpa armigera) Protocol",
        "page": 44,
        "reference": "ICAR Technical Bulletin TB-2023-TOM-IPM",
        "keywords": ["tomato", "టమాటా", "टमाटर", "tuta absoluta", "fruit borer", "కాయ తొలుచు పురుగు", "फल छेदक", "leaf miner", "ఆకు తొలిచే పురుగు", "spray", "పిచికారీ", "छिड़काव", "pest management", "neem oil"],
        "content": (
            "Pest management during fruit development: Monitor for Tuta absoluta (pinworm) mines in leaves and pinholes "
            "under fruit calyx. Install delta pheromone traps @ 12-16 traps/acre for mass trapping and monitoring. "
            "If pest incidence is below economic threshold (ETL < 5% damage), apply Azadirachtin (Neem oil 10,000 ppm) "
            "@ 2 ml/liter with sticky adjuvant. For established fruit borer (Helicoverpa armigera) infestations exceeding ETL, "
            "recommended bio-rational spray: Chlorantraniliprole 18.5% SC @ 0.3 ml/liter (or Flubendiamide 39.35% SC @ 0.25 ml/liter). "
            "Safety advisory: Strictly adhere to a 3-day waiting period (Pre-Harvest Interval) before picking fruits. "
            "Spray strictly during late evening hours (after 4:30 PM) to preserve natural pollinator activity."
        )
    },

    # -------------------------------------------------------------
    # SECONDARY CROP 2: CHILLI
    # -------------------------------------------------------------
    {
        "doc_id": "doc-chi-001",
        "crop": "Chilli",
        "title": "Chilli Advisory for Guntur, Krishna & Warangal Belts",
        "organization": "ANGRAU Lam Farm, Guntur / Spices Board of India",
        "section": "Diagnosis and Remediation of Yellowing and Leaf Curl Syndrome",
        "page": 16,
        "reference": "Lam Farm Guntur Advisory CHL-2024-YEL",
        "keywords": ["chilli", "mirchi", "మిరప", "మిర్చి", "मिर्च", "yellow leaves", "పసుపు ఆకులు", "पीली पत्तियां", "leaf curl", "ఆకు ముడత", "पर्ण कुंचन", "thrips", "తామర పురుగులు", "थ्रिप्स", "mites", "నల్లి", "మైట్స్", "micronutrients", "సూక్ష్మపోషకాలు", "guntur", "krishna"],
        "content": (
            "Yellow leaves in chilli can stem from three distinct causal factors: "
            "1. Downward leaf curling with yellowing: Caused by Yellow Mites (Polyphagotarsonemus latus). Undersides of leaves turn bronzed/rough. "
            "Remedy: Spray Spiromesifen 22.9% SC @ 1.0 ml/liter or Propargite 57% EC @ 2.5 ml/liter. "
            "2. Upward cupping / boat-shaped curling with yellow margins: Caused by Thrips (Scirtothrips dorsalis or Black Thrips). "
            "Remedy: Spinetoram 11.7% SC @ 1.0 ml/liter or Fipronil 5% SC @ 2.0 ml/liter. "
            "3. General interveinal yellowing without curling: Indicates Zinc/Magnesium deficiency or water stagnation. "
            "Remedy: Spray Formula-4 vegetable micronutrient mixture @ 2.5 g/liter + Magnesium Sulphate @ 5.0 g/liter. "
            "Always inspect leaf undersides with a hand lens to distinguish mite webbing from nutrient chlorosis before spraying."
        )
    },

    # -------------------------------------------------------------
    # SECONDARY CROP 3: GROUNDNUT
    # -------------------------------------------------------------
    {
        "doc_id": "doc-gnd-001",
        "crop": "Groundnut",
        "title": "ANGRAU Groundnut Production Manual (Rayalaseema & Coastal AP)",
        "organization": "ANGRAU Regional Agricultural Research Station, Tirupati",
        "section": "Critical Pegging Stage: Gypsum Application (40-45 Days After Sowing)",
        "page": 35,
        "reference": "RARS Tirupati Groundnut Advisory Bul. 2024-02",
        "keywords": ["groundnut", "verusanaga", "వేరుశనగ", "వేరుశెనగ", "పల్లీ", "मूंगफली", "pegging", "ఊడలు దిగే దశ", "सुई बनने की अवस्था", "40 days", "40 రోజులు", "40 दिन", "gypsum", "జిప్సం", "जिप्सम", "calcium", "కాల్షియం", "pod filling", "earthing up"],
        "content": (
            "The 40 to 45 days after sowing (DAS) stage in groundnut marks the critical peg penetration and early pod formation phase. "
            "Gypsum application at 40-45 DAS is mandatory for shell calcification and preventing 'pops' (empty pods). "
            "Recommended dose: Apply 200 kg gypsum per acre directly along the crop rows followed by light earthing up. "
            "Soil moisture must be adequate during gypsum application for calcium translocation into the developing pod zone. "
            "Avoid deep inter-cultivation or hoeing after 45 DAS as it severs fragile penetrating pegs, directly depressing pod yield by up to 30%."
        )
    },

    # -------------------------------------------------------------
    # GENERAL AGROMET & SPRAY SAFETY
    # -------------------------------------------------------------
    {
        "doc_id": "doc-gen-001",
        "crop": "General",
        "title": "ICAR Agromet Advisory Service & Chemical Safety Manual",
        "organization": "India Meteorological Department (IMD) - Agrimet / ICAR",
        "section": "Weather-Based Agricultural Operations & Pesticide Drift Minimization",
        "page": 12,
        "reference": "IMD-ICAR Integrated Agromet Guidelines 2024",
        "keywords": ["weather", "వాతావరణం", "मौसम", "spray window", "పిచికారీ సమయం", "छिड़काव", "rain", "వర్షం", "बारिश", "wind speed", "గాలి వేగం", "temperature", "ఉష్ణోగ్రత", "तापमान", "drift", "safety", "రక్షణ"],
        "content": (
            "Meteorological safety protocol for agricultural spray operations: "
            "1. Wind Speed: Do not spray when wind velocity exceeds 15 km/h to prevent severe spray drift and off-target damage. "
            "2. Rain Probability: Avoid applying systemic fungicides/insecticides if rain probability exceeds 50% within 4 hours of spraying, "
            "as chemical wash-off nullifies efficacy and causes environmental leaching. "
            "3. Temperature & Humidity: High ambient temperatures (> 34°C) cause rapid evaporation of droplets and scorching of foliage. "
            "Optimum window: Early morning (6:30 AM to 9:30 AM) or late afternoon (4:00 PM to 6:30 PM). "
            "Always wear protective masks, gloves, and rinse spray tanks away from open water channels."
        )
    }
]
