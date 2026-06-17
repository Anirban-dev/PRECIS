from fastapi import APIRouter

from backend.security.jwt_handler import (
    create_access_token
)

from backend.api.schemas.auth_schema import (
    LoginRequest
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(
    request: LoginRequest
):

    token = create_access_token(

        {
            "sub": request.username
        }
    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "username": request.username
    }