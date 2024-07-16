from aiogram import Router

from .start_handler import router as start_router


def include_routers(main_router: Router) -> None:
    router = Router()
    router.include_routers(start_router)
    main_router.include_router(router)
