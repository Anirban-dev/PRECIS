# cv_engine/pipeline_orchestrator.py

import cv2
import logging
import numpy as np
from pathlib import Path
from datetime import datetime

# =========================================================
# IMPORT ENGINES
# =========================================================

from cv_engine.optical_flow.optical_flow import (
    OpticalFlowEngine
)

from cv_engine.optical_flow.motion_vectors import (
    MotionVectorEngine
)

from cv_engine.optical_flow.turbulence_metrics import (
    TurbulenceMetricsEngine
)

from cv_engine.optical_flow.crowd_wave_detector import (
    CrowdWaveDetector
)

from cv_engine.optical_flow.resonance_engine import (
    ResonanceEngine
)

from cv_engine.optical_flow.heatmap_generator import (
    HeatmapGenerator
)

from cv_engine.optical_flow.flow_visualizer import (
    FlowVisualizer
)

from cv_engine.optical_flow.risk_scoring import (
    CrowdRiskScoringEngine
)

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("pipeline-orchestrator")

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = "cv_engine/outputs/processed_videos"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# =========================================================
# PIPELINE ORCHESTRATOR
# =========================================================

class PipelineOrchestrator:

    def __init__(self):

        logger.info(
            "Initializing PRECIS Pipeline Orchestrator..."
        )

        # -------------------------------------------------
        # ENGINE INITIALIZATION
        # -------------------------------------------------

        self.optical_engine = OpticalFlowEngine()

        self.motion_engine = MotionVectorEngine()

        self.turbulence_engine = (
            TurbulenceMetricsEngine()
        )

        self.wave_detector = CrowdWaveDetector()

        self.resonance_engine = ResonanceEngine()

        self.heatmap_generator = HeatmapGenerator()

        self.flow_visualizer = FlowVisualizer()

        self.risk_engine = CrowdRiskScoringEngine()

    # =====================================================
    # RUN COMPLETE PIPELINE
    # =====================================================

    def run_pipeline(
        self,
        video_path,
        display=True
    ):

        logger.info(
            f"Starting pipeline for: {video_path}"
        )

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():

            raise Exception(
                f"Unable to open video: {video_path}"
            )

        # -------------------------------------------------
        # FIRST FRAME
        # -------------------------------------------------

        ret, first_frame = cap.read()

        if not ret:

            raise Exception(
                "Unable to read initial frame."
            )

        previous_gray = cv2.cvtColor(
            first_frame,
            cv2.COLOR_BGR2GRAY
        )

        frame_count = 0

        # =================================================
        # PROCESS LOOP
        # =================================================

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            current_gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # -------------------------------------------------
            # OPTICAL FLOW
            # -------------------------------------------------

            flow = cv2.calcOpticalFlowFarneback(

                previous_gray,

                current_gray,

                None,

                pyr_scale=0.5,

                levels=3,

                winsize=15,

                iterations=3,

                poly_n=5,

                poly_sigma=1.2,

                flags=0
            )

            # -------------------------------------------------
            # MOTION VECTORS
            # -------------------------------------------------

            motion_metrics = (
                self.motion_engine.extract_vectors(
                    flow
                )
            )

            # -------------------------------------------------
            # TURBULENCE ANALYSIS
            # -------------------------------------------------

            turbulence_metrics = (
                self.turbulence_engine
                .calculate_metrics(flow)
            )

            # -------------------------------------------------
            # CROWD WAVE ANALYSIS
            # -------------------------------------------------

            wave_metrics = (
                self.wave_detector
                .analyze_wave_patterns(flow)
            )

            # -------------------------------------------------
            # RESONANCE ENGINE
            # -------------------------------------------------

            resonance_metrics = (
                self.resonance_engine
                .calculate_resonance(
                    motion_metrics,
                    turbulence_metrics,
                    wave_metrics
                )
            )

            # -------------------------------------------------
            # MAGNITUDE EXTRACTION
            # -------------------------------------------------

            magnitude = np.sqrt(

                flow[..., 0] ** 2
                +
                flow[..., 1] ** 2
            )

            # -------------------------------------------------
            # HEATMAP GENERATION
            # -------------------------------------------------

            heatmap_frame = (
                self.heatmap_generator
                .generate_heatmap(
                    magnitude,
                    frame
                )
            )

            # -------------------------------------------------
            # FLOW VISUALIZATION
            # -------------------------------------------------

            visual_frame = (
                self.flow_visualizer
                .draw_flow_vectors(
                    heatmap_frame,
                    flow
                )
            )

            # -------------------------------------------------
            # FINAL RISK ANALYSIS
            # -------------------------------------------------

            risk_report = (
                self.risk_engine
                .calculate_risk_score(

                    person_count=80,

                    turbulence_metrics=
                    turbulence_metrics,

                    wave_metrics=
                    wave_metrics,

                    audio_stress_level=0.3,

                    screaming_detected=False
                )
            )

            # -------------------------------------------------
            # OVERLAY FINAL ANALYTICS
            # -------------------------------------------------

            visual_frame = (
                self.flow_visualizer.draw_analytics(

                    visual_frame,

                    avg_motion=np.mean(magnitude),

                    turbulence_score=
                    turbulence_metrics[
                        "turbulence_score"
                    ],

                    resonance_score=
                    resonance_metrics[
                        "resonance_score"
                    ]
                )
            )

            # -------------------------------------------------
            # RISK DISPLAY
            # -------------------------------------------------

            cv2.putText(

                visual_frame,

                f"Risk: "
                f"{risk_report['risk_level']}",

                (20, 160),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 0, 255),

                2
            )

            # -------------------------------------------------
            # DISPLAY WINDOW
            # -------------------------------------------------

            if display:

                cv2.imshow(
                    "PRECIS Crowd Intelligence",
                    visual_frame
                )

            # -------------------------------------------------
            # UPDATE FRAME
            # -------------------------------------------------

            previous_gray = current_gray

            # -------------------------------------------------
            # EXIT
            # -------------------------------------------------

            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):

                logger.info(
                    "Pipeline manually stopped."
                )

                break

        # =================================================
        # RELEASE RESOURCES
        # =================================================

        cap.release()

        cv2.destroyAllWindows()

        logger.info(
            "Pipeline execution completed."
        )

        return {

            "status": "success",

            "frames_processed": frame_count,

            "timestamp": datetime.utcnow()
            .isoformat()
        }

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    VIDEO_PATH = (
        "datasets/sample_videos/crowd_video.mp4"
    )

    try:

        orchestrator = PipelineOrchestrator()

        result = orchestrator.run_pipeline(

            video_path=VIDEO_PATH,

            display=True
        )

        print(
            "\n========== PIPELINE REPORT ==========\n"
        )

        for key, value in result.items():

            print(f"{key}: {value}")

    except Exception as e:

        logger.error(
            f"Pipeline Orchestrator Error: {e}"
        )