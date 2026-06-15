from fastapi import APIRouter

from backend.api.schemas.camera_schema import (
    CameraSchema
)

router = APIRouter(
    prefix="/camera",
    tags=["Camera"]
)

camera_state = {
    "running": False
}


@router.post("/register")
async def register_camera(

    camera: CameraSchema
):

    return {

        "status": "registered",

        "camera": camera
    }


@router.post("/start")
async def start_camera():

    if camera_state["running"]:

        return {

            "success": False,

            "message":
                "Camera already running"
        }

    camera_state["running"] = True

    return {

        "success": True,

        "message":
            "Camera started"
    }


@router.post("/stop")
async def stop_camera():

    if not camera_state["running"]:

        return {

            "success": False,

            "message":
                "Camera already stopped"
        }

    camera_state["running"] = False

    return {

        "success": True,

        "message":
            "Camera stopped"
    }


@router.get("/status")
async def camera_runtime_status():

    return {

        "running":
            camera_state["running"]
    }


@router.get("/status/{camera_id}")
async def camera_status(

    camera_id: str
):

    return {

        "camera_id":
            camera_id,

        "status":
            "HEALTHY",

        "running":
            camera_state["running"]
    }