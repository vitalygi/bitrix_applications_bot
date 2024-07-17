from aiogram import Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from data.db import Database
from middleware.flags_check_middleware import CheckFlagsMiddleware
from middleware.user_middleware import UserInjectionMiddleware

from .user.__main__ import include_routers as _include_user_routers
from .admin.__main__ import include_routers as _include_admin_routers

async def register_middleware(router: Dispatcher, services=None):

    router.update.outer_middleware(UserInjectionMiddleware())

    router.message.middleware(CheckFlagsMiddleware())
    router.callback_query.middleware(CheckFlagsMiddleware())


async def register_dispatcher(storage=MemoryStorage()):
    await Database.init()

    dp = Dispatcher(storage=storage)

    router = Router()
    start_route = Router()

    await register_middleware(dp)
    _include_admin_routers(router)
    _include_user_routers(router)
    dp.include_routers(router, start_route)

    return dp
