from pydantic import BaseModel
from typing import List, Any


class CrowdAnalyticsRequest(BaseModel):

    rgb_density: List[float]

    thermal_density: List[float]

    infrared_density: List[float]


class AnalyticsResponse(BaseModel):

    crowd_flow: str

    panic: dict[str, Any]

    forecast: dict[str, Any]

    prediction: dict[str, Any]

    risk: dict[str, Any]