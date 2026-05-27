from fastapi import Request
from fastapi.responses import JSONResponse
import logging
import time
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "gateway-middleware"
)


async def logging_middleware(

    request: Request,

    call_next
):

    start_time = time.time()

    logger.info(

        f"[REQUEST] "

        f"{request.method} "

        f"{request.url.path}"
    )

    response = await call_next(request)

    process_time = round(

        time.time() - start_time,

        4
    )

    logger.info(

        f"[RESPONSE] "

        f"{request.method} "

        f"{request.url.path} "

        f"Status={response.status_code} "

        f"Time={process_time}s"
    )

    response.headers[
        "X-Process-Time"
    ] = str(process_time)

    return response


async def security_headers_middleware(

    request: Request,

    call_next
):

    response = await call_next(request)

    response.headers[
        "X-System"
    ] = "PRECIS"

    response.headers[
        "X-Protection"
    ] = "Crowd-Intelligence"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin"

    return response


async def emergency_mode_middleware(

    request: Request,

    call_next
):

    response = await call_next(request)

    current_hour = datetime.utcnow().hour

    emergency_mode = False

    if current_hour >= 18:

        emergency_mode = True

    response.headers[
        "X-Emergency-Mode"
    ] = str(emergency_mode)

    return response


async def exception_middleware(

    request: Request,

    call_next
):

    try:

        response = await call_next(request)

        return response

    except Exception as e:

        logger.error(

            f"[EXCEPTION] "

            f"{str(e)}"
        )

        return JSONResponse(

            status_code=500,

            content={

                "success": False,

                "error": "Internal Server Error",

                "message": str(e),

                "timestamp":
                    datetime.utcnow().isoformat()
            }
        )