from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CrowdPosition(BaseModel):
    x: float
    y: float
    width: float
    height: float

class PersonTrack(BaseModel):
    track_id: int
    bounding_box: CrowdPosition
    velocity_x: float
    velocity_y: float
    oscillation_frequency: float  # classical cv analysis (sway frequency in Hz)

class VideoAnalyticsEvent(BaseModel):
    camera_id: str
    timestamp: str
    person_count: int
    density_map_resolution: List[int] = Field(default_factory=lambda: [640, 480])
    tracks: List[PersonTrack]
    mean_velocity_magnitude: float
    flow_divergence: float  # visual turbulence

class AudioAnalyticsEvent(BaseModel):
    sensor_id: str
    timestamp: str
    decibel_level: float
    dominant_frequency: float
    stress_pitch_drift: float  # increase in vocal stress indicator
    screaming_detected: bool
    acoustic_fracture_index: float  # 0 to 1 risk score from sound

class CrowdCriticalityEvent(BaseModel):
    timestamp: str
    camera_ids: List[str]
    phase_state_index: float = Field(..., description="PSI: 0=laminar flow, 1=fully turbulent/panic transition")
    outstroke_probability: float = Field(..., description="OPS (0-100%): Probability of a crowd surge")
    crowd_criticality_index: float = Field(..., description="CCI (0-100%): Overall threat score combining audio + vision")
    shockwave_trajectories: List[Dict[str, Any]] = Field(default_factory=list)
    alert_level: str  # GREEN, YELLOW, ORANGE, RED

class EmergencyDispatchEvent(BaseModel):
    dispatch_id: str
    timestamp: str
    criticality_event: CrowdCriticalityEvent
    allocated_police_units: int
    allocated_medical_units: int
    allocated_fire_units: int
    triage_zone_lat_lng: Dict[str, float]
    rescue_routes: List[List[Dict[str, float]]]
    notified_hospitals: List[str]
    status: str  # DISPATCHED, ACTIVE, RESOLVED
