from pydantic import BaseModel


class StreamSchema(BaseModel):

    source: str

    stream_id: str

    active: bool