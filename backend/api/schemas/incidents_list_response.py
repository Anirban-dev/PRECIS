from pydantic import BaseModel
from typing import List

from backend.api.schemas.incident_response import (
    IncidentResponse
)


class IncidentsListResponse(BaseModel):
    count: int
    incidents: List[IncidentResponse]