from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.risk_service import RiskService

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)

risk_service = RiskService()


class RiskRequest(BaseModel):
    density_map: list[float]
    turbulence_score: float
    fusion_confidence: float = 0.95
    sensor_health: Literal["HEALTHY", "DEGRADED", "OFFLINE"] = "HEALTHY"


@router.post("/", operation_id="calculate_risk")
async def calculate_risk(payload: RiskRequest):
    return risk_service.calculate_risk(
        density_map=payload.density_map,
        turbulence_score=payload.turbulence_score,
        fusion_confidence=payload.fusion_confidence,
        sensor_health=payload.sensor_health
    )
