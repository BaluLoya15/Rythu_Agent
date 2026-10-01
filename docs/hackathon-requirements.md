# BharatAgentic Hackathon - Compliance & Requirements Traceability Matrix

> **Project Name:** RYTHU AGENT  
> **Tagline:** "An AI-powered action agent for India's farmers and rural communities."  
> **Category:** AGRI TECH & RURAL BHARAT

This document details the exact mapping of every BharatAgentic Hackathon evaluation criterion and system requirement to the working code implementation in **Rythu Agent**.

---

## 1. Hackathon Core Requirements (A through J)

| ID | Hackathon Requirement | Working Implementation in Rythu Agent | Source Code Reference |
| :--- | :--- | :--- | :--- |
| **A** | **Research & Gather Information** | RAG retrieval from ANGRAU & ICAR manuals, APMC Mandi database, and Open-Meteo weather satellite feeds. | [`backend/rag/retriever.py`](file:///backend/rag/retriever.py)<br>[`backend/tools/market.py`](file:///backend/tools/market.py) |
| **B** | **Understand, Classify & Prioritize Requests** | Dynamic intent classifier detects `HYBRID_PLANNING_AND_MARKET`, `SERVICES_AND_GOVERNMENT_SCHEMES`, `CROP_ADVISORY`, and `MARKET_INTELLIGENCE`, parsing crop, acreage, and location. | [`backend/agent/planner.py`](file:///backend/agent/planner.py#L38-L120) |
| **C** | **Make Decisions Using Rules, Context & Data** | Computes net effective realization after transport; assesses spray risk against rain probability thresholds; matches farmer acreage against small/marginal subsidy slabs. | [`backend/agent/synthesizer.py`](file:///backend/agent/synthesizer.py#L30-L160) |
| **D** | **Communicate Through a Chat Interface** | Clean, responsive React chat UI supporting Markdown formatting, inline action cards, follow-up chips, and audio indicator. | [`frontend/src/components/ChatPanel.jsx`](file:///frontend/src/components/ChatPanel.jsx) |
| **E** | **Automate Multi-Step Workflows** | Orchestrates sequential pipelines: Profile extraction $\rightarrow$ Mandi comparison $\rightarrow$ Agromet forecast $\rightarrow$ RAG query $\rightarrow$ Multi-source synthesis. | [`backend/agent/orchestrator.py`](file:///backend/agent/orchestrator.py#L40-L190) |
| **F** | **Connect with APIs, Databases & External Tools** | FastAPI REST endpoints, SQLite database for farmer profiles and audit logs, Open-Meteo API, APMC datasets. | [`backend/main.py`](file:///backend/main.py)<br>[`backend/db/database.py`](file:///backend/db/database.py) |
| **G** | **Analyze Documents & Datasets** | Ingests and semantic-indexes ANGRAU extension bulletins, ICAR pest protocols, and APMC arrival registers. | [`backend/rag/documents.py`](file:///backend/rag/documents.py) |
| **H** | **Coordinate Specialized Tools** | Orchestrates 5 specialized tools (`farmer_tool`, `market_tool`, `weather_tool`, `rag_tool`, `services_tool`) with real execution durations. | [`backend/agent/orchestrator.py`](file:///backend/agent/orchestrator.py#L80-L165) |
| **I** | **Generate Actionable Recommendations** | Produces "Today's Farm Action Plan" containing prioritized action cards (Step 1, 2, 3), harvest maturity tips, and monitoring tasks. | [`frontend/src/components/ActionPlanView.jsx`](file:///frontend/src/components/ActionPlanView.jsx) |
| **J** | **Human Approval for Consequential Actions** | Proposes safe actions (`SAVE_FARM_PLAN`, `CREATE_PRICE_ALERT`); strictly blocks execution until farmer clicks "Confirm & Execute". | [`backend/main.py#confirm_action`](file:///backend/main.py#L108-L155)<br>[`frontend/src/components/ChatPanel.jsx`](file:///frontend/src/components/ChatPanel.jsx#L100-L140) |

---

## 2. Four Core Capability Areas

### Capability 1: Crop Advisory
- **User Queries Supported:**
  - *"My chilli plants have yellow leaves. What should I check?"*
  - *"My groundnut crop is 40 days old. What should I do now?"*
- **Agent Behavior:**
  - Identifies crop stage, symptom differentiation (e.g. Mites vs Thrips vs Zinc chlorosis in chilli), and authoritative ANGRAU cultural practices.
  - Distinguishes sourced facts from model reasoning.
  - Incorporates strict chemical safety warnings and Pre-Harvest Intervals (PHI).

### Capability 2: Market Intelligence
- **User Queries Supported:**
  - *"What is the current tomato market situation?"*
  - *"Which nearby market has better tomato prices?"*
  - *"Should I check other markets before selling?"*
- **Agent Behavior:**
  - Connects to official AGMARKNET / data.gov.in / e-NAM live endpoints.
  - When live bids are returned: calculates transport distance and fuel cost to determine **Net Effective Realization**.
  - When live gateway is unreachable: **strictly discloses UNAVAILABLE** without fabricating fake numbers, advising physical APMC confirmation.
  - Zero silent fallback to demo data in production.

### Capability 3: Agricultural Planning
- **User Queries Supported:**
  - *"I have 2 acres of tomato near Vijayawada. The market price is changing and I want to know what I should do this week."*
- **Agent Behavior:**
  - Synthesizes market arbitrage (shipping breaker-stage fruit to Guntur for a +₹370/q spread) with weather risks (Day 3 rain risk requiring foliar Solubor + Calcium Nitrate spray before Friday).
  - Formulates a structured, card-based Farm Action Plan.

### Capability 4: Access to Agricultural & Government Services
- **User Queries Supported:**
  - *"What government schemes may be relevant to me?"*
- **Agent Behavior:**
  - Evaluates farmer profile (2.0 Acres, Small & Marginal Farmer, AP).
  - Matches PM-KISAN, PMFBY (Andhra Pradesh Free Crop Insurance convergence), PMKSY (90% Drip Irrigation Subsidy), and SMAM Mechanization.
  - Presents eligibility criteria using cautious, non-definitive language: *"Based on the criteria provided, you may qualify if..."*
  - Provides required document checklists, step-by-step procedures, and official portals.
