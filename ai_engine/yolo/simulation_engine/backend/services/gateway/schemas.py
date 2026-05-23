from pydantic import BaseModel
from typing import Optional
from typing import List


class CrowdRiskRequest(BaseModel):

    fusion_score: float

    turbulence_score: float

    resonance_probability: float

    outstroke_probability: float


class FusionRequest(BaseModel):

    optical_flow_score: float

    audio_stress_score: float

    density_score: float

    turbulence_score: float


class EmergencyAlertRequest(BaseModel):

    risk_level: str

    location: str

    shockwave_detected: bool = False


class CrowdAnalyticsResponse(BaseModel):

    timestamp: str

    overall_risk_score: float

    risk_level: str

    emergency_dispatch: bool

    system_state: str


class FusionResponse(BaseModel):

    timestamp: str

    fusion_score: float

    crowd_state: str

    fusion_engine: str


class EmergencyDispatchResponse(BaseModel):

    timestamp: str

    emergency_id: str

    location: str

    risk_level: str

    shockwave_detected: bool

    responders_notified: List[str]

    dispatch_status: str


class LiveAnalyticsSchema(BaseModel):

    crowd_state: str

    risk_level: str

    active_alerts: int

    shockwave_detected: bool

    resonance_probability: float

    timestamp: str


class EmergencyStatusSchema(BaseModel):

    ambulance_network: str

    hospital_alert_system: str

    police_control: str

    fire_response: str

    emergency_mode: bool

    timestamp: str


class SystemHealthSchema(BaseModel):

    system: str

    gateway: str

    cv_engine: str

    ai_engine: str

    event_bus: str

    dashboard: str

    timestamp: str


class NotificationSchema(BaseModel):

    recipient: str

    priority: str

    status: str


class DashboardAlertSchema(BaseModel):

    alert_status: str

    ui_color: str


class RiskInsightSchema(BaseModel):

    location: Optional[str] = None

    zone_id: Optional[str] = None

    pressure_index: Optional[float] = 0.0

    evacuation_risk: Optional[str] = "LOW"

    predicted_failure_window: Optional[str] = None