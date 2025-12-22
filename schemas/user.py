# backend/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """
    Входные данные для создания пользователя.
    Минимум: telegram_id (обязательно), username (опционально).
    Остальные поля выставляются дефолтами на уровне БД/модели.
    """
    telegram_id: str
    username: Optional[str] = None


class UserOut(BaseModel):
    """
    Полный ответ API для пользователя.
    Возвращаем ключевые поля, включая служебные (created_at, last_login, флаги).
    """
    id: int
    telegram_id: str
    username: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool
    is_banned: bool

    class Config:
        # Позволяет создавать эту схему напрямую из SQLAlchemy-модели (ORM-объекта).
        # FastAPI будет автоматически конвертировать типы при возврате.
        from_attributes = True
