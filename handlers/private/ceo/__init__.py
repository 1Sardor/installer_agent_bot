from aiogram import Router

from .start import router as start_router
from .user_service import router as hodimlar_router

router = Router()

router.include_routers(
    start_router,
    hodimlar_router,
)
