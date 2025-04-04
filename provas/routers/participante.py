# provas/routers/participante.py

from ninja import Router

router = Router(tags=["Participante"])

@router.get("/ping")
def participante_ping(request):
    return {"message": "pong from participante"}
