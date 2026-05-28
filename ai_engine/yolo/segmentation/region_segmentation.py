class RegionSegmentation:

    def split_regions(

        self,

        frame_width,

        frame_height,

        rows,

        cols
    ):

        regions = []

        cell_width = frame_width // cols

        cell_height = frame_height // rows

        for row in range(rows):

            for col in range(cols):

                x1 = col * cell_width

                y1 = row * cell_height

                x2 = x1 + cell_width

                y2 = y1 + cell_height

                regions.append(

                    (x1, y1, x2, y2)
                )

        return regions