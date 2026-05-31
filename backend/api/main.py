from fastapi import FastAPI

from backend.api.routes.analytics_routes import (
    router as analytics_router
)

from backend.api.routes.risk_routes import (
    router as risk_router
)

from backend.api.routes.emergency_routes import (
    router as emergency_router
)

from backend.api.routes.auth_routes import (
    router as auth_router
)

# 1. Added the new camera routes import
from backend.api.routes.camera_routes import (
    router as camera_router
)

app = FastAPI(
    title="PRECIS API"
)

app.include_router(
    analytics_router
)

app.include_router(
    risk_router
)

app.include_router(
    emergency_router
)

app.include_router(
    auth_router
)

# 2. Included the camera router into the FastAPI app instance
app.include_router(
    camera_router
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }