class ModelRegistry:

    def __init__(self):

        self.models = {}

    def register(

        self,

        name,

        model
    ):

        self.models[name] = model

    def fetch(

        self,

        name
    ):

        return self.models.get(
            name
        )