from ai_engine.models.model_registry import (
    ModelRegistry
)


class YOLOManager:

    def __init__(self):

        self.registry = (
            ModelRegistry()
        )

        self.registry.initialize()

    def rgb_model(self):

        return self.registry.get_model(
            "rgb"
        )

    def thermal_model(self):

        return self.registry.get_model(
            "thermal"
        )

    def infrared_model(self):

        return self.registry.get_model(
            "infrared"
        )