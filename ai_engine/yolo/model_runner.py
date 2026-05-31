from ultralytics import YOLO


class YOLOModelRunner:

    def __init__(

        self,

        model_path
    ):

        self.model = YOLO(
            model_path
        )

    def detect(

        self,

        frame
    ):

        results = self.model.predict(

            source=frame,

            verbose=False
        )

        return results