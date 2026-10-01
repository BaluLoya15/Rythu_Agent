# Rythu Agent - Hackathon Live Presentation Script

> **BharatAgentic Hackathon Presentation Script (5 to 7 Minutes)**  
> **Category: Agri Tech & Rural Bharat**

---

## 🎙️ 1. Opening Hook & The Real Problem (1 Minute)

> **Speaker:**
> *"Distinguished judges, there are over 140 million farmers in India. When a farmer has a problem—like pest infestations, changing weather, or finding selling options—they don't need a conversational chatbot reciting generic advice, nor do they want an interface filled with rigid, hardcoded demo buttons.*
> 
> *A farmer needs a genuine **Action Agent**. An agent where they can speak or type naturally; an agent that understands their exact acreage, soil type, and crop stage; queries **live satellite weather**; checks **official market portals**; retrieves **authoritative university research**; and synthesizes all of this into a concrete, prioritized Action Plan.*
>
> *Most importantly: **Rythu Agent enforces strict data honesty**. If live market data is unavailable from the official gateway, the agent openly discloses it rather than fabricating fake real-time numbers.*
>
> *Introducing **RYTHU AGENT (రైతు ఏజెంట్)**: An AI-powered action agent for India's farmers and rural communities."*

---

## 🚀 2. Live Farmer Request: 2-Acre Tomato in Vijayawada (2.5 Minutes)

### Step 1: Clean Farmer-Facing Interface
- Show the clean dashboard:
  > *"Notice how the main interface is clean and natural. There are no predefined scenario buttons cluttering the farmer's view. The entry point is a welcoming chat: **'How can I help with your farm today?'** with natural suggestion chips.*
  > 
  > *In the header, notice our active farmer profile: **Venkat Rao**, farming **2.0 Acres** of Tomato (Arka Rakshak F1 hybrid) near **Vijayawada, Andhra Pradesh** at the **Flowering & Fruit Development stage (45-50 days)**."*

### Step 2: Typing the Natural Farmer Query
- Type directly into the chat:
  > **Query:** *"I have 2 acres of tomato near Vijayawada. What should I do this week and where should I check for better market prices?"*

### Step 3: Real Tool Execution & Provenance Tracking
- Switch to the **Agent Activity Timeline** tab:
  > *"Look at the real-time execution trace. Every step is an actual tool invocation with real latencies:
  > 1. **Intent Identified:** Classified dynamically as `HYBRID_PLANNING_AND_MARKET`.
  > 2. **Farmer Context Loaded:** Extracted 2.0 acres in Vijayawada with drip irrigation.
  > 3. **Live Weather Tool (Open-Meteo):** Geocoded Vijayawada (16.51°N, 80.65°E), queried the live satellite feed, and pulled **real-time metrics: 33.5°C, 53% humidity, and wind at 8.2 km/h**.
  > 4. **Official Market Tool:** Attempted official AGMARKNET/e-NAM gateway. Because live API access was unreachable, the agent **honestly disclosed UNAVAILABLE** instead of faking prices!
  > 5. **Agri RAG:** Retrieved 3 authoritative guidelines from **ANGRAU** and **ICAR-IIHR** manuals.
  > 6. **Multi-Source Reasoning:** Formulated a safe, stage-specific action plan."*

### Step 4: The Actionable Result (Action Plan Tab)
- Click on **Today's Farm Action Plan** tab:
  > *"Notice the clear, structured cards:
  > - **Live Agro-Met Advisory:** Recommends an optimal spray window between **4:30 PM and 6:30 PM** based on the live 8.2 km/h calm wind condition.
  > - **Foliar Nutrition:** Sourced from ANGRAU Manual Page 28, recommends **Solubor (Boron 20%) @ 1.0 g/L + Calcium Nitrate @ 2.5 g/L** to prevent flower drop and blossom end rot.
  > - **Market Transparency:** Openly informs the farmer that live APMC market data was unreachable, advising physical verification with the local market yard secretary."*

### Step 5: Natural Human-in-the-Loop Confirmation
- Show the confirmation card in the chat:
  > *"Notice what appeared in the chat:
  > 
  > **🤖 Rythu Agent wants your confirmation**
  > **Proposed action:** Save 7-Day Cultivation & Cultural Plan to Farm Profile.  
  > **Why:** This will help you keep track of needed cultural tasks and spray timings on your farm profile.
  > 
  > The agent never takes consequential action without farmer approval. I click **'Confirm & Execute'**. 
  > The action is executed and permanently recorded into the SQLite farm notebook!"*

---

## 🏛️ 3. Second Query: Government Schemes & Subsidies (1.5 Minutes)

- Type into the chat:
  > **Query:** *"What agricultural government services may be relevant to me?"*

- Switch to the **Government Schemes** tab:
  > *"The agent analyzes the farmer profile (Small & Marginal, 2.0 Acres, AP) and matches verified central and state schemes:
  > 1. **PM-KISAN:** ₹6,000/year income support.
  > 2. **PMFBY Free Crop Insurance:** Under Andhra Pradesh convergence, the state covers the premium for e-Crop registered farmers.
  > 3. **PMKSY Micro-Irrigation:** Up to 90% subsidy for drip irrigation kits.
  >
  > Crucially, Rythu Agent **does not make false legal claims**. It states: *'Based on the available criteria, you may qualify if...'*, providing required document checklists (Pattadar Passbook, Aadhaar, e-Crop receipt) and official portal links."*

---

## 🔬 4. Authoritative Grounding & No Hallucinations (1 Minute)

- Click on the **ANGRAU / ICAR Sources** tab:
  > *"Every agricultural claim is grounded in verified university research:
  > - ANGRAU Commercial Tomato Production Manual (Pub No. AP-AGRI-TOM-P03, Page 28).
  > - ICAR-IIHR Solanaceous IPM Protocol (TB-2023-TOM-IPM, Page 44).
  > - Official Ministry of Agriculture Scheme Portals.
  >
  > Full data provenance: Live satellite feeds + Verified university research + Strict data honesty."*

---

## 🏆 5. Conclusion (30 Seconds)

> *"Rythu Agent proves that AI for rural Bharat does not have to be a toy or a canned demo. It is a live, transparent, grounded action agent that respects the farmer's intelligence and helps them make safer, more profitable decisions every day.
> 
> Thank you, and we welcome your questions!"*
