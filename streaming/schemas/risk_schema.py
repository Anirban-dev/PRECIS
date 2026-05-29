from pydantic import BaseModel


class RiskSchema(BaseModel):

    risk_level: str

    confidence: float

    score: float