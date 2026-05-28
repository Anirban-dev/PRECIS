import torch


class CUDAProfiler:

    def profile(self):

        return {

            "cuda_available":
                torch.cuda.is_available(),

            "gpu_count":
                torch.cuda.device_count()
        }