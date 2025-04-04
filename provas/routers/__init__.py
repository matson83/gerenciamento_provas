from ninja import Router
from .admin import router as admin_router
from .participante import router as participante_router

router = Router()
router.add_router("/admin", admin_router)
router.add_router("/participante", participante_router)
