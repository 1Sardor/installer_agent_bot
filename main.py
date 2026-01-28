import asyncio
import logging
from handlers.public.start import router as public_router
from handlers.private.ceo import router as ceo_router

from config import dp, bot


async def main():
    dp.include_routers(
        ceo_router,
        public_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
