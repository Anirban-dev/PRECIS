class StampedeDetector:

    def detect(

        self,

        density,

        turbulence
    ):

        if (

            density > 9 and

            turbulence > 8
        ):

            return {

                "stampede": True,

                "severity": "CRITICAL"
            }

        return {

            "stampede": False,

            "severity": "NORMAL"
        }