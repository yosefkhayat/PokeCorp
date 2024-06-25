from pydantic import BaseModel
from typing import List, Optional


class Pokemon(BaseModel):
    id: Optional[int] = None
    name: str
    height: float
    weight: float
    types: List[str] = []

