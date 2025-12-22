# backend/init_db.py
import asyncio
from db.database import create_tables
from models import user, character

async def main():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())
