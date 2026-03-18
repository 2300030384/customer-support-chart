from pydantic import BaseModel, Field
from typing import Optional, List

class EscalationRule(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    keywords: List[str] = []
    sentiment_threshold: Optional[float] = None
    enabled: bool = True
