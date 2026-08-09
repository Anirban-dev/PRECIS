from fastapi import APIRouter, Depends

from backend.api.schemas.camera_schema import CameraSchema
from backend.api.schemas.camera_response import CameraStatusResponse
from backend.api.schemas.camera_health_response import CameraHealthResponse
from backend.api.schemas.camera_control_response import CameraControlResponse
from backend.api.schemas.camera_start_request import CameraStartRequest
from backend.services.camera_service import CameraService
from backend.services.camera_health import CameraHealth
from backend.services.camera_registry import CameraRegistry
from backend.services.camera_registry import get_camera_registry
from backend.security.auth_dependency import get_current_user

router = APIRouter(
    prefix="/camera",
    tags=["Camera"]
)

camera_service = CameraService()
health = CameraHealth()
camera_registry = get_camera_registry()


@router.post("/register")
async def register_camera(camera: CameraSchema):
    return camera_registry.register(
        camera.camera_id,
        camera.stream_url,
        camera.sector_id,
        camera.camera_type
    )


@router.get("/list")
async def list_cameras():
    return camera_registry.all()


@router.post(
    "/start",
    response_model=CameraControlResponse
)
async def start_camera(
    payload: CameraStartRequest,
    user=Depends(get_current_user)
):
    return camera_service.start_camera(payload.camera_id)


@router.post(
    "/stop",
    response_model=CameraControlResponse
)
async def stop_camera(user=Depends(get_current_user)):
    return camera_service.stop()


@router.get(
    "/status",
    response_model=CameraStatusResponse
)
async def camera_runtime_status():
    return camera_service.status()


@router.get("/status/{camera_id}")
async def camera_status(camera_id: str):
    status = camera_service.status()
    return {
        "camera_id": camera_id,
        "status": "HEALTHY",
        "running": status["running"]
    }


@router.get(
    "/health",
    response_model=CameraHealthResponse
)
async def camera_health():
    status = camera_service.status()
    return health.check(status["running"])


@router.get("/{camera_id}")
async def get_camera(camera_id: str):
    camera = camera_registry.get(camera_id)

    if not camera:
        return {
            "success": False,
            "message": "Camera not found"
        }

    return camera
