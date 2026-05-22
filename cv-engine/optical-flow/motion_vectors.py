# cv_engine/optical_flow/motion_vectors.py
import numpy as np

class MotionVectorEngine:
    def __init__(self):
        pass

    def compute_vector_field_stats(self, flow):
        """
        Analyzes the vector field to extract global movement trends.
        """
        fx = flow[..., 0]
        fy = flow[..., 1]
        
        # Calculate mean vector (global direction)
        mean_dx = np.mean(fx)
        mean_dy = np.mean(fy)
        
        # Calculate consistency (how many vectors align with the mean)
        magnitude = np.sqrt(fx**2 + fy**2)
        dot_product = (fx * mean_dx + fy * mean_dy) / (np.sqrt(mean_dx**2 + mean_dy**2) + 1e-6)
        directional_sync = float(np.mean(dot_product / (magnitude + 1e-6)))
        
        return {
            "mean_dx": float(mean_dx),
            "mean_dy": float(mean_dy),
            "directional_sync": round(directional_sync, 4)
        }