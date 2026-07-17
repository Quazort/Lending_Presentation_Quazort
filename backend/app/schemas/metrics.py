from pydantic import BaseModel


class StatusMetrics(BaseModel):
    SUCCESS: int = 0
    FAILED: int = 0
    AI_ERROR: int = 0
    TOTAL: int = 0

class ToneMetrics(BaseModel):
    NEGATIVE: int = 0
    POSITIVE: int = 0
    NEUTRAL: int = 0

class MetricsSchema(BaseModel):
    request_statuses: StatusMetrics
    tone_of_appeals: ToneMetrics