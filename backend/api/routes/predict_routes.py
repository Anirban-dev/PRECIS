from fastapi import APIRouter
from system_integration.predictive_pipeline import PredictivePipeline
from backend.api.routes.websocket_routes import manager
import traceback

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

pipeline = PredictivePipeline()


@router.post("/")
async def predict(payload: dict):

    try:

        result = pipeline.execute(

            rgb_density=payload.get(
                "rgb_density",
                [10, 20, 30]
            ),

            thermal_density=payload.get(
                "thermal_density",
                [12, 18, 28]
            ),

            infrared_density=payload.get(
                "infrared_density",
                [11, 19, 27]
            ),

            flow_vectors=payload.get(
                "flow_vectors",
                [
                    [1, 0],
                    [0, 1]
                ]
            ),

            turbulence_score=payload.get(
                "turbulence_score",
                12
            )
        )

        await manager.broadcast(
            {
                "event": "prediction_update",
                "data": result
            }
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error_type": type(e).__name__,
            "error": str(e),
            "traceback": traceback.format_exc()
        }