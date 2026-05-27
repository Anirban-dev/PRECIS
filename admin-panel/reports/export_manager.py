import json
from datetime import datetime


class ExportManager:

    def export_json(

        self,

        payload,

        filename
    ):

        file_path = (
            f"{filename}.json"
        )

        with open(

            file_path,

            "w",

            encoding="utf-8"
        ) as file:

            json.dump(

                payload,

                file,

                indent=4
            )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "status": "EXPORTED",

            "file": file_path
        }