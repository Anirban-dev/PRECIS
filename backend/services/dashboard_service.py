from backend.services.incident_service import IncidentService


class DashboardService:

    def __init__(self):
        self.incident_service = IncidentService()

    def summary(self):
        data = self.incident_service.get_all()
        incidents = data["incidents"]

        high = sum(1 for i in incidents if i["risk_level"] == "HIGH")
        medium = sum(1 for i in incidents if i["risk_level"] == "MEDIUM")

        return {
            "total_incidents": len(incidents),
            "high_risk": high,
            "medium_risk": medium
        }

    def recent_incidents(self, limit=10):
        data = self.incident_service.get_all()
        incidents = data["incidents"]

        return {
            "count": min(limit, len(incidents)),
            "incidents": incidents[-limit:]
        }

    def risk_distribution(self):
        data = self.incident_service.get_all()
        incidents = data["incidents"]

        distribution = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        for incident in incidents:
            level = incident["risk_level"]
            if level in distribution:
                distribution[level] += 1

        return distribution

    def camera_statistics(self):
        data = self.incident_service.get_all()
        incidents = data["incidents"]

        stats = {}
        for incident in incidents:
            camera = incident["camera_id"]
            stats[camera] = stats.get(camera, 0) + 1

        return stats
