from aiogram import Router

from filters.admin_filter import IsAdmin
from .main_handler import router as main_admin_router
from .verify_user_handler import router as verify_user_router



def set_filters(router: Router):
    """
    Устанавливает фильтры для сообщений и обратных вызовов в зависимости от того, является ли пользователь администратором.

    :param router: Объект маршрутизатора для установки фильтров.
    :type router: Router

    :return: Нет возвращаемого значения.
    """
    router.message.filter(IsAdmin())
    router.callback_query.filter(IsAdmin())
def include_routers(main_router: Router) -> None:
    router = Router()
    set_filters(router)

    router.include_routers(main_admin_router)
    router.include_routers(verify_user_router)
    main_router.include_router(router)
