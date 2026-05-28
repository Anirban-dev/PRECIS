import cv2


class FaceBlur:

    def blur_faces(

        self,

        frame,

        detections
    ):

        for detection in detections:

            x1, y1, x2, y2 = detection

            face = frame[
                y1:y2,
                x1:x2
            ]

            blurred = cv2.GaussianBlur(

                face,

                (99, 99),

                30
            )

            frame[
                y1:y2,
                x1:x2
            ] = blurred

        return frame