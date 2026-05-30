from pathlib import Path

from ultralytics import YOLO


class ModelLoader:

    def __init__(self):

        self.loaded_models = {}

    def load_model(

        self,

        model_name,

        model_path
    ):

        path = Path(model_path)

        if not path.exists():

            raise FileNotFoundError(

                f"{model_path} not found"
            )

        model = YOLO(model_path)

        self.loaded_models[
            model_name
        ] = model

        return model

    def load_rgb(

        self
    ):

        return self.load_model(

            "rgb",

            "ai_engine/models/weights/rgb_yolov8.pt"
        )

    def load_thermal(

        self
    ):

        return self.load_model(

            "thermal",

            "ai_engine/models/weights/thermal_yolov8.pt"
        )

    def load_infrared(

        self
    ):

        return self.load_model(

            "infrared",

            "ai_engine/models/weights/infrared_yolov8.pt"
        )

    def get_model(

        self,

        model_name
    ):

        return self.loaded_models.get(
            model_name
        )