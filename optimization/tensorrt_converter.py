class TensorRTConverter:

    def convert(

        self,

        model_name
    ):

        return {

            "model":
                model_name,

            "engine":
                "TensorRT",

            "status":
                "CONVERTED"
        }