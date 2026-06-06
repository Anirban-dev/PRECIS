class EmergencyService:

    def generate_response(
        self,
        risk_level,
        sector_id,
        sensor_health
    ):

        recommendations = []

        if str(risk_level).upper() == "HIGH":

            recommendations.extend([
                "Activate emergency response team",
                "Increase crowd control personnel",
                "Issue public safety announcements",
                "Monitor evacuation routes"
            ])

        elif str(risk_level).upper() == "MEDIUM":

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

        if str(sensor_health).upper() != "HEALTHY":

            recommendations.append(
                "Inspect and recalibrate sensors"
            )

        return {
            "sector_id": sector_id,
            "risk_level": risk_level,
            "sensor_health": sensor_health,
            "recommendations": recommendations
        }