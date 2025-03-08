from .user import router as user_router
from .reunion import router as reunion_router
from .staff import router as staff_router
from .cours import router as cours_router
from .equipe import router as equipe_router
from .points import router as points_router

__all__ = ["user_router", "reunion_router", "staff_router", "cours_router", "equipe_router", "points_router"]