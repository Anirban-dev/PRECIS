from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Camera(Base):

    __tablename__ = "cameras"

    id = Column(
        Integer,
        primary_key=True
    )

    camera_id = Column(
        String,
        unique=True,
        nullable=False
    )

    sector_id = Column(
        String,
        nullable=False
    )

    camera_type = Column(
        String,
        nullable=False
    )

    stream_url = Column(
        String
    )

    sensor_health = Column(
        String,
        default="HEALTHY"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RiskEvent(Base):

    __tablename__ = "risk_events"

    id = Column(
        Integer,
        primary_key=True
    )

    sector_id = Column(
        String
    )

    risk_level = Column(
        String
    )

    risk_score = Column(
        Float
    )

    fusion_confidence = Column(
        Float
    )

    camera_type = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )