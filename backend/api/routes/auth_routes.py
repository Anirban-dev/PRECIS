import os

from fastapi import APIRouter, HTTPException

from backend.security.jwt_handler import (
    create_access_token
)

from backend.api.schemas.auth_schema import (
    LoginRequest
)
from backend.api.schemas.auth_response import LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest
):
    expected_username = os.getenv("PRECIS_ADMIN_USERNAME", "admin")
    expected_password = os.getenv("PRECIS_ADMIN_PASSWORD", "admin")

    if (
        request.username != expected_username
        or request.password != expected_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

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
