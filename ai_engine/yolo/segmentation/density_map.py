import numpy as np


class DensityMap:

    def generate(

        self,

        detections,

        frame_shape
    ):

        density = np.zeros(

            frame_shape[:2]
        )

        for detection in detections:

            x1, y1, x2, y2 = detection[
                "bbox"
            ]

            density[
                y1:y2,
                x1:x2
            ] += 1

        return density