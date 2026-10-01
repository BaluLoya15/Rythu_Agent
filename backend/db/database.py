import sqlite3
import json
import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), "rythu_agent.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables and seeds the demo farmer profile."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Farmer profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmer_profiles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        district TEXT NOT NULL,
        state TEXT NOT NULL,
        land_area TEXT NOT NULL,
        soil_type TEXT NOT NULL,
        current_crop TEXT NOT NULL,
        crop_variety TEXT NOT NULL,
        crop_stage TEXT NOT NULL,
        sowing_date TEXT NOT NULL,
        irrigation_type TEXT NOT NULL,
        farming_type TEXT NOT NULL,
        contact_phone TEXT,
        active_schemes TEXT,
        constraints TEXT,
        updated_at TEXT NOT NULL
    )
    """)

    # 2. Agent sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_sessions (
        session_id TEXT PRIMARY KEY,
        farmer_id TEXT NOT NULL,
        user_query TEXT NOT NULL,
        intent TEXT NOT NULL,
        plan_json TEXT,
        tool_trace_json TEXT,
        action_plan_json TEXT,
        final_reply TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 3. Consequential actions log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consequential_actions (
        action_id TEXT PRIMARY KEY,
        farmer_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        executed_at TEXT
    )
    """)

    # 4. Saved farm plans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_farm_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id TEXT NOT NULL,
        crop TEXT NOT NULL,
        location TEXT NOT NULL,
        stage TEXT NOT NULL,
        action_plan_json TEXT NOT NULL,
        saved_at TEXT NOT NULL
    )
    """)

    # 5. Persistent multi-conversation chat tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        farmer_id TEXT NOT NULL,
        title TEXT NOT NULL,
        language TEXT NOT NULL DEFAULT 'en',
        crop TEXT,
        crop_stage TEXT,
        context_json TEXT,
        archived INTEGER DEFAULT 0,
        manually_renamed INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        tool_trace_json TEXT,
        action_plan_json TEXT,
        sources_json TEXT,
        proposed_actions_json TEXT,
        metadata_json TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Ensure crops and document columns exist in farmer_profiles
    cursor.execute("PRAGMA table_info(farmer_profiles)")
    cols = [row[1] for row in cursor.fetchall()]
    if "crops" not in cols:
        cursor.execute("ALTER TABLE farmer_profiles ADD COLUMN crops TEXT")
    for doc_col in [
        ("passport_photo_url", "TEXT"),
        ("aadhaar_number", "TEXT"),
        ("pan_number", "TEXT"),
        ("bank_name", "TEXT"),
        ("bank_account_number", "TEXT"),
        ("bank_ifsc", "TEXT"),
        ("dbt_linked", "INTEGER DEFAULT 1"),
        ("pattadar_passbook_number", "TEXT"),
        ("documents", "TEXT")
    ]:
        if doc_col[0] not in cols:
            cursor.execute(f"ALTER TABLE farmer_profiles ADD COLUMN {doc_col[0]} {doc_col[1]}")

    # Ensure conversation_id column exists in consequential_actions
    cursor.execute("PRAGMA table_info(consequential_actions)")
    action_cols = [row[1] for row in cursor.fetchall()]
    if "conversation_id" not in action_cols:
        cursor.execute("ALTER TABLE consequential_actions ADD COLUMN conversation_id TEXT")

    # Ensure language column exists in messages
    cursor.execute("PRAGMA table_info(messages)")
    msg_cols = [row[1] for row in cursor.fetchall()]
    if "language" not in msg_cols:
        cursor.execute("ALTER TABLE messages ADD COLUMN language TEXT NOT NULL DEFAULT 'en'")

    # Seed or synchronize Default Farmer (Primary crop: Paddy)
    cursor.execute("SELECT id, current_crop, crops FROM farmer_profiles WHERE id = 'farmer-001'")
    existing = cursor.fetchone()
    if not existing:
        cursor.execute("""
        INSERT INTO farmer_profiles (
            id, name, location, district, state, land_area, soil_type,
            current_crop, crop_variety, crop_stage, sowing_date,
            irrigation_type, farming_type, contact_phone, crops, active_schemes,
            constraints, passport_photo_url, aadhaar_number, pan_number, bank_name,
            bank_account_number, bank_ifsc, dbt_linked, pattadar_passbook_number, documents, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "farmer-001",
            "Venkat Rao",
            "Vijayawada, Andhra Pradesh",
            "Krishna",
            "Andhra Pradesh",
            "2.0 Acres",
            "Clay loam with assured irrigation",
            "Paddy",
            "BPT-5204 (Samba Mahsuri)",
            "Panicle Initiation & Active Tillering (55-60 days)",
            "2026-08-10",
            "Canal & Borewell Furrow Irrigation",
            "Small & Marginal Farmer",
            "+91 98480 12345",
            json.dumps(["Paddy"]),
            json.dumps(["PM-KISAN", "YSR Rythu Bharosa"]),
            json.dumps(["Sensitive to waterlogging", "Requires balanced fertilizer schedule"]),
            "/assets/farmer_photo.jpg",
            "XXXX-XXXX-4829",
            "ABCDE1234F",
            "State Bank of India (SBI)",
            "XXXXXX5621",
            "SBIN0001234",
            1,
            "AP-KRI-2024-88412 (Khata: 412, Survey: 84/2A)",
            json.dumps(DEFAULT_FARMER_DOCUMENTS),
            datetime.now().isoformat()
        ))
    else:
        cursor.execute("""
            UPDATE farmer_profiles 
            SET name = 'Venkat Rao',
                location = 'Vijayawada, Andhra Pradesh',
                district = 'Krishna',
                state = 'Andhra Pradesh'
            WHERE id = 'farmer-001'
        """)
        # If existing record has Tomato or Rice or missing crops, normalize to Paddy
        c_crop = existing[1]
        c_crops = existing[2]
        if not c_crops or c_crop in ["Rice", "Tomato"]:
            normalized_crop = "Paddy" if c_crop in ["Rice", "Tomato"] else c_crop
            cursor.execute("""
                UPDATE farmer_profiles 
                SET current_crop = ?,
                    crop_variety = CASE WHEN current_crop IN ('Rice', 'Tomato') THEN 'BPT-5204 (Samba Mahsuri)' ELSE crop_variety END,
                    crop_stage = CASE WHEN current_crop IN ('Rice', 'Tomato') THEN 'Panicle Initiation & Active Tillering (55-60 days)' ELSE crop_stage END,
                    crops = ?
                WHERE id = 'farmer-001'
            """, (normalized_crop, json.dumps([normalized_crop])))

    conn.commit()
    conn.close()

DEFAULT_FARMER_DOCUMENTS = [
    {
        "id": "doc-001",
        "type": "passport_photo",
        "name": "Farmer_Passport_Photo.jpg",
        "title": "Passport Size Photo",
        "status": "Verified",
        "format": "JPG",
        "size": "240 KB",
        "upload_date": "2026-08-15",
        "file_url": "/assets/farmer_photo.jpg"
    },
    {
        "id": "doc-002",
        "type": "aadhaar_card",
        "name": "Aadhaar_Card_VenkatRao.pdf",
        "title": "Aadhaar Card (UIDAI)",
        "number": "XXXX-XXXX-4829",
        "status": "e-KYC Verified",
        "format": "PDF",
        "size": "1.2 MB",
        "upload_date": "2026-08-15"
    },
    {
        "id": "doc-003",
        "type": "pan_card",
        "name": "PAN_Card_ABCDE1234F.pdf",
        "title": "PAN Card (Income Tax Dept)",
        "number": "ABCDE1234F",
        "status": "Verified",
        "format": "PDF",
        "size": "850 KB",
        "upload_date": "2026-08-16"
    },
    {
        "id": "doc-004",
        "type": "bank_passbook",
        "name": "SBI_Passbook_AadhaarLinked.pdf",
        "title": "Bank Passbook (DBT Linked)",
        "bank_name": "State Bank of India",
        "account_number": "XXXXXX5621",
        "ifsc": "SBIN0001234",
        "status": "DBT Active",
        "format": "PDF",
        "size": "1.8 MB",
        "upload_date": "2026-08-15"
    },
    {
        "id": "doc-005",
        "type": "pattadar_passbook",
        "name": "RoR_1B_Pattadar_Passbook.pdf",
        "title": "Pattadar Passbook / 1B Record",
        "passbook_number": "AP-KRI-2024-88412",
        "survey_numbers": "84/2A, 84/2B (2.0 Acres)",
        "status": "Revenue Dept Certified",
        "format": "PDF",
        "size": "2.4 MB",
        "upload_date": "2026-08-15"
    }
]

# Helper queries
def get_farmer_by_id(farmer_id: str = "farmer-001") -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmer_profiles WHERE id = ?", (farmer_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["active_schemes"] = json.loads(d["active_schemes"]) if d.get("active_schemes") else []
    d["constraints"] = json.loads(d["constraints"]) if d.get("constraints") else []
    if "crops" in d and d["crops"]:
        try:
            d["crops"] = json.loads(d["crops"]) if isinstance(d["crops"], str) else d["crops"]
        except Exception:
            d["crops"] = [d.get("current_crop", "Paddy")]
    else:
        d["crops"] = [d.get("current_crop", "Paddy")] if d.get("current_crop") else ["Paddy"]

    # Provide default document & bank fields if null
    if not d.get("passport_photo_url"):
        d["passport_photo_url"] = "/assets/farmer_photo.jpg"
    if not d.get("aadhaar_number"):
        d["aadhaar_number"] = "XXXX-XXXX-4829"
    if not d.get("pan_number"):
        d["pan_number"] = "ABCDE1234F"
    if not d.get("bank_name"):
        d["bank_name"] = "State Bank of India (SBI)"
    if not d.get("bank_account_number"):
        d["bank_account_number"] = "XXXXXX5621"
    if not d.get("bank_ifsc"):
        d["bank_ifsc"] = "SBIN0001234"
    if d.get("dbt_linked") is None:
        d["dbt_linked"] = True
    else:
        d["dbt_linked"] = bool(d["dbt_linked"])
    if not d.get("pattadar_passbook_number"):
        d["pattadar_passbook_number"] = "AP-KRI-2024-88412 (Khata: 412, Survey: 84/2A)"

    if "documents" in d and d["documents"]:
        try:
            d["documents"] = json.loads(d["documents"]) if isinstance(d["documents"], str) else d["documents"]
        except Exception:
            d["documents"] = DEFAULT_FARMER_DOCUMENTS
    else:
        d["documents"] = DEFAULT_FARMER_DOCUMENTS
    return d

def update_farmer(farmer_id: str, updates: Dict[str, Any]) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in updates.items():
        if k in ["active_schemes", "constraints", "crops", "documents"] and isinstance(v, (list, dict)):
            v = json.dumps(v)
        fields.append(f"{k} = ?")
        values.append(v)
    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(farmer_id)
    query = f"UPDATE farmer_profiles SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def log_session(session_id: str, farmer_id: str, query: str, intent: str, plan: list, tool_trace: list, action_plan: dict, reply: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO agent_sessions (
        session_id, farmer_id, user_query, intent, plan_json, tool_trace_json, action_plan_json, final_reply, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id, farmer_id, query, intent,
        json.dumps(plan), json.dumps(tool_trace),
        json.dumps(action_plan) if action_plan else None,
        reply, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def save_consequential_action(action: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO consequential_actions (
        action_id, farmer_id, session_id, conversation_id, action_type, title, description, payload_json, status, created_at, executed_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action["action_id"], action["farmer_id"], action.get("session_id"), action.get("conversation_id"),
        action["action_type"], action["title"], action["description"],
        json.dumps(action["payload"]), action["status"],
        action["created_at"], action.get("executed_at")
    ))
    conn.commit()
    conn.close()

def get_conversation_actions(conversation_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM consequential_actions 
    WHERE conversation_id = ? 
    ORDER BY created_at ASC
    """, (conversation_id,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["payload"] = json.loads(d["payload_json"]) if d.get("payload_json") else {}
        del d["payload_json"]
        result.append(d)
    return result

def update_action_status(action_id: str, status: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE consequential_actions 
    SET status = ?, executed_at = ? 
    WHERE action_id = ?
    """, (status, datetime.now().isoformat() if status == "EXECUTED" else None, action_id))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def save_farm_plan(farmer_id: str, crop: str, location: str, stage: str, plan_data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO saved_farm_plans (farmer_id, crop, location, stage, action_plan_json, saved_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (farmer_id, crop, location, stage, json.dumps(plan_data), datetime.now().isoformat()))
    conn.commit()
    plan_id = cursor.lastrowid
    conn.close()
    return plan_id

def get_farmer_plans(farmer_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_farm_plans WHERE farmer_id = ? ORDER BY id DESC", (farmer_id,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["action_plan"] = json.loads(d["action_plan_json"])
        results.append(d)
    return results

# =====================================================================
# Conversation Management Helper Functions
# =====================================================================

def create_conversation(
    conv_id: Optional[str] = None,
    farmer_id: str = "farmer-001",
    title: str = "New Chat",
    language: str = "en",
    crop: Optional[str] = None,
    crop_stage: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if not conv_id:
        conv_id = f"conv-{uuid.uuid4().hex[:10]}"
    now = datetime.now().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO conversations (
        id, farmer_id, title, language, crop, crop_stage, context_json, archived, manually_renamed, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?)
    """, (
        conv_id, farmer_id, title, language, crop, crop_stage,
        json.dumps(context or {}), now, now
    ))
    conn.commit()
    conn.close()
    return get_conversation(conv_id)

def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["context"] = json.loads(d["context_json"]) if d.get("context_json") else {}
    d["archived"] = bool(d["archived"])
    d["manually_renamed"] = bool(d["manually_renamed"])
    return d

def list_conversations(farmer_id: str, include_archived: bool = False) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if include_archived:
        cursor.execute("SELECT * FROM conversations WHERE farmer_id = ? ORDER BY updated_at DESC", (farmer_id,))
    else:
        cursor.execute("SELECT * FROM conversations WHERE farmer_id = ? AND archived = 0 ORDER BY updated_at DESC", (farmer_id,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["context"] = json.loads(d["context_json"]) if d.get("context_json") else {}
        d["archived"] = bool(d["archived"])
        d["manually_renamed"] = bool(d["manually_renamed"])
        results.append(d)
    return results

def update_conversation(conv_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in updates.items():
        if k == "context" or k == "context_json":
            fields.append("context_json = ?")
            values.append(json.dumps(v) if isinstance(v, dict) else v)
        elif k in ["title", "language", "crop", "crop_stage", "archived", "manually_renamed"]:
            fields.append(f"{k} = ?")
            values.append(int(v) if isinstance(v, bool) else v)
    if not fields:
        conn.close()
        return get_conversation(conv_id)

    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(conv_id)
    query = f"UPDATE conversations SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_conversation(conv_id)

def archive_conversation(conv_id: str, archived: bool = True) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET archived = ?, updated_at = ? WHERE id = ?", (
        1 if archived else 0, datetime.now().isoformat(), conv_id
    ))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def delete_conversation(conv_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    cursor.execute("DELETE FROM consequential_actions WHERE conversation_id = ?", (conv_id,))
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def search_conversations(query: str, farmer_id: str = "farmer-001") -> List[Dict[str, Any]]:
    pattern = f"%{query.strip()}%"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT c.* FROM conversations c
    LEFT JOIN messages m ON c.id = m.conversation_id
    WHERE c.farmer_id = ?
      AND (
        c.title LIKE ?
        OR c.crop LIKE ?
        OR m.content LIKE ?
        OR c.context_json LIKE ?
      )
    ORDER BY c.updated_at DESC
    """, (farmer_id, pattern, pattern, pattern, pattern))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["context"] = json.loads(d["context_json"]) if d.get("context_json") else {}
        d["archived"] = bool(d["archived"])
        d["manually_renamed"] = bool(d["manually_renamed"])
        results.append(d)
    return results

def save_message(
    conversation_id: str,
    role: str,
    content: str,
    msg_id: Optional[str] = None,
    language: str = "en",
    tool_trace: Optional[List[Dict[str, Any]]] = None,
    action_plan: Optional[Dict[str, Any]] = None,
    sources: Optional[List[Dict[str, Any]]] = None,
    proposed_actions: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if not msg_id:
        msg_id = f"msg-{uuid.uuid4().hex[:10]}"
    now = datetime.now().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (
        id, conversation_id, role, content, language, tool_trace_json, action_plan_json,
        sources_json, proposed_actions_json, metadata_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        msg_id, conversation_id, role, content, language,
        json.dumps(tool_trace) if tool_trace else None,
        json.dumps(action_plan) if action_plan else None,
        json.dumps(sources) if sources else None,
        json.dumps(proposed_actions) if proposed_actions else None,
        json.dumps(metadata) if metadata else None,
        now
    ))
    # Also touch conversation updated_at
    cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()
    return {
        "id": msg_id,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "language": language,
        "tool_trace": tool_trace or [],
        "action_plan": action_plan,
        "sources": sources or [],
        "proposed_actions": proposed_actions or [],
        "metadata": metadata or {},
        "created_at": now
    }

def get_conversation_messages(conversation_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conversation_id,))
    rows = cursor.fetchall()
    conn.close()
    messages = []
    for r in rows:
        d = dict(r)
        messages.append({
            "id": d["id"],
            "conversation_id": d["conversation_id"],
            "role": d["role"],
            "content": d["content"],
            "language": d.get("language") or "en",
            "tool_trace": json.loads(d["tool_trace_json"]) if d.get("tool_trace_json") else [],
            "action_plan": json.loads(d["action_plan_json"]) if d.get("action_plan_json") else None,
            "sources": json.loads(d["sources_json"]) if d.get("sources_json") else [],
            "proposed_actions": json.loads(d["proposed_actions_json"]) if d.get("proposed_actions_json") else [],
            "metadata": json.loads(d["metadata_json"]) if d.get("metadata_json") else {},
            "created_at": d["created_at"]
        })
    return messages

# Initialize DB when module loaded
init_db()
