from fastapi import Header, HTTPException

from backend.security.jwt_handler import (
    verify_token
)


async def get_current_user(

    authorization: str = Header(
        default=None
    )
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header"
        )

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization format"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload