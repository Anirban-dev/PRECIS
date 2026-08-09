from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_incidents: int
    critical_risk: int = 0
    high_risk: int
    medium_risk: int
