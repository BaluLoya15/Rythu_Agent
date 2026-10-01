# 🌱 RYTHU AGENT (రైతు ఏజెంట్)

> **"An AI-powered action agent for India's farmers and rural communities."**  
> *Category: Agri Tech & Rural Bharat | BharatAgentic Hackathon powered by aiKart*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple.svg)](https://vitejs.dev/)
[![Tests](https://img.shields.io/badge/Tests-9%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-amber.svg)]()

---

## 📌 1. Product Philosophy: Live-First & Strict Data Honesty

Rythu Agent has been architected to address real agricultural challenges with **uncompromising data honesty**:

1. **Natural Farmer Entry Point:** The interface is not a rigid list of canned demo buttons. The farmer enters through natural chat: *"How can I help with your farm today?"* with intuitive suggestion chips.
2. **Live Data by Default:** Live satellite agro-meteorology is fetched directly from **Open-Meteo** with dynamic geocoding.
3. **No Fake Live Data or Silent Fallbacks:** When querying official market portals (AGMARKNET / e-NAM), if the live gateway returns no records or is unreachable, the agent **never silently injects fake prices**. It transparently marks market data as `UNAVAILABLE`, explains the source status, and continues using verified agronomy and live weather.
4. **Verified University Grounding:** Agricultural advice is grounded in published research manuals from **ANGRAU** (Acharya N.G. Ranga Agricultural University) and **ICAR** with exact document, section, and page citations.
5. **Human-in-the-Loop Safeguard:** The agent never executes consequential actions automatically. Safe internal actions (such as saving cultivation plans to the farm profile) require explicit farmer confirmation.

---

## 🏗️ 2. Autonomous Agentic Workflow

```
Farmer Natural Language Request
             ↓
     [Intent Analysis]
             ↓
[Farmer Context Extraction (Acreage, Crop, Location)]
             ↓
   [Dynamic Task Planning]
             ↓
    [Tool Selection & Dispatch]
     ├── Live Weather Tool (Open-Meteo Satellite Feed & Geocoding)
     ├── Official Market Tool (AGMARKNET / e-NAM Live Gateway)
     ├── Agricultural RAG (ANGRAU / ICAR Research Extension Guides)
     └── Services Tool (Central & State Government Schemes)
             ↓
  [Real-Time Execution Tracing (Latency & Exact Status)]
             ↓
[Multi-Source Reasoning & Synthesis Engine]
             ↓
 ┌──────────────────────────────────────────┐
 │       TODAY'S FARM ACTION PLAN           │
 │  🌱 Crop & Growth Stage Summary          │
 │  📍 Location & Field Context             │
 │  🌦 Live Agro-Met Weather & Spray Window │
 │  📊 Mandi Status (Live or Honest Notice) │
 │  ⚠️ Critical Considerations & Risks      │
 │  ✅ Prioritized Recommended Actions      │
 │  📅 Next Monitoring Tasks                │
 │  📚 ANGRAU / ICAR Source Grounding       │
 └──────────────────────────────────────────┘
             ↓
[Human Confirmation Gate for Consequential Actions]
             ↓
 [Persistence into SQLite Farm Notebook]
```

---

## 🔍 3. Data Provenance Standards

Every data point retrieved by Rythu Agent carries a strict provenance classification:

| Provenance Tag | Source | Verification |
| :--- | :--- | :--- |
| `LIVE` | Open-Meteo Live API, AGMARKNET Live Feed | Real-time network request with current timestamp and geocoding |
| `VERIFIED_RESEARCH` | ANGRAU & ICAR Extension Manuals | Peer-reviewed agricultural research manuals with page numbers |
| `VERIFIED_KNOWLEDGE` | Ministry of Agriculture Portals | Official central & AP government scheme documentation |
| `LOCAL_KNOWLEDGE` | Farmer Profile (SQLite DB) | Landholding, soil type, irrigation setup, and stage diary |
| `UNAVAILABLE` | External Live Gateway Timeout | Transparent disclosure when an official API is unreachable |

---

## 🛠️ 4. The Four Core Capabilities

### 1. Crop Advisory (Tool: `rag_tool`)
- Grounded in official **ANGRAU** and **ICAR** extension bulletins for **Tomato, Chilli, Groundnut, and Rice**.
- Precise diagnosis for complex symptoms (e.g. Mite vs Thrips vs Zinc chlorosis in chilli).
- Cites exact document titles, sections, page numbers, and repository IDs. Zero hallucinations.

### 2. Market Intelligence (Tool: `market_tool`)
- Queries official **AGMARKNET / data.gov.in / e-NAM** live gateways.
- When live data is returned: computes transport costs and **Net Effective Realization**.
- When live data is unreachable: **strictly discloses UNAVAILABLE** without fabricating fake numbers, advising physical APMC confirmation.

### 3. Agricultural Planning (Reasoning Engine)
- Synthesizes live weather conditions with stage-specific cultural tasks into prioritized action cards.
- Advises on chemical safety windows (e.g., maximum wind speed thresholds of 15 km/h to prevent spray drift).

### 4. Access to Services (Tool: `services_tool`)
- Curated database of verified central and state schemes: **PM-KISAN, PMFBY Free Crop Insurance, PMKSY (90% Drip Subsidy), SMAM Mechanization, and Soil Health Cards**.
- Uses conservative, non-definitive language: *"Based on the available criteria, you may qualify if..."* with required document checklists and official portals.

---

## 🚀 5. Installation & Quick Start

### Prerequisites
- Python 3.11 or 3.12
- Node.js v18+ and npm

### Step 1: Clone & Configure
```bash
git clone https://github.com/your-username/Rythuagent.git
cd Rythuagent

cp .env.example .env
```

### Step 2: Set Up Backend
```bash
uv venv backend/.venv --python 3.11
backend\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

### Step 3: Run Backend Tests
```bash
python -m pytest backend/tests/test_agent.py -v
```
*(All 9 test suites pass: Live Open-Meteo, Market honesty, RAG citations, Schemes, Profiles, and Live execution)*

### Step 4: Start Backend Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend runs on: `http://127.0.0.1:8000` (Health check at `http://127.0.0.1:8000/api/health`)*

### Step 5: Start Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend opens at: `http://localhost:5173`*

---

## 🧪 6. Natural Queries & Verification

Start the application at `http://localhost:5173`. Type naturally into the chat:

### Query 1: Tomato Cultivation & Market Check
> **Query:** *"I have 2 acres of tomato near Vijayawada. What should I do this week and where should I check for better market prices?"*
- **Live Output:**
  1. Profile context loaded: Venkat Rao, 2.0 Acres, Vijayawada, Tomato at flowering/fruit set.
  2. Live weather queried via Open-Meteo satellite feed (temperature, humidity, calm evening spray window).
  3. Official market tool queries AGMARKNET/e-NAM gateway (honest disclosure if live feed is unavailable).
  4. RAG tool retrieves ANGRAU guidance (Boron 20% + Calcium Nitrate foliar spray to prevent blossom end rot).
  5. Action Card proposed: *"Save 7-Day Cultivation & Cultural Plan to Farm Profile"*.
  6. Click **Confirm & Execute** $\rightarrow$ Safely logs plan to SQLite!

### Query 2: Government Schemes & Welfare Access
> **Query:** *"What agricultural government services may be relevant to me?"*
- **Live Output:** Matches PM-KISAN, PMFBY, and PMKSY 90% Drip Subsidy with clear document checklists and official portals.

*(Note: An internal Developer & Automated Testing Harness is accessible via the "Dev / Test Mode" button in the header for automated regression testing and offline mock verification).*

---

## 📊 7. BharatAgentic Hackathon Compliance Matrix

| Requirement | Satisfied in Rythu Agent | Verification |
| :--- | :--- | :--- |
| **A. Research & Gather Info** | Live Open-Meteo satellite feed, AGMARKNET gateways, ANGRAU RAG | [`backend/tools/weather.py`](file:///backend/tools/weather.py) |
| **B. Understand & Classify** | Multi-intent classification and entity extraction | [`backend/agent/planner.py`](file:///backend/agent/planner.py) |
| **C. Decision-Making** | Net transportation modeling & live agro-met spray risk assessment | [`backend/agent/synthesizer.py`](file:///backend/agent/synthesizer.py) |
| **D. Chat Interface** | Modern React chat with Markdown & natural action confirmation | [`frontend/src/components/ChatPanel.jsx`](file:///frontend/src/components/ChatPanel.jsx) |
| **E. Multi-Step Workflows** | Dynamic sequential planning and tool execution | [`backend/agent/orchestrator.py`](file:///backend/agent/orchestrator.py) |
| **F. External APIs & DB** | REST API, SQLite persistence, Open-Meteo live integration | [`backend/main.py`](file:///backend/main.py) |
| **G. Document Analysis** | Ingested ANGRAU & ICAR research manuals with page citations | [`backend/rag/documents.py`](file:///backend/rag/documents.py) |
| **H. Tool Coordination** | Coordinates 5 specialized tools with real latency logging | [`frontend/src/components/AgentTracePanel.jsx`](file:///frontend/src/components/AgentTracePanel.jsx) |
| **I. Actionable Results** | Card-based Farm Action Plan with prioritized steps | [`frontend/src/components/ActionPlanView.jsx`](file:///frontend/src/components/ActionPlanView.jsx) |
| **J. Human Confirmation** | Consequential actions require explicit farmer approval | [`POST /api/action/confirm`](file:///backend/main.py#L108) |

---

## 📄 8. License

Released under the **MIT License** for the BharatAgentic Hackathon powered by aiKart.
