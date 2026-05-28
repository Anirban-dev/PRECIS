class ViolenceDetector:

    def detect(

        self,

        motion_intensity,

        collision_rate
    ):

        if (

            motion_intensity > 8 and

            collision_rate > 6
        ):

            return {

                "violence": True,

                "risk_level": "HIGH"
            }

        return {

            "violence": False,

            "risk_level": "LOW"
        }