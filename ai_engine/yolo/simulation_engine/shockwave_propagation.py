import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("shockwave-propagation")

class ShockwavePropagationEngine:
    def __init__(self, max_density: float = 7.0, free_flow_speed: float = 1.4):
        logger.info("Initializing Shockwave Propagation Engine...")
        self.rho_max = max_density
        self.v_f = free_flow_speed

    def _calculate_flux(self, density_map: np.ndarray) -> np.ndarray:
        """
        Calculates macroscopic flow (Q) using a linear Greenshields velocity model.
        Q = rho * v(rho)
        """
        # Velocity decreases linearly to 0 as density approaches rho_max
        velocity_field = self.v_f * (1 - (density_map / self.rho_max))
        velocity_field = np.clip(velocity_field, 0, self.v_f)
        return density_map * velocity_field

    def _calculate_wave_speed(self, density_map: np.ndarray) -> np.ndarray:
        """
        Calculates the kinematic wave speed (c = dQ/dRho).
        Negative wave speed indicates a backward-propagating shockwave.
        """
        return self.v_f * (1 - 2 * (density_map / self.rho_max))

    def detect_and_propagate(self, density_map: np.ndarray, cell_size: float = 1.0) -> dict:
        """
        Analyzes a 2D density map to locate shockwave fronts and calculate their severity.
        """
        logger.info("Analyzing density matrix for kinematic shockwaves...")
        
        flux = self._calculate_flux(density_map)
        wave_speeds = self._calculate_wave_speed(density_map)
        
        # Calculate spatial gradients of density
        grad_y, grad_x = np.gradient(density_map, cell_size)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

        # Define a shockwave front as an area with high density gradient AND negative wave speed
        shockwave_mask = (gradient_magnitude > 1.5) & (wave_speeds < -0.2)
        
        front_coordinates = np.argwhere(shockwave_mask)
        severity_index = float(np.sum(gradient_magnitude[shockwave_mask]))
        
        risk_level = "NORMAL"
        if severity_index > 20:
            risk_level = "CRITICAL (Crush Hazard)"
        elif severity_index > 10:
            risk_level = "HIGH (Turbulence Active)"
        elif len(front_coordinates) > 0:
            risk_level = "ELEVATED"

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "shockwave_risk": risk_level,
            "severity_index": round(severity_index, 4),
            "front_count": len(front_coordinates),
            "max_backward_wave_speed": round(float(np.min(wave_speeds)), 4),
            "average_flux": round(float(np.mean(flux)), 4),
            "shockwave_fronts": [
                {"x": int(coord[1]), "y": int(coord[0]), "gradient": round(gradient_magnitude[coord[0], coord[1]], 2)}
                for coord in front_coordinates[:10]  # Return top 10 fronts to save payload size
            ]
        }

        logger.info(f"[SHOCKWAVE ENGINE] Risk={risk_level} | Fronts={len(front_coordinates)} | Severity={severity_index:.2f}")
        return report

if __name__ == "__main__":
    engine = ShockwavePropagationEngine()
    
    # Create a mock 2D grid with a sudden bottleneck (density spike)
    base_density = np.random.uniform(0.5, 2.0, (20, 20))
    # Inject a dense shockwave block
    base_density[8:12, 10:15] = np.random.uniform(5.0, 6.8, (4, 5))
    
    result = engine.detect_and_propagate(base_density)
    
    print("\n========== SHOCKWAVE REPORT ==========\n")
    for key, value in result.items():
        if key == "shockwave_fronts":
            print(f"{key}: {len(value)} listed.")
        else:
            print(f"{key}: {value}")