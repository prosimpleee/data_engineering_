from pydantic.dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


@dataclass
class Player:
    id: int
    name: str
    username: str
    age: int
    created_at: datetime


@dataclass
class PlayersList:
    count: int
    players: List[Player]


class UpdatePlayerSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    username: Optional[str]
    age: Optional[int]
    created_at: Optional[datetime]
