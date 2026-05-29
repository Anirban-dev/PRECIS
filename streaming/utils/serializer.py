import json


class Serializer:

    def encode(

        self,

        payload
    ):

        return json.dumps(
            payload
        )

    def decode(

        self,

        payload
    ):

        return json.loads(
            payload
        )