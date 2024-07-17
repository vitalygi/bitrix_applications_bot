from aiogram import Router

from .main_handler import router as main_admin_router
from .verify_user_handler import router as verify_user_router

def include_routers(main_router: Router) -> None:
    router = Router()
    router.include_routers(main_admin_router)
    router.include_routers(verify_user_router)
    main_router.include_router(router)
