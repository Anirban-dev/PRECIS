from pydantic import BaseModel
from typing import List
from typing import Optional


class RiskScoreSchema(BaseModel):

    risk_score: float

    risk_level: str

    emergency_required: bool


class CriticalitySchema(BaseModel):

    criticality_score: float

    crowd_state: str

    collapse_probability: float

    evacuation_complexity: float


class RiskAssessmentSchema(BaseModel):

    timestamp: str

    turbulence_score: float

    bottleneck_score: float

    outstroke_probability: float

    resonance_probability: float

    final_risk_score: float

    risk_level: str


class EmergencyRecommendationSchema(BaseModel):

    emergency_units: List[str]

    evacuation_required: bool

    alert_status: str

    response_priority: str

    nearest_safe_zone: Optional[str] = None