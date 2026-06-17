from fastapi import APIRouter

from backend.services.analytics_service import AnalyticsService
from backend.api.schemas.analytics_schema import CrowdAnalyticsRequest

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
async def crowd_analytics(payload: CrowdAnalyticsRequest):
    return analytics_service.generate_crowd_analytics(
        payload.rgb_density,
        payload.thermal_density,
        payload.infrared_density
    )
