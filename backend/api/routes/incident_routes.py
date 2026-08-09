from fastapi import APIRouter

from backend.services.incident_service import (
    IncidentService
)
from backend.api.schemas.incidents_list_response import IncidentsListResponse

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

service = IncidentService()


@router.get("/", response_model=IncidentsListResponse)
async def list_incidents():
    return service.get_all()
