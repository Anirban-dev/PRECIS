import importlib

import pytest
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.services.incident_service import IncidentService


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_incident_store(tmp_path, monkeypatch):
    incident_path = tmp_path / "incidents.json"
    monkeypatch.setattr(IncidentService, "FILE_PATH", incident_path)
    IncidentService().clear()
    yield


@pytest.fixture()
def auth_header():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_auth_login_rejects_arbitrary_password():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_analytics_health_and_crowd():
    health = client.get("/analytics/health")
    assert health.status_code == 200

    response = client.post(
        "/analytics/crowd",
        json={
            "rgb_density": [10, 20, 30],
            "thermal_density": [15, 25, 35],
            "infrared_density": [12, 22, 32],
        },
    )
    assert response.status_code == 200
    assert response.json()["overall_density"] == 21.5


def test_predict_creates_critical_incident_and_dashboard(auth_header, monkeypatch):
    predict_routes = importlib.import_module("backend.api.routes.predict_routes")

    def critical_prediction(**kwargs):
        return {
            "crowd_flow": "MIXED",
            "optical_flow": {"avg_velocity": 5, "max_velocity": 8, "flow_direction": "SURGE"},
            "shockwave": {"shockwave_detected": True, "severity": "HIGH"},
            "panic": {"panic_score": 100},
            "forecast": {"pressure_score": 100},
            "prediction": {"stampede_risk": "CRITICAL"},
            "risk": {
                "risk_score": 100,
                "risk_level": "CRITICAL",
                "sensor_health": "HEALTHY",
                "fusion_confidence": 0.95,
            },
        }

    monkeypatch.setattr(predict_routes.pipeline, "execute", critical_prediction)

    response = client.post(
        "/predict/",
        headers=auth_header,
        json={
            "rgb_density": [100, 100, 100],
            "thermal_density": [100, 100, 100],
            "infrared_density": [100, 100, 100],
            "flow_vectors": [[100, 100], [100, 100]],
            "turbulence_score": 100,
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["result"]["risk"]["risk_level"] == "CRITICAL"

    incidents = client.get("/incidents/")
    assert incidents.status_code == 200
    assert incidents.json()["count"] == 1
    assert incidents.json()["incidents"][0]["risk_level"] == "CRITICAL"

    dashboard = client.get("/dashboard/summary")
    assert dashboard.status_code == 200
    assert dashboard.json()["critical_risk"] == 1
    assert dashboard.json()["high_risk"] == 1


def test_emergency_validation_and_critical_recommendation():
    invalid = client.post("/emergency/recommend", json={})
    assert invalid.status_code == 422

    response = client.post(
        "/emergency/recommend",
        json={
            "risk_level": "CRITICAL",
            "sector_id": "A",
            "sensor_health": "HEALTHY",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["priority"] == "IMMEDIATE"
    assert body["recommendations"]


def test_camera_registry_start_status(auth_header, monkeypatch):
    camera_routes = importlib.import_module("backend.api.routes.camera_routes")
    camera_service = camera_routes.camera_service

    class FakeProcess:
        pid = 1234

        def __init__(self):
            self.terminated = False

        def poll(self):
            return None if not self.terminated else 0

        def terminate(self):
            self.terminated = True

    monkeypatch.setattr(
        "backend.services.camera_service.subprocess.Popen",
        lambda *args, **kwargs: FakeProcess(),
    )
    camera_service.process = None

    registered = client.post(
        "/camera/register",
        json={
            "camera_id": "cam1",
            "sector_id": "A",
            "camera_type": "CCTV",
            "stream_url": "rtsp://test",
        },
    )
    assert registered.status_code == 200

    listed = client.get("/camera/list")
    assert listed.status_code == 200
    assert any(camera["camera_id"] == "cam1" for camera in listed.json()["cameras"])

    lookup = client.get("/camera/cam1")
    assert lookup.status_code == 200
    assert lookup.json()["stream_url"] == "rtsp://test"

    started = client.post(
        "/camera/start",
        headers=auth_header,
        json={"camera_id": "cam1"},
    )
    assert started.status_code == 200
    assert started.json()["success"] is True
    assert started.json()["pid"] == 1234

    status = client.get("/camera/status")
    assert status.status_code == 200
    assert status.json()["running"] is True


def test_gateway_routes(monkeypatch):
    gateway_routes = importlib.import_module("gateway.routes")
    gateway_app_module = importlib.import_module("gateway.main")
    gateway_client = TestClient(gateway_app_module.app)

    monkeypatch.setattr(
        gateway_routes.service,
        "_forward",
        lambda path, payload: {"forwarded": True, "path": path},
    )

    assert gateway_client.get("/api/health").status_code == 200

    event = gateway_client.post(
        "/api/event",
        json={
            "event_id": "evt1",
            "event_type": "crowd",
            "timestamp": "2026-08-08T00:00:00",
            "location": "A",
        },
    )
    assert event.status_code == 200

    risk = gateway_client.post(
        "/api/risk",
        json={
            "risk_score": 95,
            "risk_level": "CRITICAL",
            "crowd_density": 100,
            "turbulence_score": 100,
        },
    )
    assert risk.status_code == 200
    assert risk.json()["backend"]["forwarded"] is True

    alert = gateway_client.post(
        "/api/alert",
        json={
            "alert_id": "alert1",
            "responders": ["security"],
            "alert_level": "CRITICAL",
            "active": True,
        },
    )
    assert alert.status_code == 200
