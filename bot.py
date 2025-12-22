import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from core.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Открыть Madness RPG",
            web_app=WebAppInfo(url="https://your-render-app.onrender.com")  # ссылка на фронтенд
        )
    )
    await message.answer("Добро пожаловать в Madness RPG!", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
