class ShockwaveDetector:

    def __init__(self):

        self.previous_velocity = None

    def detect(
        self,
        current_velocity
    ):

        if self.previous_velocity is None:

            self.previous_velocity = current_velocity

            return {

                "shockwave_detected": False,

                "severity": "LOW"
            }

        delta = abs(
            current_velocity
            - self.previous_velocity
        )

        self.previous_velocity = current_velocity

        if delta > 2:

            return {

                "shockwave_detected": True,

                "severity": "HIGH"
            }

        elif delta > 1:

            return {

                "shockwave_detected": True,

                "severity": "MEDIUM"
            }

        return {

            "shockwave_detected": False,

            "severity": "LOW"
        }