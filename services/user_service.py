# /backend/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from models.user import User

async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str) -> User:
    telegram_id = int(telegram_id)
    q = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = q.scalar_one_or_none()
    if user:
        user.last_login = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
        return user
    new_user = User(
        telegram_id=telegram_id,
        username=username,
        created_at=datetime.utcnow(),
        is_active=True,
        is_banned=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    print("🔎 get_or_create_user called with:", telegram_id, type(telegram_id))
    return new_user
