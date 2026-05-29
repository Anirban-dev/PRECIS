from .connection import engine
from .models import (
    CrowdAnalytics,
    RiskEvent,
    EmergencyAlert
)

def initialize_database():

    CrowdAnalytics.metadata.create_all(
        bind=engine
    )