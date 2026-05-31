from fastapi import APIRouter

from backend.services.risk_service import (
    RiskService
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)

risk_service = RiskService()


@router.post("/evaluate")
async def evaluate_risk(payload: dict):

    return risk_service.calculate_risk(

        density_map=payload["density_map"],

        turbulence_score=payload[
            "turbulence_score"
        ],

        fusion_confidence=payload[
            "fusion_confidence"
        ],

        sensor_health=payload[
            "sensor_health"
        ]
    )