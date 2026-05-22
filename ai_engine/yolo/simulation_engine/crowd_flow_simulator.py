import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("crowd-flow-simulator")

class SocialForceSimulator:
    def __init__(self, time_step: float = 0.1, tau: float = 0.5, A: float = 2000.0, B: float = 0.08):
        logger.info("Initializing Social Force Flow Simulator...")
        self.dt = time_step
        self.tau = tau  # Relaxation time
        self.A = A      # Repulsive interaction strength
        self.B = B      # Repulsive interaction range

    def _compute_driving_force(self, positions: np.ndarray, velocities: np.ndarray, destinations: np.ndarray, desired_speed: float = 1.34) -> np.ndarray:
        direction = destinations - positions
        distances = np.linalg.norm(direction, axis=1, keepdims=True)
        distances[distances == 0] = 1e-5  # Prevent division by zero
        
        desired_velocities = (direction / distances) * desired_speed
        return (desired_velocities - velocities) / self.tau

    def _compute_agent_repulsion(self, positions: np.ndarray) -> np.ndarray:
        num_agents = positions.shape[0]
        repulsive_forces = np.zeros_like(positions)

        # Vectorized pairwise differences and distances
        diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
        distances = np.linalg.norm(diff, axis=2)
        
        np.fill_diagonal(distances, np.inf)  # Ignore self-interaction
        
        # Calculate force magnitude using exponential decay
        force_magnitude = self.A * np.exp(-distances / self.B)
        
        # Normalize direction vectors
        direction = diff / distances[..., np.newaxis]
        
        # Sum forces for each agent
        forces = force_magnitude[..., np.newaxis] * direction
        repulsive_forces = np.sum(forces, axis=1)
        
        return repulsive_forces

    def simulate_step(self, current_positions: np.ndarray, current_velocities: np.ndarray, destinations: np.ndarray) -> dict:
        """
        Advances the crowd simulation by one time step using Euler integration.
        """
        if len(current_positions) == 0:
            return {"positions": current_positions, "velocities": current_velocities}

        # 1. Calculate Forces
        driving_force = self._compute_driving_force(current_positions, current_velocities, destinations)
        repulsive_force = self._compute_agent_repulsion(current_positions)
        
        # Total Acceleration (assuming mass = 1 for all agents)
        acceleration = driving_force + repulsive_force
        
        # 2. Integrate to find new velocities and positions
        new_velocities = current_velocities + acceleration * self.dt
        
        # Cap max speed to realistic human sprinting (approx 5 m/s)
        speeds = np.linalg.norm(new_velocities, axis=1, keepdims=True)
        speeds[speeds == 0] = 1e-5
        new_velocities = np.where(speeds > 5.0, (new_velocities / speeds) * 5.0, new_velocities)
        
        new_positions = current_positions + new_velocities * self.dt

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "positions": new_positions,
            "velocities": new_velocities,
            "mean_velocity": float(np.mean(np.linalg.norm(new_velocities, axis=1)))
        }

if __name__ == "__main__":
    sim = SocialForceSimulator()
    # Mock 100 agents
    positions = np.random.rand(100, 2) * 50
    velocities = np.zeros((100, 2))
    destinations = np.ones((100, 2)) * 25  # All moving to center (25, 25)
    
    result = sim.simulate_step(positions, velocities, destinations)
    print(f"Simulation Step Complete. Mean Velocity: {result['mean_velocity']:.2f} m/s")