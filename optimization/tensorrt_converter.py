class TensorRTConverter:

    def build_dual_engine(

        self,

        rgb_model_path,

        thermal_model_path
    ):

        return {

            "rgb_engine":
                rgb_model_path.replace(
                    ".onnx",
                    ".engine"
                ),

            "thermal_engine":
                thermal_model_path.replace(
                    ".onnx",
                    ".engine"
                ),

            "mode":
                "DUAL_SPECTRAL"
        }