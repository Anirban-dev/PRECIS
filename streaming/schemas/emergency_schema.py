from pydantic import BaseModel


class EmergencySchema(BaseModel):

    title: str

    description: str

    priority: str