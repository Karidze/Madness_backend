from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.database import get_db
from models.character import Character
from schemas.character import CharacterCreate, CharacterOut

router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterOut)
async def create_character(payload: CharacterCreate, db: AsyncSession = Depends(get_db)):
    character = Character(user_id=payload.user_id)
    db.add(character)
    await db.commit()
    await db.refresh(character)
    return character

@router.get("/", response_model=list[CharacterOut])
async def list_characters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Character))
    characters = result.scalars().all()
    return characters

@router.get("/{character_id}", response_model=CharacterOut)
async def get_character(character_id: int, db: AsyncSession = Depends(get_db)):
    character = await db.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
