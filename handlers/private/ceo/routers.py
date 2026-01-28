from handlers.private.ceo.start import router as start_router
from handlers.private.ceo.user_service import router as user_router

def register_admin_routers(main_router):
    main_router.include_router(user_router)
    main_router.include_router(start_router)
