import numpy as np

from backend.services.notification_service import (
    NotificationService
)


class SpectralFusion:

    def fuse_density_maps(

        self,

        rgb_density,

        thermal_density,

        rgb_weight=0.55,

        thermal_weight=0.45
    ):

        rgb_density = np.array(
            rgb_density
        )

        thermal_density = np.array(
            thermal_density
        )

        fused = (

            rgb_density * rgb_weight +

            thermal_density * thermal_weight
        )

        return fused.tolist()

    def confidence_adjustment(

        self,

        rgb_confidence,

        thermal_confidence
    ):

        return max(

            rgb_confidence,

            thermal_confidence
        )


class AIToBackend:

    def __init__(self):

        self.notification = (
            NotificationService()
        )

        self.fusion = (
            SpectralFusion()
        )

    def fuse_sector_density(

        self,

        rgb_density,

        thermal_density,

        rgb_confidence,

        thermal_confidence
    ):

        fused_density = (

            self.fusion.fuse_density_maps(

                rgb_density,

                thermal_density
            )
        )

        confidence = (

            self.fusion.confidence_adjustment(

                rgb_confidence,

                thermal_confidence
            )
        )

        return {

            "density_map":
                fused_density,

            "confidence":
                confidence,

            "sensor_mode":
                "RGB_THERMAL_FUSION"
        }

    def send_alert(

        self,

        risk_level,

        message,

        camera_type="RGB"
    ):

        return self.notification.broadcast_alert(

            risk_level,

            {

                "message":
                    message,

                "camera_type":
                    camera_type
            }
        )

    def process_sector(

        self,

        rgb_density,

        thermal_density,

        rgb_confidence,

        thermal_confidence,

        risk_level
    ):

        fusion_result = (

            self.fuse_sector_density(

                rgb_density,

                thermal_density,

                rgb_confidence,

                thermal_confidence
            )
        )

        average_density = (

            np.mean(
                fusion_result[
                    "density_map"
                ]
            )
        )

        if risk_level in [

            "HIGH",

            "CRITICAL"
        ]:

            self.send_alert(

                risk_level,

                f"Sector density anomaly detected: {average_density:.2f}",

                camera_type="RGB_THERMAL"
            )

        return {

            "fusion":
                fusion_result,

            "risk_level":
                risk_level,

            "average_density":
                float(
                    average_density
                )
        }