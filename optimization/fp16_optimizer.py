import torch


class FP16Optimizer:

    def optimize(

        self,

        model
    ):

        if torch.cuda.is_available():

            model = model.half()

        return model

    def info(self):

        return {

            "fp16_enabled":

                torch.cuda.is_available()
        }