from ai_engine.models.model_loader import (
    ModelLoader
)


class ModelRegistry:

    def __init__(self):

        self.loader = ModelLoader()

        self.registry = {}

    def initialize(self):

        self.registry["rgb"] = (

            self.loader.load_rgb()
        )

        self.registry["thermal"] = (

            self.loader.load_thermal()
        )

        self.registry["infrared"] = (

            self.loader.load_infrared()
        )

    def get(

        self,

        model_type
    ):

        return self.registry.get(
            model_type
        )

    def available_models(self):

        return list(

            self.registry.keys()
        )