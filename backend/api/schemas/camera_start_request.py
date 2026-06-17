from pydantic import BaseModel


class CameraStartRequest(BaseModel):

    camera_id: str