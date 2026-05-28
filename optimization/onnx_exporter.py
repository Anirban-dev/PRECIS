class ONNXExporter:

    def export(

        self,

        model_name
    ):

        return {

            "model":
                model_name,

            "format":
                "ONNX",

            "status":
                "EXPORTED"
        }