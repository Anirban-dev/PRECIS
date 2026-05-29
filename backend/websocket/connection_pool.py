class ConnectionPool:

    def __init__(self):

        self.connections = {}

    def add(

        self,

        client_id,

        websocket
    ):

        self.connections[
            client_id
        ] = websocket

    def remove(

        self,

        client_id
    ):

        self.connections.pop(
            client_id,
            None
        )

    def get(

        self,

        client_id
    ):

        return self.connections.get(
            client_id
        )

    def count(self):

        return len(
            self.connections
        )