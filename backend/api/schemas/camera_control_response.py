from pydantic import BaseModel


class CameraControlResponse(BaseModel):
    success: bool
    message: str
    pid: int | None = None
