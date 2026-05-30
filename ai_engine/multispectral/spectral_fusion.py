import numpy as np


class SpectralFusion:

    def fuse_density(

        self,

        rgb_density,

        thermal_density,

        infrared_density,

        rgb_weight=0.4,

        thermal_weight=0.35,

        infrared_weight=0.25
    ):

        rgb = np.array(
            rgb_density
        )

        thermal = np.array(
            thermal_density
        )

        infrared = np.array(
            infrared_density
        )

        fused = (

            rgb * rgb_weight +

            thermal * thermal_weight +

            infrared * infrared_weight
        )

        return fused.tolist()

    def fuse_confidence(

        self,

        confidences
    ):

        return max(
            confidences
        )