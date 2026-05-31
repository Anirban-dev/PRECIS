from pydantic import BaseModel


class CameraSchema(BaseModel):

    camera_id: str

    sector_id: str

    camera_type: str

    stream_url: str