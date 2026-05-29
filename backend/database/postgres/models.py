from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    JSON
)

from .connection import Base


class CrowdAnalytics(Base):

    __tablename__ = "crowd_analytics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    crowd_count = Column(Integer)

    density = Column(Float)

    turbulence_score = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RiskEvent(Base):

    __tablename__ = "risk_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_type = Column(String)

    risk_level = Column(String)

    confidence = Column(Float)

    metadata = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class EmergencyAlert(Base):

    __tablename__ = "emergency_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(String)

    message = Column(String)

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )