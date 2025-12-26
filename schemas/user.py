# backend/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.character import CharacterOut

class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None

class UserOut(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    is_active: Optional[bool]
    is_banned: Optional[bool]

    class Config:
        from_attributes = True

class UserWithCharacterOut(UserOut):
    character: Optional[CharacterOut] = None
