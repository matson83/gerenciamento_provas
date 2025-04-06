# provas/routers/__init__.py
from provas.routers.admin import router as admin_router


def include_routers(api):
    api.add_router("/provas/admin", admin_router)
    
