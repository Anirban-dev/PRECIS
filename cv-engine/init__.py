# cv_engine/__init__.py

"""
=========================================================
PRECIS / NEURAL-SHIELD
Crowd Dynamics & Predictive Risk Intelligence System
=========================================================

cv_engine package initialization.

This package contains:
- Optical Flow Intelligence
- Crowd Turbulence Analysis
- Resonance Detection
- Passive Outstroke Prediction
- Risk Scoring & Alert Systems
- Stream Ingestion Pipelines
- Preprocessing Utilities

Author:
PRECIS R&D Team

=========================================================
"""

__version__ = "1.0.0"

__author__ = "PRECIS R&D Team"

__license__ = "MIT"

# =========================================================
# OPTIONAL PACKAGE EXPORTS
# =========================================================

from .optical_flow.optical_flow import OpticalFlowEngine

from .optical_flow.turbulence_metrics import (
    TurbulenceMetricsEngine
)

from .optical_flow.crowd_wave_detector import (
    CrowdWaveDetector
)

from .optical_flow.risk_scoring import (
    CrowdRiskScoringEngine
)

# =========================================================
# PACKAGE METADATA
# =========================================================

PACKAGE_NAME = "cv_engine"

DESCRIPTION = (
    "Crowd Dynamics & Predictive Motion Intelligence"
)

SUPPORTED_STREAMS = [
    "video",
    "webcam",
    "rtsp"
]

SUPPORTED_ANALYTICS = [
    "optical_flow",
    "turbulence_analysis",
    "wave_detection",
    "resonance_scoring",
    "risk_prediction"
]