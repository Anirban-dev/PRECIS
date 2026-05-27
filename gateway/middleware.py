from fastapi import Request
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-middleware"
)


async def request_logging_middleware(

    request: Request,

    call_next
):

    start_time = time.time()

    response = await call_next(
        request
    )

    duration = round(

        time.time() - start_time,

        4
    )

    logger.info(

        f"{request.method} "

        f"{request.url.path} "

        f"{duration}s"
    )

    return response