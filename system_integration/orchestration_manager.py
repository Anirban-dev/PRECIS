class OrchestrationManager:

    def execute_pipeline(

        self,

        cv_payload,

        ai_payload
    ):

        return {

            "cv":
                cv_payload,

            "ai":
                ai_payload,

            "status":
                "PIPELINE_EXECUTED"
        }