import torch


class GPUManager:

    def gpu_available(self):

        return torch.cuda.is_available()

    def device_count(self):

        return torch.cuda.device_count()

    def current_device(self):

        if torch.cuda.is_available():

            return torch.cuda.get_device_name(0)

        return "CPU"