from ultralytics import YOLO


class ModelLoader:

    def load_yolo_model(

        self,

        model_path
    ):

        return YOLO(
            model_path
        )