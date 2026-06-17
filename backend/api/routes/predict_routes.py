from fastapi import APIRouter, Depends
from system_integration.predictive_pipeline import PredictivePipeline
from backend.api.routes.websocket_routes import manager
from backend.api.schemas.predict_schema import PredictRequest
from backend.security.auth_dependency import get_current_user
from backend.services.incident_service import IncidentService
from backend.services.alert_service import AlertService
import traceback

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

pipeline = PredictivePipeline()
incident_service = IncidentService()
alert_service = AlertService()

@router.post("/")
async def predict(
    payload: PredictRequest,
    user=Depends(get_current_user)
):
    try:
        result = pipeline.execute(
            rgb_density=payload.rgb_density,
            thermal_density=payload.thermal_density,
            infrared_density=payload.infrared_density,
            flow_vectors=payload.flow_vectors,
            turbulence_score=payload.turbulence_score
        )

        risk_level = result["risk"]["risk_level"]

        if risk_level in ["MEDIUM", "HIGH"]:
            incident_service.create_incident(
                camera_id="gate_a",
                density=len(payload.rgb_density),
                risk_level=risk_level
            )

            alert = alert_service.create_alert(
                camera_id="gate_a",
                risk_level=risk_level
            )

            await manager.broadcast(
                {
                    "event": "alert",
                    "data": alert
                }
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
