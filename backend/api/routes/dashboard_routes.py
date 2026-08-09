from fastapi import APIRouter

from backend.services.dashboard_service import (
    DashboardService
)
from backend.api.schemas.dashboard_response import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

dashboard = DashboardService()


@router.get("/summary", response_model=DashboardResponse)
async def summary():

    return dashboard.summary()
