from datetime import datetime


class PipelineScheduler:

    def schedule(

        self,

        pipeline
    ):

        return {

            "pipeline":
                pipeline,

            "scheduled_at":
                datetime.utcnow().isoformat()
        }