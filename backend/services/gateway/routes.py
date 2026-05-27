from fastapi import APIRouter, HTTPException
from datetime import datetime

from gateway.services import GatewayService
from gateway.schemas import (

    CrowdRiskRequest,
    FusionRequest,
    EmergencyAlertRequest
)

router = APIRouter()

service = GatewayService()


@router.get("/health")

async def health_check():

    return {

        "status": "online",

        "service": "PRECIS Gateway",

        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/risk/analyze")

async def analyze_risk(

    payload: CrowdRiskRequest
):

    try:

        result = service.process_risk_analysis(
            payload.dict()
        )

        return {

            "success": True,

            "data": result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


@router.post("/fusion/process")

async def process_fusion(

    payload: FusionRequest
):

    try:

        result = service.process_fusion(
            payload.dict()
        )

        return {

            "success": True,

            "data": result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


@router.post("/emergency/dispatch")

async def dispatch_emergency(

    payload: EmergencyAlertRequest
):

    try:

        result = service.dispatch_emergency(
            payload.dict()
        )

        return {

            "success": True,

            "data": result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


@router.get("/system/status")

async def system_status():

    return {

        "system": "PRECIS",

        "gateway": "active",

        "cv_engine": "connected",

        "ai_engine": "connected",

        "event_bus": "connected",

        "dashboard": "active",

        "timestamp":
            datetime.utcnow().isoformat()
    }


@router.get("/analytics/live")

async def live_analytics():

    return {

        "crowd_state": "STABLE",

        "risk_level": "LOW",

        "active_alerts": 0,

        "shockwave_detected": False,

        "resonance_probability": 0.14,

        "timestamp":
            datetime.utcnow().isoformat()
    }


@router.get("/emergency/status")

async def emergency_status():

    return {

        "ambulance_network": "READY",

        "hospital_alert_system": "READY",

        "police_control": "READY",

        "fire_response": "READY",

        "emergency_mode": False,

        "timestamp":
            datetime.utcnow().isoformat()
    }