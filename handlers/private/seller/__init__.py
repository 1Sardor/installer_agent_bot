from aiogram import Router

from .start import router as start_router
from .work_service import router as work_router

router = Router()

router.include_routers(
    start_router,
    work_router,
)
