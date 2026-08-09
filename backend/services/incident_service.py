import json
import logging
import threading
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class IncidentService:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    FILE_PATH = PROJECT_ROOT / "data" / "incidents.json"
    _lock = threading.Lock()

    def __init__(self):
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        if not self.FILE_PATH.exists():
            self._save([])

    def _load(self):
        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logger.exception("Malformed incidents JSON. Resetting to an empty list.")
            self._save([])
            return []
        except FileNotFoundError:
            self._save([])
            return []

        if not isinstance(data, list):
            logger.error("Incidents JSON root was not a list. Resetting.")
            self._save([])
            return []

        return data

    def _save(self, incidents):
        temp_path = self.FILE_PATH.with_suffix(".json.tmp")
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(incidents, f, indent=4)
        temp_path.replace(self.FILE_PATH)

    def create_incident(self, camera_id, density, risk_level):
        with self._lock:
            incidents = self._load()

            incident = {
                "timestamp": datetime.utcnow().isoformat(),
                "camera_id": camera_id,
                "density": density,
                "risk_level": str(risk_level).upper(),
                "description": f"{str(risk_level).upper()} crowd event detected"
            }

            incidents.append(incident)
            self._save(incidents)

            return incident

    def get_all(self):
        with self._lock:
            incidents = self._load()
        return {
            "count": len(incidents),
            "incidents": incidents
        }

    def clear(self):
        with self._lock:
            self._save([])
