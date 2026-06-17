from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    rgb_density: List[int]
    thermal_density: List[int]
    infrared_density: List[int]
    flow_vectors: List[List[int]]
    turbulence_score: int
