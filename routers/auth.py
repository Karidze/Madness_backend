import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiogram.utils.token import TokenValidationError

from core.config import settings
from db.database import get_db
from models.user import User
from services.user_service import get_or_create_user

# Настройка логирования, чтобы видеть ошибки в консоли бэкенда
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

class TelegramAuthIn(BaseModel):
    initData: str

def create_jwt_for_user(user: User) -> str:
    # Ваша логика создания токена
    return f"TEST_TOKEN_USER_{user.id}"

@router.post("/telegram")
async def auth_telegram(payload: TelegramAuthIn, db: AsyncSession = Depends(get_db)):
    # 1. Отладка входящих данных
    logger.info("--- New Auth Attempt ---")
    logger.info(f"Received initData: {payload.initData[:50]}...") # Печатаем начало для проверки
    logger.info(f"Using BOT_TOKEN: {settings.BOT_TOKEN[:5]}...***") # Проверяем, что токен не пустой

    try:
        # 2. Валидация данных с использованием ИМЕНОВАННЫХ аргументов
        # В aiogram 3.x порядок: (token, init_data) или именованные
        params = safe_parse_webapp_init_data(
            token=settings.BOT_TOKEN,
            init_data=payload.initData
        )
        logger.info("Validation successful!")

    except TokenValidationError:
        logger.error("Validation error: Invalid BOT_TOKEN format")
        raise HTTPException(status_code=403, detail="Invalid Bot Token format")
    except ValueError as e:
        # Чаще всего падает здесь, если hash не совпадает
        logger.error(f"Validation error (Hash mismatch): {e}")
        raise HTTPException(status_code=403, detail=f"Hash mismatch or data expired: {e}")
    except Exception as e:
        logger.error(f"Unknown validation error: {e}")
        raise HTTPException(status_code=403, detail=f"Unexpected error: {e}")

    # 3. Извлечение данных пользователя
    user_obj = params.user
    if not user_obj or not user_obj.id:
        logger.warning("User data missing in initData")
        raise HTTPException(status_code=400, detail="Missing user in initData")

    telegram_id = user_obj.id
    username = user_obj.username or "Unknown"

    try:
        # 4. Сохранение/получение пользователя в БД
        user = await get_or_create_user(db, telegram_id, username)
        token = create_jwt_for_user(user)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
            },
        }
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during user creation")