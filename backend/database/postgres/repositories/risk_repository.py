from sqlalchemy.orm import Session

from ..models import RiskEvent


class RiskRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def create(
        self,
        event_type,
        risk_level,
        confidence,
        metadata
    ):

        event = RiskEvent(
            event_type=event_type,
            risk_level=risk_level,
            confidence=confidence,
            metadata=metadata
        )

        self.db.add(event)

        self.db.commit()

        self.db.refresh(event)

        return event

    def all(self):

        return (
            self.db.query(RiskEvent)
            .order_by(
                RiskEvent.created_at.desc()
            )
            .all()
        )