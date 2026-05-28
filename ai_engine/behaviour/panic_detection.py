class PanicDetection:

    def detect(

        self,

        turbulence_score,

        movement_speed,

        scream_probability
    ):

        if (

            turbulence_score > 8 and

            movement_speed > 6 and

            scream_probability > 0.7
        ):

            return {

                "panic": True,

                "severity": "HIGH"
            }

        return {

            "panic": False,

            "severity": "LOW"
        }