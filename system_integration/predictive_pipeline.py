from ai_engine.multispectral.thermal_detector import (
    ThermalDetector
)

from ai_engine.multispectral.infrared_detector import (
    InfraredDetector
)

from ai_engine.multispectral.spectral_fusion import (
    SpectralFusion
)

from ai_engine.behavior.crowd_flow_classifier import (
    CrowdFlowClassifier
)

from ai_engine.anomaly_detection.panic_score_engine import (
    PanicScoreEngine
)

from cv_engine.simulation.risk_forecaster import (
    RiskForecaster
)

from cv_engine.predictive.stampede_predictor import (
    StampedePredictor
)

from backend.services.risk_service import (
    RiskService
)

from cv_engine.optical_flow.optical_flow_service import (
    OpticalFlowService
)

from cv_engine.shockwave.shockwave_detector import (
    ShockwaveDetector
)


class PredictivePipeline:

    def __init__(self):
        self.thermal_detector = ThermalDetector()
        self.infrared_detector = InfraredDetector()
        self.fusion = SpectralFusion()
        self.flow_classifier = CrowdFlowClassifier()
        self.panic_engine = PanicScoreEngine()
        self.forecaster = RiskForecaster()
        self.predictor = StampedePredictor()
        self.risk_service = RiskService()
        self.optical_flow = OpticalFlowService()
        self.shockwave_detector = ShockwaveDetector()

    def execute(
        self,
        rgb_density,
        thermal_density,
        infrared_density,
        flow_vectors,
        turbulence_score
    ):
        fused_density = self.fusion.fuse_density(
            rgb_density,
            thermal_density,
            infrared_density
        )

        crowd_flow = self.flow_classifier.classify(flow_vectors)

        # Generate Optical Flow Data
        optical_flow = self.optical_flow.analyze()
        shockwave = self.shockwave_detector.detect(
            optical_flow["avg_velocity"]
        )

        # Use Real Shockwave Score
        panic_result = self.panic_engine.calculate(
            density_score=sum(fused_density) / len(fused_density),
            turbulence_score=turbulence_score,
            shockwave_score=50 if shockwave["shockwave_detected"] else 10,
            trajectory_score=20
        )

        forecast = self.forecaster.forecast(
            fused_density,
            flow_vectors
        )

        prediction = self.predictor.predict(
            density_score=panic_result["panic_score"],
            turbulence_score=turbulence_score,
            pressure_score=forecast["pressure_score"],
            panic_score=panic_result["panic_score"]
        )

        risk = self.risk_service.calculate_risk(
            density_map=fused_density,
            turbulence_score=turbulence_score,
            fusion_confidence=0.95,
            sensor_health="HEALTHY"
        )

        # Add Results To Response
        return {
            "crowd_flow": crowd_flow,
            "optical_flow": optical_flow,
            "shockwave": shockwave,
            "panic": panic_result,
            "forecast": forecast,
            "prediction": prediction,
            "risk": risk
        }
