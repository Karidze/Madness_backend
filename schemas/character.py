#schemas/character.py

from pydantic import BaseModel, constr
from typing import Optional, Dict, Any
from datetime import datetime

class CharacterCreate(BaseModel):
    user_id: int
    gender: str  # "male" или "female"
    username: constr(min_length=3, max_length=16)
    avatar_full: Optional[str] = None
    avatar_card: Optional[str] = None

class CharacterOut(BaseModel):
    id: int
    user_id: int
    gender: str
    username: str
    avatar_full: Optional[str]
    avatar_card: Optional[str]

    class Config:
        from_attributes = True
