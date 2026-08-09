import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


class JWTHandler:

    SECRET_KEY = os.getenv("PRECIS_JWT_SECRET", "precis-dev-secret-change-me")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("PRECIS_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    @staticmethod
    def create_access_token(data: dict):

        payload = data.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload["exp"] = int(expires_at.timestamp())
        payload["iat"] = int(datetime.now(timezone.utc).timestamp())

        header = {
            "alg": JWTHandler.ALGORITHM,
            "typ": "JWT"
        }
        encoded_header = _b64encode(
            json.dumps(header, separators=(",", ":")).encode("utf-8")
        )
        encoded_payload = _b64encode(
            json.dumps(payload, separators=(",", ":")).encode("utf-8")
        )
        signing_input = f"{encoded_header}.{encoded_payload}"
        signature = hmac.new(
            JWTHandler.SECRET_KEY.encode("utf-8"),
            signing_input.encode("ascii"),
            hashlib.sha256
        ).digest()

        return f"{signing_input}.{_b64encode(signature)}"

    @staticmethod
    def verify_token(token: str):
        try:
            return JWTHandler.decode_token(token)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None

    @staticmethod
    def decode_token(token: str):
        if not token:
            raise ValueError("Missing token")

        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        signing_input = f"{parts[0]}.{parts[1]}"
        expected_signature = hmac.new(
            JWTHandler.SECRET_KEY.encode("utf-8"),
            signing_input.encode("ascii"),
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(_b64encode(expected_signature), parts[2]):
            raise ValueError("Invalid token signature")

        payload = json.loads(_b64decode(parts[1]).decode("utf-8"))
        exp = payload.get("exp")
        if not isinstance(exp, int):
            raise ValueError("Missing token expiry")

        if exp < int(datetime.now(timezone.utc).timestamp()):
            raise ValueError("Token expired")

        return payload


def create_access_token(data: dict):

    return JWTHandler.create_access_token(data)


def verify_token(token: str):

    return JWTHandler.verify_token(token)


def decode_token(token: str):

    return JWTHandler.decode_token(token)
