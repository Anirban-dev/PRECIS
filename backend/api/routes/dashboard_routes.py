from fastapi import APIRouter

from backend.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

dashboard = DashboardService()


@router.get("/summary")
async def summary():

    return dashboard.summary()