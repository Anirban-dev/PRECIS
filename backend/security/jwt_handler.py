from datetime import datetime, timedelta


class JWTHandler:

    SECRET_KEY = "precis-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def create_access_token(data: dict):

        payload = data.copy()

        payload["exp"] = (
            datetime.utcnow()
            + timedelta(
                minutes=JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        ).isoformat()

        return f"mock-jwt-token-{payload}"

    @staticmethod
    def verify_token(token: str):

        if not token:
            return None

        return {
            "valid": True,
            "token": token
        }

    @staticmethod
    def decode_token(token: str):

        return {
            "valid": True,
            "token": token
        }


def create_access_token(data: dict):

    return JWTHandler.create_access_token(data)


def verify_token(token: str):

    return JWTHandler.verify_token(token)


def decode_token(token: str):

    return JWTHandler.decode_token(token)