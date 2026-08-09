from typing import Literal

from pydantic import BaseModel


class EmergencyRecommendationRequest(BaseModel):
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    sector_id: str
    sensor_health: Literal["HEALTHY", "DEGRADED", "OFFLINE"]


class EmergencyRecommendationResponse(BaseModel):
    sector_id: str
    risk_level: str
    sensor_health: str
    priority: str
    recommendations: list[str]
