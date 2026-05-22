import logging
from datetime import datetime
from collections import deque
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("digital-twin-manager")

class DigitalTwinManager:
    def __init__(self, environment_id: str, history_limit: int = 100):
        logger.info(f"Initializing Digital Twin for environment: {environment_id}")
        self.environment_id = environment_id
        self.state_history = deque(maxlen=history_limit)
        self.current_state = {
            "timestamp": None,
            "agent_positions": np.array([]),
            "agent_velocities": np.array([]),
            "density_map": np.zeros((20, 20)),
            "active_alerts": []
        }

    def ingest_telemetry(self, sensor_data: dict) -> bool:
        """
        Updates the twin's state with real-world IoT/Camera feeds.
        """
        try:
            timestamp = sensor_data.get("timestamp", datetime.utcnow().isoformat())
            positions = np.array(sensor_data.get("agent_positions", []))
            velocities = np.array(sensor_data.get("agent_velocities", []))
            density_map = np.array(sensor_data.get("density_map", np.zeros((20, 20))))

            self.current_state = {
                "timestamp": timestamp,
                "agent_positions": positions,
                "agent_velocities": velocities,
                "density_map": density_map,
                "active_alerts": self._evaluate_thresholds(density_map)
            }
            
            self.state_history.append(self.current_state)
            logger.debug(f"Telemetry ingested successfully at {timestamp}")
            return True

        except Exception as e:
            logger.error(f"Failed to ingest telemetry data: {e}")
            return False

    def _evaluate_thresholds(self, density_map: np.ndarray) -> list:
        alerts = []
        max_density = np.max(density_map)
        if max_density > 6.0:
            alerts.append(f"CRITICAL: Localized density exceeded 6.0 p/m^2 (Current: {max_density:.2f})")
        return alerts

    def get_historical_trend(self, metric: str, window: int = 10) -> np.ndarray:
        """
        Retrieves a time-series trend for a specific metric to feed predictive engines.
        """
        if len(self.state_history) < window:
            window = len(self.state_history)
        
        recent_states = list(self.state_history)[-window:]
        if metric == "max_density":
            return np.array([np.max(state["density_map"]) for state in recent_states])
        elif metric == "mean_velocity":
            return np.array([np.mean(np.linalg.norm(state["agent_velocities"], axis=1)) 
                             if len(state["agent_velocities"]) > 0 else 0.0 
                             for state in recent_states])
        return np.array([])

    def export_state_snapshot(self) -> dict:
        logger.info("Exporting current digital twin state snapshot.")
        return self.current_state

if __name__ == "__main__":
    twin = DigitalTwinManager(environment_id="STADIUM_SEC_A")
    mock_sensor_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_positions": np.random.rand(50, 2) * 100,
        "agent_velocities": np.random.randn(50, 2),
        "density_map": np.random.uniform(0, 7, (20, 20))
    }
    twin.ingest_telemetry(mock_sensor_data)
    print(f"Twin Alerts: {twin.current_state['active_alerts']}")