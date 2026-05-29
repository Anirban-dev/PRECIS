from sqlalchemy.orm import Session

from .models import (
    CrowdAnalytics,
    RiskEvent,
    EmergencyAlert
)


def insert_analytics(
    db: Session,
    crowd_count: int,
    density: float,
    turbulence_score: float
):

    row = CrowdAnalytics(
        crowd_count=crowd_count,
        density=density,
        turbulence_score=turbulence_score
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    return row


def fetch_recent_analytics(
    db: Session,
    limit: int = 20
):

    return (
        db.query(CrowdAnalytics)
        .order_by(
            CrowdAnalytics.created_at.desc()
        )
        .limit(limit)
        .all()
    )