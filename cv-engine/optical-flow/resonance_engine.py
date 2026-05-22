# cv_engine/optical_flow/resonance_engine.py
import numpy as np
from collections import deque

class ResonanceEngine:
    def __init__(self, buffer_size=30):
        self.magnitude_history = deque(maxlen=buffer_size)

    def analyze_waves(self, current_magnitude):
        """
        Detects shockwaves by analyzing temporal spikes in motion magnitude.
        """
        avg_mag = np.mean(current_magnitude)
        self.magnitude_history.append(avg_mag)
        
        # Detect sudden surge (Potential Shockwave)
        shockwave_detected = False
        if len(self.magnitude_history) == self.magnitude_history.maxlen:
            prev_avg = np.mean(list(self.magnitude_history)[:-1])
            if avg_mag > (prev_avg * 2.5): # Threshold for surge
                shockwave_detected = True
        
        # Resonance Score: Variance of the mean intensity over time
        resonance_score = float(np.var(self.magnitude_history)) if len(self.magnitude_history) > 1 else 0.0
        
        return {
            "resonance_score": round(resonance_score, 4),
            "shockwave_detected": shockwave_detected
        }