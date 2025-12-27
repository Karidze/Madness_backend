#backend/bot.py

import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import F
from core.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

from aiogram import Router
router = Router()
dp.include_router(router)

# локальный backend во время разработки
BACKEND_URL = "https://madnessbackend-production.up.railway.app/api"  # если settings.API_PREFIX = "/api"

@router.message(F.text == "/start")
async def start(message: types.Message):
    # дергаем backend, чтобы создать/обновить юзера
    async with aiohttp.ClientSession() as session:
        payload = {
            "telegram_id": str(message.from_user.id),
            "username": message.from_user.username
        }
        try:
            async with session.post(f"{BACKEND_URL}/users/", json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print("User created or loaded:", data)
                else:
                    err = await resp.text()
                    print(f"Backend error {resp.status}: {err}")
        except Exception as e:
            print("Error calling backend:", e)

    # клавиатура для открытия фронта
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть Madness RPG",
                    web_app=WebAppInfo(url="https://subprofitable-distractingly-allen.ngrok-free.dev")  # локальный фронт
                )
            ]
        ]
    )
    await message.answer("Добро пожаловать в Madness RPG!", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
