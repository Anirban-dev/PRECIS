from backend.services.analytics_service import AnalyticsService
from backend.services.risk_service import RiskService


class StreamingToBackend:

    def __init__(self):

        self.analytics = AnalyticsService()

        self.risk = RiskService()

    def process_event(

        self,

        payload
    ):

        analytics = self.analytics.generate_live_analytics()

        risk = self.risk.evaluate_risk(
            analytics
        )

        return {

            "analytics":
                analytics,

            "risk":
                risk,

            "stream_payload":
                payload
        }