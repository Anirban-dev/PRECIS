from pydantic import BaseModel


class IncidentResponse(BaseModel):
    timestamp: str
    camera_id: str
    density: float
    risk_level: str
    description: str