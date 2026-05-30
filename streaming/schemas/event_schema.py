from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class EventSchema(BaseModel):

    event_type: str

    payload: Dict

    camera_type: str

    sensor_health: str

    timestamp: datetime

    sector_id: Optional[str] = None

    camera_id: Optional[str] = None

    confidence: Optional[float] = None