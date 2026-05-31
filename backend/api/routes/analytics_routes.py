from fastapi import APIRouter

from backend.services.analytics_service import (
    AnalyticsService
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

analytics_service = AnalyticsService()


@router.get("/health")
async def analytics_health():

    return {
        "service": "analytics",
        "status": "healthy"
    }


@router.post("/crowd")
async def crowd_analytics(payload: dict):

    return analytics_service.generate_crowd_analytics(

        payload.get("rgb_density", []),

        payload.get("thermal_density", []),

        payload.get("infrared_density", [])
    )