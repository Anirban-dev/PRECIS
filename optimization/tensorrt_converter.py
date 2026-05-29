from pathlib import Path


class TensorRTConverter:

    def __init__(self):

        self.supported_formats = [
            ".onnx"
        ]

    def validate_model(

        self,

        model_path: str
    ):

        path = Path(model_path)

        return (

            path.exists()

            and

            path.suffix in self.supported_formats
        )

    def convert(

        self,

        model_path: str
    ):

        if not self.validate_model(
            model_path
        ):

            raise ValueError(
                "Unsupported model format"
            )

        engine_path = model_path.replace(
            ".onnx",
            ".engine"
        )

        return {

            "source": model_path,

            "engine": engine_path,

            "status": "SUCCESS"
        }