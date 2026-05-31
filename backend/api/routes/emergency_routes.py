from fastapi import APIRouter

from backend.services.emergency_service import (
    EmergencyService
)

router = APIRouter(
    prefix="/emergency",
    tags=["Emergency"]
)

service = EmergencyService()


@router.post("/recommend")
async def recommend(payload: dict):

    return service.generate_response(

        payload["risk_level"],

        payload["sector_id"],

        payload["sensor_health"]
    )