from fastapi import APIRouter

from backend.api.schemas.camera_schema import (
    CameraSchema
)

router = APIRouter(
    prefix="/camera",
    tags=["Camera"]
)


@router.post("/register")
async def register_camera(

    camera: CameraSchema
):

    return {

        "status": "registered",

        "camera": camera
    }


@router.get("/status/{camera_id}")
async def camera_status(

    camera_id: str
):

    return {

        "camera_id": camera_id,

        "status": "HEALTHY"
    }