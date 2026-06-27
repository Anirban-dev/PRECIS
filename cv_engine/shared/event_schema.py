from pydantic import BaseModel
from typing import List
from typing import Optional


class EmergencyEventSchema(BaseModel):

    event_id: str

    event_type: str

    timestamp: str

    location: str

    severity: str

    active: bool = True


class AlertDispatchSchema(BaseModel):

    responders: List[str]

    dispatch_status: str

    estimated_response_time: str


class CrowdIncidentSchema(BaseModel):

    incident_id: str

    crowd_state: str

    shockwave_detected: bool

    evacuation_required: bool

    affected_zones: List[str]

    notes: Optional[str] = None