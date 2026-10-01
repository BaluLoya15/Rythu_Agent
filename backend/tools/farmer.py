from typing import Optional, Dict, Any, List
from backend.db.database import get_farmer_by_id, update_farmer, get_connection
from backend.models.schemas import FarmerProfile, FarmerProfileUpdate

def get_farmer_profile(farmer_id: str = "farmer-001") -> Optional[FarmerProfile]:
    """Retrieves farmer profile from SQLite database."""
    data = get_farmer_by_id(farmer_id)
    if not data:
        return None
    return FarmerProfile(**data)

def update_farmer_profile(farmer_id: str, updates: FarmerProfileUpdate) -> Optional[FarmerProfile]:
    """Updates farmer profile in SQLite database."""
    update_dict = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not update_dict:
        return get_farmer_profile(farmer_id)
    
    success = update_farmer(farmer_id, update_dict)
    if success:
        return get_farmer_profile(farmer_id)
    return None

def list_all_farmers() -> List[FarmerProfile]:
    """Lists all available farmer profiles."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmer_profiles ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    
    profiles = []
    for r in rows:
        d = dict(r)
        d["active_schemes"] = json.loads(d["active_schemes"]) if d.get("active_schemes") else []
        d["constraints"] = json.loads(d["constraints"]) if d.get("constraints") else []
        if d.get("crops") and isinstance(d["crops"], str):
            try:
                d["crops"] = json.loads(d["crops"])
            except Exception:
                d["crops"] = [d.get("current_crop", "Paddy")]
        if d.get("documents") and isinstance(d["documents"], str):
            try:
                d["documents"] = json.loads(d["documents"])
            except Exception:
                pass
        profiles.append(FarmerProfile(**d))
    return profiles
