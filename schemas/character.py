# backend/schemas/character.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class CharacterCreate(BaseModel):
    """
    Входные данные для создания персонажа.
    Обычно достаточно user_id, остальное подтянется из дефолтов SQLAlchemy-модели.
    """
    user_id: int


class CharacterOut(BaseModel):
    """
    Полный ответ API для персонажа.
    Включает все ключевые поля, которые хотим показывать клиенту.
    """
    id: int
    user_id: int
    level: int
    xp: int
    energy: int

    str: int
    agi: int
    lck: int
    end: int
    int: int

    gold: int
    pills: int
    bucks: int

    bandage_count: int
    medkit_count: int
    energy_drink_count: int

    # JSON‑поле: список/словарь купленных предметов
    #purchased_items: Optional[Dict[str, Any]]

    lifesteal: float
    regen: float

    stat_points_unspent: int
    battle_state: str

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # позволяет конвертировать из SQLAlchemy-модели
