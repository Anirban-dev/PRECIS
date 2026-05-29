from sqlalchemy.orm import Session

from ..queries import (
    insert_analytics,
    fetch_recent_analytics
)


class AnalyticsRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def create(
        self,
        crowd_count,
        density,
        turbulence
    ):
        return insert_analytics(
            self.db,
            crowd_count,
            density,
            turbulence
        )

    def recent(
        self,
        limit=20
    ):
        return fetch_recent_analytics(
            self.db,
            limit
        )