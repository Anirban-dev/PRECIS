import torch


class ONNXExporter:

    def export(

        self,

        model,

        sample_input,

        output_path
    ):

        torch.onnx.export(

            model,

            sample_input,

            output_path,

            export_params=True,

            opset_version=17,

            do_constant_folding=True
        )

        return {

            "path": output_path,

            "status": "EXPORTED"
        }