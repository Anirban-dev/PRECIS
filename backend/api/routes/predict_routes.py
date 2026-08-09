import logging

from fastapi import APIRouter, Depends, HTTPException
from system_integration.predictive_pipeline import PredictivePipeline
from backend.api.routes.websocket_routes import manager
from backend.api.schemas.predict_schema import PredictRequest
from backend.api.schemas.predict_response import PredictResponse
from backend.security.auth_dependency import get_current_user
from backend.services.incident_service import IncidentService
from backend.services.alert_service import AlertService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

pipeline = PredictivePipeline()
incident_service = IncidentService()
alert_service = AlertService()

@router.post("/", response_model=PredictResponse, operation_id="run_prediction")
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

        if risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
            incident = incident_service.create_incident(
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
                    "data": alert,
                    "incident": incident
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

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Prediction pipeline failed")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction pipeline failed: {type(e).__name__}"
        ) from e
