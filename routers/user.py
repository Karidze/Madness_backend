# backend/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверим, что telegram_id уникален
    q = await db.execute(select(User).where(User.telegram_id == payload.telegram_id))
    existing = q.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="User with this telegram_id already exists")

    user = User(
        telegram_id=payload.telegram_id,
        username=payload.username,
        # остальные поля возьмут дефолты из модели (is_active=True, is_banned=False, created_at=now)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user  # будет сериализован в UserOut автоматически


@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users



@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
