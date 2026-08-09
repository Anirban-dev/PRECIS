from fastapi import APIRouter

from gateway.services import GatewayService
from gateway.schemas import EventSchema
from gateway.schemas import RiskSchema
from gateway.schemas import AlertSchema


router = APIRouter(
    prefix="/api"
)

service = GatewayService()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@router.post("/event")
async def ingest_event(
    payload: EventSchema
):
    return service.process_event(
        payload.dict()
    )


@router.post("/risk")
async def ingest_risk(
    payload: RiskSchema
):
    return service.process_risk(
        payload.dict()
    )


@router.post("/alert")
async def ingest_alert(
    payload: AlertSchema
):
    return service.process_alert(
        payload.dict()
    )