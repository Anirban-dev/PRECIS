import random


class OpticalFlowService:
    def analyze(self):
        avg_velocity = round(random.uniform(0.5, 5.0), 2)
        max_velocity = round(random.uniform(avg_velocity, avg_velocity + 3), 2)

        if avg_velocity < 1.5:
            direction = "STABLE"
        elif avg_velocity < 3:
            direction = "MOVING"
        else:
            direction = "SURGE"

        return {
            "avg_velocity": avg_velocity,
            "max_velocity": max_velocity,
            "flow_direction": direction,
        }
