import asyncio
import logging
from handlers.public.bot import group_router
from handlers.private.register import user_router
from config import dp, bot


async def main():
    dp.include_routers(
        group_router,
        user_router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
