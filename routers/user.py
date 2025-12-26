# backend/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut, UserWithCharacterOut
from services.user_service import get_or_create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_or_get_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_or_create_user(db, payload.telegram_id, payload.username)
    return user

@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/auth", response_model=UserWithCharacterOut)
async def auth_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_or_create_user(db, payload.telegram_id, payload.username)
    stmt = select(User).options(selectinload(User.character)).filter_by(id=user.id)
    result = await db.execute(stmt)
    return result.scalar_one()


