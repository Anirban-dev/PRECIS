from pydantic import BaseModel
from typing import List
from typing import Optional


class EventSchema(BaseModel):

    event_id: str

    event_type: str

    timestamp: str

    location: str


class RiskSchema(BaseModel):

    risk_score: float

    risk_level: str

    crowd_density: float

    turbulence_score: float


class AlertSchema(BaseModel):

    alert_id: str

    responders: List[str]

    alert_level: str

    active: bool = True

    notes: Optional[str] = None