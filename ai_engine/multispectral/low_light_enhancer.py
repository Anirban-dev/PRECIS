import cv2


class LowLightEnhancer:

    def enhance(

        self,

        frame
    ):

        lab = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2LAB
        )

        l, a, b = cv2.split(
            lab
        )

        clahe = cv2.createCLAHE(

            clipLimit=3.0,

            tileGridSize=(8, 8)
        )

        enhanced_l = clahe.apply(
            l
        )

        merged = cv2.merge(

            [
                enhanced_l,
                a,
                b
            ]
        )

        return cv2.cvtColor(

            merged,

            cv2.COLOR_LAB2BGR
        )

    def brightness(

        self,

        frame
    ):

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        return float(
            gray.mean()
        )