from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "heatmap-streamer"
)


class HeatmapStreamer:

    def __init__(self):

        logger.info(
            "Initializing Heatmap Streamer..."
        )

    def stream_heatmap(

        self,

        heatmap_path
    ):

        payload = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "heatmap":
                heatmap_path,

            "stream_status":
                "ACTIVE"
        }

        logger.info(

            f"[HEATMAP STREAM] "

            f"{heatmap_path}"
        )

        return payload
    