# provas/routers/admin.py

from ninja import Router

router = Router(tags=["Admin"])

@router.get("/ping")
def admin_ping(request):
    return {"message": "pong from admin"}
