import torch


class CUDAProfiler:

    def profile(self):

        if not torch.cuda.is_available():

            return {

                "device": "CPU",

                "memory_allocated": 0
            }

        return {

            "device":

                torch.cuda.get_device_name(0),

            "memory_allocated":

                torch.cuda.memory_allocated(0),

            "memory_reserved":

                torch.cuda.memory_reserved(0)
        }