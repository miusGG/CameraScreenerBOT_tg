"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .user import user_router
from .texter import all_text_router


routers_list = [
    admin_router,
    user_router,
    all_text_router,
]

__all__ = [
    "routers_list",
]
