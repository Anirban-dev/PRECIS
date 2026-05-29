from pydantic import BaseModel


class WebSocketSchema(BaseModel):

    client_id: str

    event_type: str

    payload: dict