from sqlalchemy.orm import Session

from ..models import EmergencyAlert


class EmergencyRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def create(
        self,
        title,
        message
    ):

        alert = EmergencyAlert(
            title=title,
            message=message
        )

        self.db.add(alert)

        self.db.commit()

        self.db.refresh(alert)

        return alert

    def active_alerts(self):

        return (
            self.db.query(
                EmergencyAlert
            )
            .filter(
                EmergencyAlert.active == True
            )
            .all()
        )