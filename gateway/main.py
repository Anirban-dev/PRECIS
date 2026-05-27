from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from websocket_gateway import websocket_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("gateway-main")

app = FastAPI(
    title="PRECIS Gateway",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(websocket_router)

@app.get("/")
async def root():

    logger.info(
        "PRECIS Gateway initialized."
    )

    return {

        "system": "PRECIS",

        "status": "ACTIVE"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )