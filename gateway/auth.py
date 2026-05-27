from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from datetime import datetime
from datetime import timedelta
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-auth"
)

SECRET_KEY = "PRECIS_SECRET"

ALGORITHM = "HS256"

security = HTTPBearer()


class AuthManager:

    def create_access_token(

        self,

        user_id
    ):

        payload = {

            "sub": user_id,

            "exp":
                datetime.utcnow() +
                timedelta(hours=2)
        }

        token = jwt.encode(

            payload,

            SECRET_KEY,

            algorithm=ALGORITHM
        )

        logger.info(
            f"Token generated for {user_id}"
        )

        return token

    def verify_token(

        self,

        token
    ):

        try:

            payload = jwt.decode(

                token,

                SECRET_KEY,

                algorithms=[ALGORITHM]
            )

            return payload

        except Exception:

            raise HTTPException(

                status_code=401,

                detail="Invalid token"
            )


auth_manager = AuthManager()


async def authenticate(

    credentials:
    HTTPAuthorizationCredentials = security
):

    token = credentials.credentials

    return auth_manager.verify_token(
        token
    )