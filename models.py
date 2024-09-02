from pydantic import BaseModel
from typing import Optional

class Position(BaseModel):
    company: str
    title: str
    location: str
    link: Optional[str] = None
    description: Optional[str] = None
    posted_date: Optional[str] = None

