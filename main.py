import asyncio
import logging
from handlers.public.start import router as public_router
from handlers.private.agent.start import router as agent_router
from handlers.private.ceo.start import router as ceo_router
from handlers.private.seller.start import router as seller_router

from config import dp, bot


async def main():
    dp.include_routers(
        ceo_router,
        agent_router,
        seller_router,
        public_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
