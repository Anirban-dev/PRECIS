import json
import os
from datetime import datetime


class IncidentService:
    FILE_PATH = "data/incidents.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(self.FILE_PATH, "r") as f:
            return json.load(f)

    def _save(self, incidents):
        with open(self.FILE_PATH, "w") as f:
            json.dump(incidents, f, indent=4)

    def create_incident(self, camera_id, density, risk_level):
        incidents = self._load()

        incident = {
            "timestamp": datetime.utcnow().isoformat(),
            "camera_id": camera_id,
            "density": density,
            "risk_level": risk_level,
            "description": f"{risk_level} crowd event detected"
        }

        incidents.append(incident)
        self._save(incidents)

        return incident

    def get_all(self):
        incidents = self._load()
        return {
            "count": len(incidents),
            "incidents": incidents
        }
