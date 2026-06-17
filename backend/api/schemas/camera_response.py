from pydantic import BaseModel


class CameraStatusResponse(
    BaseModel
):

    running: bool

    pid: int | None = None