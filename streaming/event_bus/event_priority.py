class EventPriority:

    def assign(
        self,
        risk_score
    ):

        if risk_score >= 90:

            return "CRITICAL"

        if risk_score >= 70:

            return "HIGH"

        if risk_score >= 40:

            return "MEDIUM"

        return "LOW"