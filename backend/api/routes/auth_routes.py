from fastapi import APIRouter

from backend.security.jwt_handler import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(payload: dict):

    username = payload.get(
        "username"
    )

    token = create_access_token({

        "sub": username
    })

    return {

        "access_token": token,

        "token_type": "bearer"
    }