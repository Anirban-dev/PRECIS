from datetime import datetime
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(
    "database-writer"
)


class DatabaseWriter:

    def __init__(self):

        self.output_dir = Path(
            "cv-engine/outputs/analytics"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Initializing Database Writer..."
        )

    def store_report(

        self,

        report,

        filename
    ):

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_path = (

            self.output_dir /

            f"{filename}_{timestamp}.json"
        )

        with open(

            file_path,

            "w",

            encoding="utf-8"
        ) as file:

            json.dump(

                report,

                file,

                indent=4
            )

        logger.info(

            f"[DATABASE] "

            f"Stored: {file_path}"
        )

        return str(file_path)