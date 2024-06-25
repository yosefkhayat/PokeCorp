from pydantic import BaseModel
from typing import List


class Pokemon(BaseModel):
    id: int
    name: str
    height: float
    weight: float
    types: List[str] = []

