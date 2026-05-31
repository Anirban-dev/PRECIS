class PanicScoreEngine:

    def calculate(

        self,

        density_score,

        turbulence_score,

        shockwave_score,

        trajectory_score
    ):

        panic_score = (

            density_score * 0.30 +

            turbulence_score * 0.30 +

            shockwave_score * 0.25 +

            trajectory_score * 0.15
        )

        if panic_score >= 80:

            level = "CRITICAL"

        elif panic_score >= 60:

            level = "HIGH"

        elif panic_score >= 40:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {

            "panic_score":

                round(
                    panic_score,
                    2
                ),

            "panic_level":
                level
        }