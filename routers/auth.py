# backend/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import parse_qsl
import hmac
import hashlib
import json
import time

from core.config import settings
from db.database import get_db
from models.user import User
from services.user_service import get_or_create_user   # <-- используем сервис

router = APIRouter(prefix="/auth", tags=["auth"])


class TelegramAuthIn(BaseModel):
    initData: str


def verify_init_data(init_data: str, bot_token: str) -> dict:
    """
    Валидирует initData от Telegram, возвращает params как dict, если всё ок.
    """
    params = dict(parse_qsl(init_data, keep_blank_values=True))

    received_hash = params.get("hash")
    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash in initData")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params.items()) if k != "hash"
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        raise HTTPException(status_code=403, detail="Invalid Telegram initData signature")

    # Проверка свежести
    try:
        auth_date = int(params.get("auth_date", "0"))
    except ValueError:
        auth_date = 0
    if auth_date and (time.time() - auth_date) > 3600:
        raise HTTPException(status_code=403, detail="Auth data expired")

    return params


def create_jwt_for_user(user: User) -> str:
    """
    Заглушка для JWT. В проде используй PyJWT/JOSE.
    """
    return f"TEST_TOKEN_USER_{user.id}"


@router.post("/telegram")
async def auth_telegram(payload: TelegramAuthIn, db: AsyncSession = Depends(get_db)):
    # 1) Проверяем подпись initData
    params = verify_init_data(payload.initData, settings.BOT_TOKEN)

    # 2) Достаём объект user из initData
    if "user" not in params:
        raise HTTPException(status_code=400, detail="Missing user in initData")

    try:
        user_obj = json.loads(params["user"])
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user JSON in initData")

    telegram_id = user_obj.get("id")
    username = user_obj.get("username") or "Unknown"

    if not isinstance(telegram_id, int):
        raise HTTPException(status_code=400, detail="Invalid user id in initData")

    # 3) Ищем/создаём юзера через сервис
    user = await get_or_create_user(db, telegram_id, username)

    # 4) Выдаём токен
    token = create_jwt_for_user(user)

    # 5) Возвращаем фронту
    return {
        "token": token,
        "user": {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
        },
    }
