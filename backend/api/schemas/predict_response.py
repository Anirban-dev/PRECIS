from pydantic import BaseModel
from typing import Any


class PredictResponse(BaseModel):
    success: bool
    result: dict[str, Any]