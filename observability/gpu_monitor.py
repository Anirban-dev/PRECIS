import torch


class GPUMonitor:

    def stats(self):

        return {

            "cuda":
                torch.cuda.is_available(),

            "devices":
                torch.cuda.device_count()
        }