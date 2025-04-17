import asyncio
from aiogram import Bot, Dispatcher
from payment_check_handler import router

BOT_TOKEN = "7618485150:AAHsOnDRfUa1oqK0jDBzY-alSzt0PIHfW_M"

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
