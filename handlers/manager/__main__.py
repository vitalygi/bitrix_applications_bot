from aiogram import Router

from filters.manager_filter import IsManager
from filters.register_filter import IsRegistered
from .main_handler import router as main_manager_router




def set_filters(router: Router):
    router.message.filter(IsManager())
    router.callback_query.filter(IsManager())
def include_routers(main_router: Router) -> None:
    router = Router()
    set_filters(router)

    router.include_routers(main_manager_router)
    main_router.include_router(router)
