# provas/routers/__init__.py
from provas.routers.admin import router as admin_router
from provas.routers.participante import router as participante_router

def include_routers(api):
    api.add_router("/provas/admin", admin_router)
    api.add_router("/provas/participante", participante_router)
