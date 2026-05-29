from backend.security.jwt_handler import (
    verify_token
)


class WebSocketSecurity:

    def authorize(

        self,

        token
    ):

        try:

            verify_token(token)

            return True

        except Exception:

            return False