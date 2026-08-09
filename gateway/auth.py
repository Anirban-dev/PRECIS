import logging

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.security.jwt_handler import create_access_token, verify_token

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("gateway-auth")
security = HTTPBearer()


class AuthManager:
    def create_access_token(self, user_id):
        token = create_access_token({"sub": user_id})
        logger.info("Token generated for %s", user_id)
        return token

    def verify_token(self, token):
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return payload


auth_manager = AuthManager()


async def authenticate(credentials: HTTPAuthorizationCredentials = security):
    return auth_manager.verify_token(credentials.credentials)
