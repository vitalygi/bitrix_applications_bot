from aiogram import Router

from .start_handler import router as start_router
from .register_handler import router as register_router
from .create_application import router as create_application_router


def include_routers(main_router: Router) -> None:
    router = Router()
    router.include_routers(create_application_router)
    router.include_routers(register_router)
    router.include_routers(start_router)
    main_router.include_router(router)
