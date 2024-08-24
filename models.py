from pydantic import BaseModel
from typing import Optional

class Position(BaseModel):
    title: str
    location: str
    link: Optional[str] = None
    description: Optional[str] = None

