from fastapi import APIRouter

from backend.services.incident_service import (
    IncidentService
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

service = IncidentService()


@router.get("/")
async def list_incidents():
    return service.get_all()
