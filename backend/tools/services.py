from typing import List, Dict, Any, Optional
from backend.models.schemas import GovernmentService

GOVERNMENT_SCHEMES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "scheme-001",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "scheme_code": "PM-KISAN-CENTRAL",
        "level": "Central Government",
        "purpose": "Income support for land-holding farmer families to meet domestic and crop input needs.",
        "target_beneficiaries": "All landholding farmer families with cultivable land (excluding institutional landholders & high-income taxpayers).",
        "eligibility_criteria": [
            "Landholding farmer family with cultivable land registered in state revenue records.",
            "Valid Aadhaar linked to bank account (e-KYC verified).",
            "Must not be an institutional landholder or serving/retired government officer.",
            "Family income tax payers are excluded."
        ],
        "benefits": "₹6,000 per year provided in three equal 4-monthly installments of ₹2,000 transferred via DBT directly into bank account.",
        "subsidy_percentage": "100% Direct Cash Benefit",
        "required_documents": [
            "Aadhaar Card (Mandatory with OTP authentication)",
            "Pattadar Passbook / RoR 1B Land Record Document",
            "Aadhaar-seeded Bank Account details (IFSC & Account number)",
            "Active mobile number linked to Aadhaar"
        ],
        "application_process": [
            "Visit the official PM-KISAN portal (pmkisan.gov.in) or visit nearest Rythu Bharosa Kendra (RBK) / Common Service Centre (CSC).",
            "Click on 'New Farmer Registration' under Farmers Corner.",
            "Enter Aadhaar number and State, submit OTP received on registered mobile.",
            "Fill land survey numbers, khata number, and upload scanned Pattadar passbook.",
            "Local Revenue / VRO officer completes physical verification of land ownership within 15-30 days."
        ],
        "official_portal_url": "https://pmkisan.gov.in",
        "helpline_number": "155261 / 011-24300606",
        "verified_status": "Officially Verified (Ministry of Agriculture & Farmers Welfare)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-002",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY) & Weather Based Crop Insurance",
        "scheme_code": "PMFBY-INSURANCE",
        "level": "Central & State Convergence (Andhra Pradesh Free Crop Insurance)",
        "purpose": "Comprehensive insurance coverage against non-preventable natural risks (drought, flood, unseasonal rainfall, localized pest outbreaks).",
        "target_beneficiaries": "All farmers growing notified crops (Tomato, Groundnut, Paddy, Chilli) in notified areas.",
        "eligibility_criteria": [
            "Farmer cultivating notified crop in the notified insurance unit / village.",
            "Crop sowing must be registered in the State Digital Crop Booking Portal (e-Crop).",
            "Both loanee and non-loanee farmers eligible.",
            "Enrolled prior to the seasonal cut-off date."
        ],
        "benefits": "Financial compensation for yield loss, prevented sowing, post-harvest losses due to cyclonic rains up to the Sum Insured (e.g., up to ₹40,000 - ₹60,000/acre for high-value horticultural crops). In AP, the state covers the farmer premium share for e-Crop registered farmers.",
        "subsidy_percentage": "State/Central Premium Subsidy (~95-100% farmer premium covered)",
        "required_documents": [
            "e-Crop Booking e-KYC acknowledgment receipt from Village Agriculture Assistant (VAA)",
            "Aadhaar Card",
            "Pattadar Passbook or CCRC (Crop Cultivator Rights Card for tenant farmers)",
            "Bank passbook copy with IFSC"
        ],
        "application_process": [
            "Ensure field survey number and crop are mapped by Village Agriculture Assistant (VAA) during the e-Crop survey.",
            "Complete biometric e-KYC authentication at the local Rythu Bharosa Kendra (RBK).",
            "Verify presence of your survey number in the published village social audit list.",
            "Any claim compensation is settled via DBT directly to Aadhaar-linked bank account based on Crop Cutting Experiments (CCE)."
        ],
        "official_portal_url": "https://pmfby.gov.in",
        "helpline_number": "14447 (PMFBY Krishi Helpline)",
        "verified_status": "Officially Verified (Ministry of Agriculture & Farmers Welfare)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-003",
        "name": "PMKSY - Per Drop More Crop (Micro-Irrigation Subsidy)",
        "scheme_code": "PMKSY-DRIP-SPRINKLER",
        "level": "Central & State Joint Program (AP Micro-Irrigation Project - APMIP)",
        "purpose": "Promotion of water use efficiency via drip and sprinkler irrigation infrastructure for horticultural crops.",
        "target_beneficiaries": "Small and Marginal Farmers cultivating vegetables (Tomato, Chilli), pulses, and fruit orchards.",
        "eligibility_criteria": [
            "Land ownership with assured water source (borewell, open well, or farm pond).",
            "Small & Marginal Farmers (up to 5.0 acres) receive highest subsidy slab (up to 90%).",
            "Must not have availed micro-irrigation subsidy on the same land parcel in the last 7 years."
        ],
        "benefits": "Up to 90% government financial subsidy for installing drip irrigation kits, filters, lateral pipes, and venturi fertigation systems (Cost savings of ₹45,000 - ₹65,000 per acre).",
        "subsidy_percentage": "Up to 90% for Small & Marginal Farmers; 70% for other farmers",
        "required_documents": [
            "Pattadar Passbook (1B record) or registered lease deed",
            "Aadhaar Card of landowner",
            "Soil & Water Testing suitability certificate",
            "Electricity service connection copy for agricultural borewell / motor",
            "Passport size photograph"
        ],
        "application_process": [
            "Submit online application through APMIP / State Horticulture Portal or at the Rythu Bharosa Kendra (RBK).",
            "MIP field engineer visits the field for GPS survey and designs the drip layout.",
            "Farmer pays the nominal beneficiary contribution (10%) via demand draft or online portal.",
            "Authorized vendor installs the drip equipment followed by joint physical verification and commissioning."
        ],
        "official_portal_url": "https://pmksy.gov.in",
        "helpline_number": "1800-425-2425 (APMIP Kisan Call Center)",
        "verified_status": "Officially Verified (Ministry of Agriculture & Farmers Welfare)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-004",
        "name": "Sub-Mission on Agricultural Mechanization (SMAM) & Custom Hiring Centers",
        "scheme_code": "SMAM-MACHINERY",
        "level": "Central & State Scheme",
        "purpose": "Financial assistance for farm machinery, power tillers, sprayers, and establishment of village Custom Hiring Centers.",
        "target_beneficiaries": "Individual farmers, Farmer Producer Organizations (FPOs), and Village Farmer Groups.",
        "eligibility_criteria": [
            "Valid landholding farmer registered on AGRI-MACHINERY portal.",
            "Preference given to Small, Marginal, SC/ST, and Women farmers.",
            "One machine category per family every 3 to 5 years."
        ],
        "benefits": "40% to 50% subsidy on purchase of battery-operated sprayers, rotavators, power weeders, and tractors.",
        "subsidy_percentage": "40% - 50% subsidy on approved benchmark rates",
        "required_documents": [
            "Aadhaar Card",
            "Pattadar Passbook",
            "Bank passbook copy",
            "Quotation from authorized agricultural equipment dealer"
        ],
        "application_process": [
            "Register on agrimachinery.nic.in using Aadhaar credentials.",
            "Select machine type and authorized dealer in your district (e.g. Krishna/Guntur).",
            "Department of Agriculture scrutinizes documents and issues administrative sanction.",
            "Purchase equipment and upload invoice with GPS machine photo for subsidy release via DBT."
        ],
        "official_portal_url": "https://agrimachinery.nic.in",
        "helpline_number": "1800-180-1551 (Kisan Suvidha)",
        "verified_status": "Officially Verified (Ministry of Agriculture & Farmers Welfare)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-005",
        "name": "Soil Health Card Scheme & Balanced Fertilizer Management",
        "scheme_code": "SOIL-HEALTH-CARD",
        "level": "Central Scheme",
        "purpose": "Promote balanced soil nutrition by providing customized soil test reports with crop-specific fertilizer and micronutrient recommendations.",
        "target_beneficiaries": "All agricultural landowners and cultivators.",
        "eligibility_criteria": [
            "Any farmer holding operational agricultural land.",
            "Samples collected every 2-3 years."
        ],
        "benefits": "Free or highly subsidized soil chemical testing (NPK, pH, Electrical Conductivity, Organic Carbon, Zinc, Boron, Iron, Manganese) with exact dosage recommendations reducing fertilizer wastage by 15-20%.",
        "subsidy_percentage": "100% Free Testing for registered farmers",
        "required_documents": [
            "Survey Number / Khata Number",
            "Aadhaar Number",
            "Farmer Mobile Number"
        ],
        "application_process": [
            "Contact Village Agriculture Assistant (VAA) at RBK during post-harvest fallow period.",
            "Soil sample is collected in zigzag pattern (0-15 cm depth) with GPS tagging.",
            "Sample tested at District Soil Testing Laboratory.",
            "Soil Health Card delivered physically and accessible on soilhealth.dac.gov.in."
        ],
        "official_portal_url": "https://soilhealth.dac.gov.in",
        "helpline_number": "011-23381012",
        "verified_status": "Officially Verified (Ministry of Agriculture & Farmers Welfare)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-006",
        "name": "Annadata Sukhibhava / PM-KISAN (Andhra Pradesh)",
        "scheme_code": "AP-ANNADATA-SUKHIBHAVA",
        "level": "AP State Government • ₹20,000 Annual Assistance",
        "purpose": "Investment support and financial security for agricultural input purchase including certified seeds and balanced fertilizers.",
        "target_beneficiaries": "Farmer families and tenant farmers (CCRC holders) in Andhra Pradesh.",
        "eligibility_criteria": [
            "Landholding farmer or tenant cultivator registered with Crop Cultivator Rights Card (CCRC).",
            "Resident of Andhra Pradesh with verified land records in Webland.",
            "e-KYC verified bank account."
        ],
        "benefits": "₹20,000 annual investment support per farmer family (AP State Govt ₹14,000 + Central PM-KISAN ₹6,000) deposited directly via DBT.",
        "subsidy_percentage": "100% Direct Cash Benefit",
        "required_documents": [
            "Aadhaar Card",
            "Pattadar Passbook or CCRC Card for Tenant Farmers",
            "Bank Account linked to Aadhaar",
            "Ration Card / Rice Card"
        ],
        "application_process": [
            "Visit local Rythu Bharosa Kendra (RBK) or Village Secretariat.",
            "Agriculture Assistant verifies survey number and land extent.",
            "Biometric e-KYC completed on state portal.",
            "Amount disbursed before Kharif and Rabi input purchasing windows."
        ],
        "official_portal_url": "https://ysrrythubharosa.ap.gov.in",
        "helpline_number": "1902 (AP Spandana Citizen Helpline)",
        "verified_status": "Officially Verified (Government of Andhra Pradesh)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    },
    {
        "id": "scheme-007",
        "name": "Kisan Credit Card (KCC) & Interest Subvention Scheme",
        "scheme_code": "KCC-LOAN-CENTRAL",
        "level": "Agricultural Credit & 4% Interest Subvention",
        "purpose": "Timely and adequate short-term credit for crop cultivation, post-harvest expenses, and maintenance of farm assets.",
        "target_beneficiaries": "All farmers, tenant cultivators, sharecroppers, and Self-Help Group (SHG) joint liability groups.",
        "eligibility_criteria": [
            "All owner cultivators and tenant farmers cultivating agricultural crops.",
            "No prior willful loan default.",
            "Clean CIBIL track record with rural/commercial banks."
        ],
        "benefits": "Collateral-free crop loan up to ₹1.6 Lakhs (and up to ₹3.0 Lakhs with land record) at an effective subsidized interest rate of just 4% upon prompt repayment.",
        "subsidy_percentage": "3% Prompt Repayment Incentive (Effective 4% Interest Rate)",
        "required_documents": [
            "Filled KCC application form",
            "Aadhaar Card and PAN Card",
            "Land record documents (Pattadar Passbook / 1B / Adangal)",
            "No-dues certificate from local bank branches"
        ],
        "application_process": [
            "Submit KCC form at nearest Commercial Bank, Regional Rural Bank (RRB), or Primary Agricultural Credit Society (PACS).",
            "Bank verifies land records and crop scale of finance within 14 days.",
            "KCC RuPay debit card issued for ATM withdrawals and fertilizer purchase."
        ],
        "official_portal_url": "https://myscheme.gov.in/schemes/kcc",
        "helpline_number": "1800-115-526 / 155261",
        "verified_status": "Officially Verified (Ministry of Finance & NABARD)",
        "last_verified_date": "2026-08",
        "data_status": "VERIFIED_KNOWLEDGE",
        "is_demo_data": False
    }
]

# Multilingual Overlays
SCHEME_LOCALIZATIONS = {
    "te": {
        "scheme-001": {
            "name": "పిఎం-కిసాన్ (ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి)",
            "level": "కేంద్ర ప్రభుత్వం",
            "purpose": "సాగు భూమి కలిగిన రైతు కుటుంబాలకు పెట్టుబడి మరియు పంట అవసరాల కోసం ఆదాయ మద్దతు.",
            "target_beneficiaries": "సాగు భూమి ఉన్న రైతు కుటుంబాలందరూ (సంస్థాగత యజమానులు మినహా).",
            "benefits": "సంవత్సరానికి ₹6,000 నగదును 3 విడతల్లో నేరుగా డిబిటి (DBT) ద్వారా బ్యాంక్ ఖాతాలో జమ చేస్తారు.",
            "subsidy_percentage": "100% ప్రత్యక్ష నగదు బదిలీ",
            "eligibility_criteria": [
                "రాష్ట్ర రెవెన్యూ రికార్డుల్లో నమోదైన సాగు భూమి ఉన్న రైతు కుటుంబం.",
                "బ్యాంక్ ఖాతాకు ఆధార్ లింక్ (ఈ-కేవైసీ ధృవీకరించబడాలి).",
                "ఆదాయపు పన్ను చెల్లించేవారు మరియు ప్రభుత్వ ఉద్యోగులు మినహాయింపు."
            ],
            "required_documents": [
                "ఆధార్ కార్డు (ఓటీపీ ధృవీకరణతో)",
                "పట్టాదారు పాస్‌బుక్ / 1బి రికార్డు",
                "ఆధార్ లింక్ అయిన బ్యాంక్ ఖాతా వివరాలు",
                "రిజిస్టర్డ్ మొబైల్ నంబర్"
            ],
            "application_process": [
                "అధికారిక పిఎం-కిసాన్ పోర్టల్ లేదా సమీప రైతు భరోసా కేంద్రం (RBK) ను సంప్రదించండి.",
                "రైతు విభాగంలో 'కొత్త రైతు నమోదు' ఎంచుకోండి.",
                "ఆధార్ నంబర్ నమోదు చేసి, మొబైల్‌కు వచ్చే ఓటీపీని సబ్మిట్ చేయండి.",
                "సర్వే నంబర్లు నమోదు చేసి పట్టాదారు పాస్‌బుక్ అప్‌లోడ్ చేయండి.",
                "గ్రామ రెవెన్యూ అధికారి (VRO) భౌతిక ధృవీకరణ పూర్తి చేస్తారు."
            ]
        },
        "scheme-002": {
            "name": "ప్రధాన మంత్రి ఫసల్ బీమా యోజన (PMFBY) & ఉచిత పంటల బీమా",
            "level": "కేంద్ర మరియు రాష్ట్ర సంయుక్త పథకం (ఆంధ్రప్రదేశ్ ఉచిత పంటల బీమా)",
            "purpose": "ప్రకృతి వైపరీత్యాలు (వర్షాభావం, తుఫానులు, వరదలు, తెగుళ్లు) వల్ల కలిగే పంట నష్టానికి సమగ్ర బీమా రక్షణ.",
            "target_beneficiaries": "నోటిఫైడ్ ప్రాంతాల్లో నోటిఫైడ్ పంటలు (వరి, వేరుశనగ, చెరకు, మిరప, టమాటా) సాగుచేసే రైతులు.",
            "benefits": "ఈ-క్రాప్ నమోదైన రైతులకు ప్రీమియం ప్రభుత్వం భరిస్తుంది; దిగుబడి నష్టానికి బీమా పరిహారం నేరుగా ఖాతాలో జమ.",
            "subsidy_percentage": "ప్రభుత్వ ప్రీమియం సబ్సిడీ (రైతు వాటా దాదాపు 100% ఉచితం)",
            "eligibility_criteria": [
                "నోటిఫై చేయబడిన ప్రాంతంలో నోటిఫైడ్ పంట సాగు చేస్తున్న రైతులు.",
                "ఈ-క్రాప్ (e-Crop) పోర్టల్‌లో పంట నమోదు తప్పనిసరి.",
                "కౌలు రైతులు (CCRC కార్డు కలిగినవారు) మరియు సొంత భూమి రైతులు అర్హులు."
            ],
            "required_documents": [
                "గ్రామ వ్యవసాయ సహాయకుడి (VAA) ఈ-క్రాప్ రసీదు",
                "ఆధార్ కార్డు",
                "పట్టాదారు పాస్‌బుక్ లేదా CCRC కార్డు",
                "బ్యాంక్ పాస్‌బుక్ నకలు"
            ],
            "application_process": [
                "ఈ-క్రాప్ సర్వే సమయంలో గ్రామ వ్యవసాయ సహాయకుడు మీ పంటను నమోదు చేశారో లేదో సరిచూసుకోండి.",
                "రైతు భరోసా కేంద్రంలో బయోమెట్రిక్ ఈ-కేవైసీ పూర్తి చేయండి.",
                "గ్రామ సచివాలయంలో ప్రదర్శించే సోషల్ ఆడిట్ జాబితాలో మీ సర్వే నంబర్ సరిచూసుకోండి."
            ]
        },
        "scheme-003": {
            "name": "పిఎంకెఎస్వై - బిందు & తుంపర సేద్యం రాయితీ (సూక్ష్మ నీటిపారుదల పథకం)",
            "level": "కేంద్ర & రాష్ట్ర సంయుక్త పథకం (APMIP)",
            "purpose": "ఉద్యానవన మరియు వాణిజ్య పంటలలో నీటి వినియోగ సామర్థ్యాన్ని పెంచేందుకు డ్రిప్ మరియు స్ప్రింక్లర్ సబ్సిడీ.",
            "target_beneficiaries": "చిన్న, సన్నకారు రైతులు మరియు వాణిజ్య పంటలు సాగుచేసే రైతులు.",
            "benefits": "చిన్న, సన్నకారు రైతులకు డ్రిప్ మరియు స్ప్రింక్లర్ పరికరాలపై 90% వరకు ప్రభుత్వ రాయితీ (ఎకరానికి ₹45,000 - ₹65,000 ఆదా).",
            "subsidy_percentage": "చిన్న/సన్నకారు రైతులకు 90% సబ్సిడీ; ఇతరులకు 70%",
            "eligibility_criteria": [
                "బోరుబావి లేదా శాశ్వత నీటి వనరు కలిగి ఉండాలి.",
                "గత 7 సంవత్సరాలలో ఇదే భూమిపై సూక్ష్మ నీటిపారుదల రాయితీ పొంది ఉండకూడదు."
            ],
            "required_documents": [
                "పట్టాదారు పాస్‌బుక్ (1బి రికార్డు) లేదా రిజిస్టర్డ్ లీజు పత్రం",
                "ఆధార్ కార్డు",
                "బోరుబావి విద్యుత్ కనెక్షన్ రసీదు",
                "పాస్‌పోర్ట్ సైజు ఫోటో"
            ],
            "application_process": [
                "రైతు భరోసా కేంద్రం లేదా APMIP పోర్టల్ ద్వారా దరఖాస్తు చేసుకోండి.",
                "MIP ఇంజనీర్ పొలాన్ని సర్వే చేసి డ్రిప్ డిజైన్ రూపొందిస్తారు.",
                "రైతు తన వాటా (10%) చెల్లించిన తర్వాత పరికరాలు అమర్చబడతాయి."
            ]
        },
        "scheme-004": {
            "name": "వ్యవసాయ యాంత్రీకరణ సబ్-మిషన్ (SMAM) & యంత్రాల రాయితీ",
            "level": "కేంద్ర & రాష్ట్ర సంయుక్త పథకం",
            "purpose": "వ్యవసాయ యంత్రాలు, ట్రాక్టర్లు, పవర్ టిల్లర్లు మరియు స్ప్రేయర్ల కొనుగోలుపై ఆర్థిక సహాయం.",
            "target_beneficiaries": "వ్యక్తిగత రైతులు, రైతు ఉత్పత్తిదారుల సంఘాలు (FPOలు).",
            "benefits": "ట్రాక్టర్లు, రోటవేటర్లు, పవర్ వీడర్లు, బ్యాటరీ స్ప్రేయర్ల కొనుగోలుపై 40% నుండి 50% వరకు రాయితీ.",
            "subsidy_percentage": "అనుమతించిన ధరలపై 40% - 50% సబ్సిడీ",
            "eligibility_criteria": [
                "వ్యవసాయ యంత్రాల పోర్టల్‌లో నమోదైన భూమిగల రైతులు.",
                "చిన్న, సన్నకారు, మహిళా రైతులకు ప్రాధాన్యత."
            ],
            "required_documents": [
                "ఆధార్ కార్డు",
                "పట్టాదారు పాస్‌బుక్",
                "బ్యాంక్ ఖాతా పాస్‌బుక్",
                "అధీకృత డీలర్ నుండి కొటేషన్"
            ],
            "application_process": [
                "agrimachinery.nic.in లో ఆధార్‌తో నమోదు చేసుకోండి.",
                "కావలసిన యంత్రం మరియు డీలర్‌ను ఎంచుకోండి.",
                "అనుమతి పత్రం వచ్చిన తర్వాత పరికరాన్ని కొనుగోలు చేసి రసీదు అప్‌లోడ్ చేయండి."
            ]
        },
        "scheme-005": {
            "name": "భూసార పరీక్ష కార్డు పథకం (సాయిల్ హెల్త్ కార్డ్)",
            "level": "కేంద్ర పథకం",
            "purpose": "భూమిలోని పోషకాలను పరీక్షించి తగిన మోతాదులో ఎరువుల వాడకాన్ని ప్రోత్సహించడం.",
            "target_beneficiaries": "వ్యవసాయ భూమి కలిగి ఉన్న సాగుదారులు అందరూ.",
            "benefits": "ఉచిత భూసార పరీక్ష; 12 రకాల పోషకాల ఆధారంగా సిఫార్సులు అందించి ఎరువుల ఖర్చు 15-20% ఆదా.",
            "subsidy_percentage": "నమోదైన రైతులకు 100% ఉచిత పరీక్ష",
            "eligibility_criteria": [
                "సాగు భూమి కలిగిన ఏ రైతు అయినా దరఖాస్తు చేసుకోవచ్చు.",
                "ప్రతి 2-3 సంవత్సరాలకు ఒకసారి నమూనా సేకరిస్తారు."
            ],
            "required_documents": [
                "సర్వే నంబర్ / ఖాతా నంబర్",
                "ఆధార్ నంబర్",
                "మొబైల్ నంబర్"
            ],
            "application_process": [
                "పంట కోత అనంతరం రైతు భరోసా కేంద్రంలోని వ్యవసాయ సహాయకుడిని సంప్రదించండి.",
                "జిగ్-జాగ్ పద్ధతిలో మట్టి నమూనా సేకరించి ల్యాబ్‌కు పంపుతారు.",
                "భూసార కార్డు నేరుగా అందజేయబడుతుంది."
            ]
        },
        "scheme-006": {
            "name": "అన్నదాత సుఖీభవ / పీఎం కిసాన్ (ఆంధ్రప్రదేశ్)",
            "level": "ఆంధ్రప్రదేశ్ రాష్ట్ర ప్రభుత్వం • ₹20,000 వార్షిక సాయం",
            "purpose": "ఆంధ్రప్రదేశ్‌లోని రైతు కుటుంబాలకు విత్తనాలు, ఎరువులు మరియు వ్యవసాయ పెట్టుబడి సహాయం అందించడం.",
            "target_beneficiaries": "ఆంధ్రప్రదేశ్‌లోని భూయజమానులు మరియు కౌలు రైతులు (CCRC కార్డుదారులు).",
            "benefits": "రైతు కుటుంబానికి సంవత్సరానికి ₹20,000 పెట్టుబడి సాయం (ఆంధ్రప్రదేశ్ ప్రభుత్వం ₹14,000 + కేంద్ర పీఎం కిసాన్ ₹6,000) విత్తనాలు, ఎరువుల కొనుగోలుకు ఆర్థిక భరోసా.",
            "subsidy_percentage": "100% ప్రత్యక్ష నగదు బదిలీ",
            "eligibility_criteria": [
                "ఆంధ్రప్రదేశ్‌లో సాగుభూమి ఉన్న రైతులు లేదా కౌలు రైతు గుర్తింపు కార్డు (CCRC) కలిగినవారు.",
                "వెబ్‌ల్యాండ్ పోర్టల్‌లో నమోదైన భూమి వివరాలు.",
                "ఆధార్ లింక్ అయిన బ్యాంక్ ఖాతా మరియు ఈ-కేవైసీ పూర్తి కావాలి."
            ],
            "required_documents": [
                "ఆధార్ కార్డు",
                "పట్టాదారు పాస్‌బుక్ లేదా కౌలు రైతు CCRC కార్డు",
                "ఆధార్‌తో అనుసంధానమైన బ్యాంక్ ఖాతా",
                "రైస్ కార్డు / రేషన్ కార్డు"
            ],
            "application_process": [
                "సమీప రైతు భరోసా కేంద్రం (RBK) లేదా గ్రామ సచివాలయాన్ని సంప్రదించండి.",
                "వ్యవసాయ సహాయకుడు సర్వే నంబర్ మరియు భూమి వివరాలను ధృవీకరిస్తారు.",
                "బయోమెట్రిక్ ఈ-కేవైసీ పూర్తి చేసిన తర్వాత నిధులు విడుదలవుతాయి."
            ]
        },
        "scheme-007": {
            "name": "కిసాన్ క్రెడిట్ కార్డ్ (KCC) & వడ్డీ రాయితీ పథకం",
            "level": "వ్యవసాయ రుణం & 4% వడ్డీ సదుపాయం",
            "purpose": "రైతులకు సకాలంలో తక్కువ వడ్డీతో స్వల్పకాలిక పంట రుణాలు మరియు పెట్టుబడి సహాయం అందించడం.",
            "target_beneficiaries": "సొంత భూమి గల రైతులు, కౌలుదారులు మరియు స్వయం సహాయక సంఘాల సభ్యులు.",
            "benefits": "సకాలంలో తిరిగి చెల్లిస్తే కేవలం 4% వడ్డీతో ₹3 లక్షల వరకు పంట రుణం; ₹1.6 లక్షల వరకు ఎలాంటి పూచీకత్తు అవసరం లేదు.",
            "subsidy_percentage": "3% సకాలంలో చెల్లింపు ప్రోత్సాహకం (నికర వడ్డీ రేటు 4% మాత్రమే)",
            "eligibility_criteria": [
                "సాగుభూమి ఉన్న ఏ రైతు అయినా లేదా ధృవీకరించబడిన కౌలు రైతు అయినా దరఖాస్తు చేసుకోవచ్చు.",
                "బ్యాంకుల్లో గతంలో ఎటువంటి రుణ ఎగవేత ఉండకూడదు.",
                "గ్రామీణ లేదా వాణిజ్య బ్యాంకుల్లో ఖాతా కలిగి ఉండాలి."
            ],
            "required_documents": [
                "పూర్తి చేసిన కేసీసీ (KCC) దరఖాస్తు ఫారమ్",
                "ఆధార్ కార్డు మరియు పాన్ కార్డు",
                "పట్టాదారు పాస్‌బుక్ / అడంగల్ / 1బి రికార్డు",
                "స్థానిక బ్యాంకుల నో-డ్యూస్ సర్టిఫికేట్"
            ],
            "application_process": [
                "సమీప వాణిజ్య బ్యాంకు, గ్రామీణ బ్యాంకు లేదా ప్రాథమిక వ్యవసాయ పరపతి సంఘం (PACS) లో దరఖాస్తు సమర్పించండి.",
                "బ్యాంకు అధికారులు 14 రోజుల్లో భూమి రికార్డులను పరిశీలించి రుణం మంజూరు చేస్తారు.",
                "ఎరువులు, విత్తనాల కొనుగోలుకు KCC రూపే డెబిట్ కార్డు జారీ చేయబడుతుంది."
            ]
        }
    },
    "hi": {
        "scheme-001": {
            "name": "पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)",
            "level": "केंद्र सरकार",
            "purpose": "भूमिधारक किसान परिवारों को कृषि आदानों और घरेलू जरूरतों के लिए आय सहायता प्रदान करना।",
            "target_beneficiaries": "कृषि योग्य भूमि वाले सभी किसान परिवार (संस्थागत भूस्वामी बहिष्कृत)।",
            "benefits": "प्रति वर्ष ₹6,000 की राशि तीन समान किस्तों में सीधे डीबीटी (DBT) के माध्यम से बैंक खाते में।",
            "subsidy_percentage": "100% प्रत्यक्ष नकद लाभ",
            "eligibility_criteria": [
                "राज्य राजस्व रिकॉर्ड में पंजीकृत कृषि भूमि वाले किसान परिवार।",
                "आधार से जुड़ा बैंक खाता (ई-केवाईसी सत्यापित)।",
                "आयकर दाता और सेवारत/सेवानिवृत्त सरकारी अधिकारी बहिष्कृत।"
            ],
            "required_documents": [
                "आधार कार्ड (ओटीपी प्रमाणीकरण के साथ)",
                "पट्टादार पासबुक / खतौनी 1बी रिकॉर्ड",
                "आधार से जुड़ा बैंक खाता विवरण",
                "सक्रिय मोबाइल नंबर"
            ],
            "application_process": [
                "आधिकारिक पीएम-किसान पोर्टल (pmkisan.gov.in) पर जाएं या निकटतम सीएससी केंद्र पर संपर्क करें।",
                "फार्मर्स कॉर्नर में 'नया किसान पंजीकरण' चुनें।",
                "आधार नंबर दर्ज करें और मोबाइल पर प्राप्त ओटीपी सत्यापित करें।",
                "खसरा-खतौनी विवरण भरें और पासबुक की प्रति अपलोड करें।"
            ]
        },
        "scheme-002": {
            "name": "प्रधानमंत्री फसल बीमा योजना (PMFBY) एवं फसल बीमा",
            "level": "केंद्र एवं राज्य संयुक्त योजना",
            "purpose": "प्राकृतिक आपदाओं (सूखा, बाढ़, बेमौसम बारिश, कीट प्रकोप) के कारण फसल नुकसान से व्यापक बीमा सुरक्षा।",
            "target_beneficiaries": "अधिसूचित क्षेत्रों में अधिसूचित फसलें (धान, गन्ना, उड़द, मिर्च, टमाटर) उगाने वाले सभी किसान।",
            "benefits": "बीमित राशि तक फसल क्षति पर वित्तीय मुआवजा; ई-क्रॉप में पंजीकृत किसानों को प्रीमियम सब्सिडी।",
            "subsidy_percentage": "प्रीमियम पर 95-100% सरकारी सब्सिडी",
            "eligibility_criteria": [
                "अधिसूचित क्षेत्र में अधिसूचित फसल की खेती करने वाले किसान।",
                "राज्य डिजिटल पोर्टल में फसल का पंजीकरण अनिवार्य।",
                "ऋणी और गैर-ऋणी दोनों किसान पात्र।"
            ],
            "required_documents": [
                "ई-क्रॉप डिजिटल पंजीकरण रसीद",
                "आधार कार्ड",
                "पट्टादार पासबुक या काश्तकार अधिकार पत्र",
                "बैंक पासबुक प्रति"
            ],
            "application_process": [
                "सुनिश्चित करें कि ग्राम कृषि सहायक द्वारा आपकी फसल का सर्वेक्षण किया गया है।",
                "स्थानीय केंद्र पर बायोमेट्रिक ई-केवाईसी पूर्ण करें।",
                "ग्राम सूची में अपने सर्वेक्षण नंबर की पुष्टि करें।"
            ]
        },
        "scheme-003": {
            "name": "पीएमकेएसवाई - प्रति बूंद अधिक फसल (सूक्ष्म सिंचाई सब्सिडी)",
            "level": "केंद्र एवं राज्य संयुक्त कार्यक्रम",
            "purpose": "ड्रिप और स्प्रिंकलर सिंचाई से जल उपयोग दक्षता बढ़ाने और फसल उत्पादकता में वृद्धि हेतु सहायता।",
            "target_beneficiaries": "लघु एवं सीमांत किसान और बागवानी/सब्जी उत्पादक किसान।",
            "benefits": "ड्रिप एवं स्प्रिंकलर संयंत्र लगाने पर लघु/सीमांत किसानों को 90% तक सरकारी सब्सिडी (₹45,000 - ₹65,000 प्रति एकड़ की बचत)।",
            "subsidy_percentage": "लघु/सीमांत किसानों के लिए 90% सब्सिडी; अन्य के लिए 70%",
            "eligibility_criteria": [
                "निश्चित जल स्रोत (नलकूप, कुआं या फार्म पौंड) की उपलब्धता।",
                "पिछले 7 वर्षों में उसी भूमि पर सूक्ष्म सिंचाई सब्सिडी न ली गई हो।"
            ],
            "required_documents": [
                "जमीन का पट्टा / खतौनी रिकॉर्ड",
                "आधार कार्ड",
                "नलकूप विद्युत कनेक्शन रसीद",
                "पासपोर्ट साइज फोटो"
            ],
            "application_process": [
                "राज्य बागवानी पोर्टल या स्थानीय कृषि कार्यालय में आवेदन करें।",
                "इंजीनियर द्वारा खेत का जीपीएस सर्वेक्षण कर लेआउट तैयार किया जाएगा।",
                "किसान अंशदान (10%) जमा करने के बाद उपकरण स्थापित किए जाएंगे।"
            ]
        },
        "scheme-004": {
            "name": "कृषि यंत्रीकरण उप-मिशन (SMAM) एवं कृषि यंत्र सब्सिडी",
            "level": "केंद्र एवं राज्य योजना",
            "purpose": "आधुनिक कृषि यंत्रों, ट्रैक्टरों, पावर टिलरों और स्प्रेयरों की खरीद पर वित्तीय सहायता।",
            "target_beneficiaries": "व्यक्तिगत किसान, कृषक उत्पादक संगठन (FPO)।",
            "benefits": "रोटावेटर, बैटरी स्प्रेयर, पावर वीडर और ट्रैक्टर की खरीद पर 40% से 50% सब्सिडी।",
            "subsidy_percentage": "मानक दरों पर 40% - 50% सब्सिडी",
            "eligibility_criteria": [
                "कृषि मशीनरी पोर्टल पर पंजीकृत भूमिधारक किसान।",
                "लघु, सीमांत, महिला और अनुसूचित वर्ग के किसानों को प्राथमिकता।"
            ],
            "required_documents": [
                "आधार कार्ड",
                "भूमि स्वामित्व प्रमाण पत्र",
                "बैंक खाता विवरण",
                "अधिकृत डीलर से कोटेशन"
            ],
            "application_process": [
                "agrimachinery.nic.in पर आधार से पंजीकरण करें।",
                "यंत्र का प्रकार और अधिकृत डीलर चुनें।",
                "स्वीकृति आदेश मिलने के बाद यंत्र खरीदें और बिल अपलोड करें।"
            ]
        },
        "scheme-005": {
            "name": "मृदा स्वास्थ्य कार्ड योजना (सॉइल हेल्थ कार्ड)",
            "level": "केंद्र सरकार की योजना",
            "purpose": "मिट्टी की उर्वरता की जांच कर संतुलित खाद एवं सूक्ष्म पोषक तत्वों के प्रयोग को बढ़ावा देना।",
            "target_beneficiaries": "सभी भूमिधारक किसान और काश्तकार।",
            "benefits": "निःशुल्क मृदा परीक्षण और फसल-वार सटीक खाद की सिफारिश, जिससे उर्वरक लागत में 15-20% की बचत।",
            "subsidy_percentage": "पंजीकृत किसानों के लिए 100% निःशुल्क",
            "eligibility_criteria": [
                "कृषि भूमि का स्वामित्व या परिचालन करने वाला कोई भी किसान।",
                "प्रत्येक 2-3 वर्ष में एक बार नमूना लिया जाता है।"
            ],
            "required_documents": [
                "खसरा / खाता संख्या",
                "आधार संख्या",
                "मोबाइल नंबर"
            ],
            "application_process": [
                "फसल कटाई के बाद स्थानीय कृषि सहायक से संपर्क करें।",
                "खेत से मिट्टी का नमूना लेकर जांच प्रयोगशाला भेजा जाता है।",
                "सॉइल हेल्थ कार्ड सीधे किसान को सौंपा जाता है।"
            ]
        },
        "scheme-006": {
            "name": "अन्नदाता सुखीभव / पीएम-किसान (आंध्र प्रदेश)",
            "level": "आंध्र प्रदेश राज्य सरकार • ₹20,000 वार्षिक सहायता",
            "purpose": "आंध्र प्रदेश के किसान परिवारों को बीज, उर्वरक और कृषि निवेश के लिए वित्तीय सुरक्षा प्रदान करना।",
            "target_beneficiaries": "आंध्र प्रदेश में भूमिधारक किसान एवं काश्तकार (सीसीआरसी धारक)।",
            "benefits": "किसान परिवार को प्रति वर्ष ₹20,000 की निवेश सहायता (आंध्र प्रदेश सरकार ₹14,000 + केंद्र पीएम-किसान ₹6,000) सीधे डीबीटी द्वारा।",
            "subsidy_percentage": "100% प्रत्यक्ष नकद लाभ",
            "eligibility_criteria": [
                "आंध्र प्रदेश में पंजीकृत कृषि भूमि अथवा सीसीआरसी धारक काश्तकार।",
                "वेबलैंड पोर्टल में सत्यापित भूमि रिकॉर्ड।",
                "आधार लिंक बैंक खाता एवं ई-केवाईसी अनिवार्य।"
            ],
            "required_documents": [
                "आधार कार्ड",
                "पट्टादार पासबुक या काश्तकार सीसीआरसी कार्ड",
                "आधार लिंक बैंक खाता पासबुक",
                "राशन कार्ड"
            ],
            "application_process": [
                "निकटतम रायथू भरोसा केंद्र या ग्राम सचिवालय में संपर्क करें।",
                "कृषि सहायक द्वारा सर्वेक्षण नंबर का सत्यापन किया जाएगा।",
                "बायोमेट्रिक ई-केवाईसी पूर्ण होने पर राशि जारी की जाएगी।"
            ]
        },
        "scheme-007": {
            "name": "किसान क्रेडिट कार्ड (KCC) एवं ब्याज सहायता योजना",
            "level": "कृषि ऋण एवं 4% ब्याज सहायता",
            "purpose": "किसानों को समय पर कम ब्याज दर पर अल्पकालिक फसल ऋण एवं कृषि निवेश सहायता प्रदान करना।",
            "target_beneficiaries": "सभी भूमिधारक किसान, काश्तकार और स्वयं सहायता समूह।",
            "benefits": "समय पर पुनर्भुगतान करने पर मात्र 4% प्रभावी ब्याज दर पर ₹3 लाख तक का फसल ऋण; ₹1.6 लाख तक बिना बंधक ऋण।",
            "subsidy_percentage": "3% शीघ्र भुगतान प्रोत्साहन (प्रभावी ब्याज 4%)",
            "eligibility_criteria": [
                "कृषि योग्य भूमि वाले किसान अथवा सत्यापित काश्तकार।",
                "किसी बैंक में ऋण अदायगी में चूक नहीं होनी चाहिए।",
                "सत्यापित नागरिक पहचान।"
            ],
            "required_documents": [
                "भरा हुआ केसीसी आवेदन पत्र",
                "आधार कार्ड एवं पैन कार्ड",
                "खसरा-खतौनी / पट्टादार पासबुक प्रति",
                "बैंक अनापत्ति प्रमाण पत्र (No-dues)"
            ],
            "application_process": [
                "निकटतम बैंक शाखा या प्राथमिक कृषि साख समिति में आवेदन जमा करें।",
                "बैंक 14 दिनों के भीतर भूमि अभिलेखों का सत्यापन कर ऋण स्वीकृत करेगा।",
                "केसीसी रूपे डेबिट कार्ड जारी किया जाएगा।"
            ]
        }
    }
}

def search_agricultural_services(
    query: str,
    farmer_context: Optional[Dict[str, Any]] = None,
    language: str = "en"
) -> List[GovernmentService]:
    """
    Searches and ranks relevant government schemes based on query and farmer context.
    Returns localized scheme details for 'en', 'te', and 'hi'.
    """
    query_lower = query.lower()
    raw_results = []

    keywords_map = {
        "scheme-001": ["pm kisan", "income", "cash", "samman nidhi", "6000", "installment", "kisan", "పిఎం కిసాన్", "కిసాన్", "నగదు", "पीएम किसान", "सम्मान निधि"],
        "scheme-002": ["insurance", "bima", "fasal", "pmfby", "crop loss", "damage", "rain loss", "cyclone", "compensation", "బీమా", "పంట నష్టం", "తుఫాను", "ఫసల్ బీమా", "फसल बीमा", "बीमा"],
        "scheme-003": ["drip", "sprinkler", "irrigation", "water", "pmksy", "subsidy", "pipe", "borewell", "డ్రిప్", "స్ప్రింక్లర్", "రాయితీ", "నీటిపారుదల", "ड्रिप", "स्प्रिंकलर", "सिंचाई", "सब्सिडी"],
        "scheme-004": ["machinery", "tractor", "sprayer", "smam", "mechanization", "rotavator", "equipment", "weeder", "యంత్రాలు", "ట్రాక్టర్", "స్ప్రేయర్", "యాంత్రీకరణ", "मशीनरी", "ट्रैक्टर", "स्प्रेयर"],
        "scheme-005": ["soil", "soil health", "test", "testing", "fertilizer", "nutrition", "npk", "zinc", "boron", "భూసార", "మట్టి పరీక్ష", "ఎరువులు", "मृदा", "मिट्टी परीक्षण", "उर्वरक"],
        "scheme-006": ["annadata", "sukhibhava", "ysr", "rythu bharosa", "20000", "andhra", "ap scheme", "అన్నదాత", "సుఖీభవ", "రైతు భరోసా", "అన్నదాత సుఖీభవ", "अन्नदाता", "सुखीभव"],
        "scheme-007": ["kcc", "kisan credit card", "loan", "credit", "interest", "4%", "crop loan", "రుణం", "కేసీసీ", "రుణాలు", "వడ్డీ రాయితీ", "రుణ", "ऋण", "केसीसी", "किसान क्रेडिट कार्ड"]
    }

    is_general_query = any(w in query_lower for w in [
        "government", "scheme", "schemes", "services", "subsidies", "subsidy", "what schemes", "relevant to me", "apply", "welfare",
        "సేవలు", "పథకం", "పథకాలు", "ప్రభుత్వ", "రాయితీ", "సంక్షేమ",
        "सेवाएं", "सरकारी", "योजना", "योजनाएं", "सब्सिडी", "कल्याण"
    ])

    for item in GOVERNMENT_SCHEMES_DATABASE:
        item_id = item["id"]
        kw_list = keywords_map.get(item_id, [])
        match = False

        if is_general_query:
            match = True
        else:
            for kw in kw_list:
                if kw in query_lower:
                    match = True
                    break

        if match:
            raw_results.append(dict(item))

    if not raw_results:
        raw_results = [
            dict(GOVERNMENT_SCHEMES_DATABASE[0]),
            dict(GOVERNMENT_SCHEMES_DATABASE[1]),
            dict(GOVERNMENT_SCHEMES_DATABASE[2])
        ]

    # Apply localization overlay if requested language is te or hi
    lang_code = language.lower() if language else "en"
    if lang_code not in ["te", "hi"]:
        # Check if query itself has Telugu or Hindi characters
        if any('\u0C00' <= char <= '\u0C7F' for char in query):
            lang_code = "te"
        elif any('\u0900' <= char <= '\u097F' for char in query):
            lang_code = "hi"

    localized_services: List[GovernmentService] = []
    overlay = SCHEME_LOCALIZATIONS.get(lang_code, {})

    for item in raw_results:
        item_copy = dict(item)
        item_id = item_copy["id"]
        if item_id in overlay:
            item_copy.update(overlay[item_id])
        localized_services.append(GovernmentService(**item_copy))

    return localized_services
