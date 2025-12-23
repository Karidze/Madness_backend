import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import F
from core.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

from aiogram import Router
router = Router()
dp.include_router(router)

@router.message(F.text == "/start")
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть Madness RPG",
                    web_app=WebAppInfo(url="https://madnessfrontend-production.up.railway.app")
                )
            ]
        ]
    )
    await message.answer("Добро пожаловать в Madness RPG!", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
