import requests
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "api-client"
)


class APIClient:

    def __init__(

        self,

        base_url="http://localhost:8000"
    ):

        self.base_url = base_url

        logger.info(
            "Initializing API Client..."
        )

    def send_payload(

        self,

        endpoint,

        payload
    ):

        url = f"{self.base_url}/{endpoint}"

        try:

            response = requests.post(

                url,

                json=payload,

                timeout=5
            )

            logger.info(

                f"[API CLIENT] "

                f"Sent payload to {url}"
            )

            return {

                "timestamp":
                    datetime.utcnow().isoformat(),

                "status_code":
                    response.status_code,

                "response":
                    response.json()
            }

        except Exception as e:

            logger.error(
                f"API Error: {e}"
            )

            return {

                "error": str(e)
            }