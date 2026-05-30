import cv2
import numpy as np
from datetime import datetime


class AdaptiveSpectralProcessor:

    def __init__(self):

        self.low_light_threshold = 45

    def estimate_brightness(

        self,

        frame
    ):

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        return float(
            np.mean(gray)
        )

    def apply_clahe(

        self,

        frame
    ):

        lab = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2LAB
        )

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(

            clipLimit=3.0,

            tileGridSize=(8, 8)
        )

        enhanced_l = clahe.apply(l)

        merged = cv2.merge(

            [enhanced_l, a, b]
        )

        return cv2.cvtColor(

            merged,

            cv2.COLOR_LAB2BGR
        )

    def preprocess(

        self,

        rgb_frame,

        thermal_frame=None
    ):

        brightness = (
            self.estimate_brightness(
                rgb_frame
            )
        )

        if brightness < self.low_light_threshold:

            enhanced_rgb = (
                self.apply_clahe(
                    rgb_frame
                )
            )

            return {

                "mode":
                    "THERMAL_ASSISTED",

                "rgb":
                    enhanced_rgb,

                "thermal":
                    thermal_frame
            }

        return {

            "mode":
                "RGB",

            "rgb":
                rgb_frame,

            "thermal":
                None
        }


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

        spectral_result = (
            self.processor.preprocess(

                rgb_frame,

                thermal_frame
            )
        )

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "spectral_mode":
                spectral_result["mode"],

            "cv_payload":
                cv_payload,

            "ai_payload":
                ai_payload,

            "pipeline":
                "RGB_THERMAL_FUSION",

            "status":
                "PIPELINE_EXECUTED"
        }