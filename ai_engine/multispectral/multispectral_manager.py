from ai_engine.multispectral.thermal_detector import (
    ThermalDetector
)

from ai_engine.multispectral.infrared_detector import (
    InfraredDetector
)

from ai_engine.multispectral.spectral_fusion import (
    SpectralFusion
)


class MultispectralManager:

    def __init__(self):

        self.thermal = ThermalDetector()

        self.infrared = InfraredDetector()

        self.fusion = SpectralFusion()

    def process(

        self,

        thermal_frame,

        infrared_frame
    ):

        thermal_result = (

            self.thermal.detect(
                thermal_frame
            )
        )

        infrared_result = (

            self.infrared.detect(
                infrared_frame
            )
        )

        return {

            "thermal":
                thermal_result,

            "infrared":
                infrared_result
        }