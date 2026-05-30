import torch


class GPUManager:

    def __init__(self):

        self.cuda_available = (

            torch.cuda.is_available()
        )

    def device(self):

        if self.cuda_available:

            return "cuda"

        return "cpu"

    def gpu_info(self):

        if not self.cuda_available:

            return {

                "device":
                    "cpu",

                "available":
                    False
            }

        return {

            "device":
                torch.cuda.get_device_name(0),

            "available":
                True,

            "count":
                torch.cuda.device_count(),

            "memory_allocated":

                torch.cuda.memory_allocated(0),

            "memory_reserved":

                torch.cuda.memory_reserved(0)
        }

    def move_model(

        self,

        model
    ):

        model.to(
            self.device()
        )

        return model