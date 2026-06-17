from pydantic import BaseModel


class CameraHealthResponse(BaseModel):

    healthy: bool

    last_check: str