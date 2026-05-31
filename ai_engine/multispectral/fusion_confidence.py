class FusionConfidence:

    def calculate(

        self,

        rgb_confidence,

        thermal_confidence,

        infrared_confidence
    ):

        return (

            rgb_confidence * 0.4 +

            thermal_confidence * 0.35 +

            infrared_confidence * 0.25
        )