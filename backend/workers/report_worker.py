from datetime import datetime


class ReportWorker:

    def generate_report(

        self,

        incidents
    ):

        return {

            "generated_at":
                datetime.utcnow().isoformat(),

            "total_incidents":
                len(incidents),

            "incidents":
                incidents
        }