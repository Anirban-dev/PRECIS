from fastapi import Header
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import secrets
import jwt
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("gateway-auth")


SECRET_KEY = "PRECIS_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 120

security = HTTPBearer()


class AuthManager:

    def __init__(self):

        logger.info(
            "Initializing Gateway Authentication Manager..."
        )

    def create_access_token(

        self,

        user_id,

        role="operator"
    ):

        expire = datetime.utcnow() + timedelta(

            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {

            "sub": user_id,

            "role": role,

            "exp": expire
        }

        token = jwt.encode(

            payload,

            SECRET_KEY,

            algorithm=ALGORITHM
        )

        logger.info(
            f"Access token generated for {user_id}"
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

            logger.info(
                f"Token verified for "
                f"{payload.get('sub')}"
            )

            return payload

        except jwt.ExpiredSignatureError:

            logger.warning(
                "Expired authentication token."
            )

            raise HTTPException(

                status_code=401,

                detail="Token expired"
            )

        except jwt.InvalidTokenError:

            logger.warning(
                "Invalid authentication token."
            )

            raise HTTPException(

                status_code=401,

                detail="Invalid token"
            )

    def generate_api_key(self):

        api_key = secrets.token_hex(32)

        logger.info(
            "New API key generated."
        )

        return api_key


auth_manager = AuthManager()


async def authenticate_user(

    credentials: HTTPAuthorizationCredentials = security
):

    token = credentials.credentials

    payload = auth_manager.verify_token(
        token
    )

    return payload


async def validate_api_key(

    x_api_key: str = Header(None)
):

    if not x_api_key:

        logger.warning(
            "Missing API key."
        )

        raise HTTPException(

            status_code=401,

            detail="API key missing"
        )

    if len(x_api_key) < 20:

        logger.warning(
            "Invalid API key format."
        )

        raise HTTPException(

            status_code=403,

            detail="Invalid API key"
        )

    logger.info(
        "API key validation successful."
    )

    return True


if __name__ == "__main__":

    try:

        token = auth_manager.create_access_token(

            user_id="precis-admin",

            role="supervisor"
        )

        print(
            "\n========== GENERATED TOKEN ==========\n"
        )

        print(token)

        payload = auth_manager.verify_token(
            token
        )

        print(
            "\n========== VERIFIED PAYLOAD ==========\n"
        )

        print(payload)

        api_key = auth_manager.generate_api_key()

        print(
            "\n========== GENERATED API KEY ==========\n"
        )

        print(api_key)

    except Exception as e:

        logger.error(
            f"Authentication Error: {e}"
        )