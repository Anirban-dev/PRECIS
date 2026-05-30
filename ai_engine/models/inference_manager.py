from ai_engine.models.model_registry import (
    ModelRegistry
)


class InferenceManager:

    def __init__(self):

        self.registry = ModelRegistry()

        self.registry.initialize()

    def predict(

        self,

        model_name,

        frame
    ):

        model = self.registry.get_model(
            model_name
        )

        if model is None:

            raise ValueError(
                f"{model_name} not loaded"
            )

        return model.predict(
            source=frame,
            verbose=False
        )