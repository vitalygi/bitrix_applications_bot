from aiogram import Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from data.db import Database
from middleware.delete_messages_middleware import DeleteMessagesMiddleware
from middleware.flags_check_middleware import CheckFlagsMiddleware
from middleware.user_middleware import UserInjectionMiddleware

from .user.__main__ import include_routers as _include_user_routers
from .admin.__main__ import include_routers as _include_admin_routers
from .manager.__main__ import include_routers as _include_manager_routers


async def register_middleware(router: Dispatcher, services=None):
    router.update.outer_middleware(UserInjectionMiddleware())
    router.update.outer_middleware(DeleteMessagesMiddleware())

    router.message.middleware(CheckFlagsMiddleware())
    router.callback_query.middleware(CheckFlagsMiddleware())


async def register_dispatcher(storage=MemoryStorage()):
    await Database.init()

    dp = Dispatcher(storage=storage)

    router = Router()
    start_route = Router()

    await register_middleware(dp)
    _include_admin_routers(router)
    _include_manager_routers(router)
    _include_user_routers(router)

    dp.include_routers(router, start_route)
    setup_dialogs(dp)
    return dp
