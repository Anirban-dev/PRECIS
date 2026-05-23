from pydantic import BaseModel
from typing import List
from typing import Optional


class MotionVectorSchema(BaseModel):

    vector_id: str

    magnitude: float

    direction: float

    velocity: float

    zone: str


class MotionFrameSchema(BaseModel):

    frame_id: str

    timestamp: str

    active_vectors: int

    average_velocity: float

    vectors: List[MotionVectorSchema]


class CrowdMotionAnalyticsSchema(BaseModel):

    crowd_density: float

    turbulence_score: float

    synchronized_motion: bool

    resonance_probability: float

    dominant_direction: Optional[float] = 0.0