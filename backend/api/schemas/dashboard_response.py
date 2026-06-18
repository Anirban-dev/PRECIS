from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_incidents: int
    high_risk: int
    medium_risk: int