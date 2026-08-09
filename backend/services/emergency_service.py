class EmergencyService:

    def generate_response(
        self,
        risk_level,
        sector_id,
        sensor_health
    ):

        recommendations = []

        normalized_risk = str(risk_level).upper()
        normalized_sensor = str(sensor_health).upper()

        if normalized_risk == "CRITICAL":
            recommendations.extend([
                "Activate emergency response team immediately",
                "Open evacuation routes for the affected sector",
                "Dispatch crowd control personnel to pressure points",
                "Issue urgent public safety announcements",
                "Notify incident commander"
            ])

        elif normalized_risk == "HIGH":

            recommendations.extend([
                "Activate emergency response team",
                "Increase crowd control personnel",
                "Issue public safety announcements",
                "Monitor evacuation routes"
            ])

        elif normalized_risk == "MEDIUM":

            recommendations.extend([
                "Increase monitoring frequency",
                "Deploy standby personnel",
                "Inspect high-density zones"
            ])

        else:

            recommendations.extend([
                "Continue normal operations",
                "Maintain routine monitoring"
            ])

        if normalized_sensor != "HEALTHY":

            recommendations.append(
                "Inspect and recalibrate sensors"
            )

        return {
            "sector_id": sector_id,
            "risk_level": normalized_risk,
            "sensor_health": normalized_sensor,
            "priority": "IMMEDIATE" if normalized_risk == "CRITICAL" else normalized_risk,
            "recommendations": recommendations
        }
