import cv2


class CrowdSegmentation:

    def segment(

        self,

        frame
    ):

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        _, mask = cv2.threshold(

            gray,

            120,

            255,

            cv2.THRESH_BINARY
        )

        return mask