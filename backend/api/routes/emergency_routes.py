from fastapi import APIRouter

from backend.services.emergency_service import (
    EmergencyService
)
from backend.api.schemas.emergency_schema import (
    EmergencyRecommendationRequest,
    EmergencyRecommendationResponse
)

router = APIRouter(
    prefix="/emergency",
    tags=["Emergency"]
)

service = EmergencyService()


@router.post("/recommend", response_model=EmergencyRecommendationResponse)
async def recommend(payload: EmergencyRecommendationRequest):

    return service.generate_response(

        payload.risk_level,

        payload.sector_id,

        payload.sensor_health
    )
