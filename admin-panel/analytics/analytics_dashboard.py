from datetime import datetime


class AnalyticsDashboard:

    def dashboard_summary(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "crowd_density": 7.1,

            "turbulence_score": 5.4,

            "risk_level": "HIGH"
        }