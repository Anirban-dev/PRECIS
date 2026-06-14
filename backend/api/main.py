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

from backend.api.routes.camera_routes import (
    router as camera_router
)

from backend.api.routes.predict_routes import (
    router as predict_router
)

from backend.api.routes.websocket_routes import (
    router as websocket_router
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

app.include_router(
    camera_router
)

app.include_router(
    predict_router
)

app.include_router(
    websocket_router
)

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }