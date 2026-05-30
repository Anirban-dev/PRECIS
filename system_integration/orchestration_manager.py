from datetime import datetime

from system_integration.cv_to_streaming import (
    AdaptiveSpectralProcessor
)


class OrchestrationManager:

    def __init__(self):

        self.processor = (
            AdaptiveSpectralProcessor()
        )

    def execute_pipeline(

        self,

        rgb_frame,

        thermal_frame,

        cv_payload,

        ai_payload
    ):

        spectral_output = (
            self.processor.preprocess(

                rgb_frame,

                thermal_frame
            )
        )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "spectral_mode":
                spectral_output["mode"],

            "cv":
                cv_payload,

            "ai":
                ai_payload,

            "stream_ready":
                True,

            "status":
                "PIPELINE_EXECUTED"
        }