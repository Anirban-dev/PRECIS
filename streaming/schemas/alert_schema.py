from pydantic import BaseModel


class AlertSchema(BaseModel):

    title: str

    message: str

    severity: str