from ai_engine.models.model_registry import (
    ModelRegistry
)


registry = ModelRegistry()

registry.initialize()

print(

    registry.available_models()
)