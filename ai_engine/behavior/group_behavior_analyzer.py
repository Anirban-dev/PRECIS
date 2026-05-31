import numpy as np


class GroupBehaviorAnalyzer:

    def analyze(

        self,

        positions
    ):

        if len(positions) < 2:

            return {

                "group_count": 0,

                "cohesion": 0
            }

        points = np.array(
            positions
        )

        center = np.mean(

            points,

            axis=0
        )

        distances = np.linalg.norm(

            points - center,

            axis=1
        )

        cohesion = float(

            np.mean(
                distances
            )
        )

        return {

            "group_count":
                len(points),

            "cohesion":
                cohesion
        }