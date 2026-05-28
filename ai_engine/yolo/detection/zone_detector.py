class ZoneDetector:

    def inside_zone(

        self,

        point,

        zone
    ):

        x, y = point

        x1, y1, x2, y2 = zone

        return (

            x1 <= x <= x2 and

            y1 <= y <= y2
        )

    def detect_zone_intrusion(

        self,

        tracks,

        zone
    ):

        intrusions = []

        for track in tracks:

            bbox = track["bbox"]

            center_x = int(

                (bbox[0] + bbox[2]) / 2
            )

            center_y = int(

                (bbox[1] + bbox[3]) / 2
            )

            if self.inside_zone(

                (center_x, center_y),

                zone
            ):

                intrusions.append(track)

        return intrusions