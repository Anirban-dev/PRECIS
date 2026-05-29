from pydantic import BaseModel
from datetime import datetime


class EventSchema(BaseModel):

    event_type: str

    payload: dict

    timestamp: datetime