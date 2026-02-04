from aiogram import Router

from .start import router as start_router
from .user_service import router as hodimlar_router
from .clients_service import router as clients_router
from .razxod_service import router as razxod_router
from .statistics_service import router as statistics_router
from .active_works import router as active_works_router
from .work_service import router as work_router

router = Router()

router.include_routers(
    start_router,
    hodimlar_router,
    clients_router,
    razxod_router,
    statistics_router,
    active_works_router,
    work_router,
)
