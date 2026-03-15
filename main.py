import asyncio
import logging
from handlers.private.ceo import router as ceo_router
from handlers.private.seller import router as seller_router
from handlers.private.agent import router as agent_router
from handlers.public.start import router as start_router
from config import dp, bot
from send_works import start_scheduler

async def main():
    dp.include_routers(
        ceo_router,
        agent_router,
        seller_router,
        start_router,
    )
    start_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
