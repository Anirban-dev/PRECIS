import numpy as np


class OccupancyGrid:

    def generate_grid(

        self,

        detections,

        rows,

        cols
    ):

        grid = np.zeros(

            (rows, cols)
        )

        for detection in detections:

            x1, y1, x2, y2 = detection[
                "bbox"
            ]

            grid_x = min(
                cols - 1,
                x1 // 50
            )

            grid_y = min(
                rows - 1,
                y1 // 50
            )

            grid[
                grid_y,
                grid_x
            ] += 1

        return grid